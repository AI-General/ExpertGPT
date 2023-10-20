import os
import time
from typing import List
from uuid import UUID
from uuid import uuid4
from venv import logger

from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from langchain.memory import ZepMemory
from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from auth.check_admin import check_admin
from repository.chat.get_all_chats import get_all_chats
from llm.openai import OpenAIBrainPicking
from models.brains import Brain, Personality
from models.chat import Chat, ChatHistory
from models.chats import ChatQuestion
from models.databases.supabase.supabase import SupabaseDB
from models.settings import LLMSettings, DatabaseSettings, get_supabase_db, get_qdrant_db
from models.users import User
from repository.brain.get_brain_details import get_brain_details
from repository.brain.get_default_user_brain_or_create_new import (
    get_default_user_brain_or_create_new,
)
from repository.chat.create_chat import CreateChatProperties, create_chat
from repository.chat.get_chat_by_id import get_chat_by_id
from repository.chat.get_chat_history import get_chat_history
from repository.chat.get_brain_history import get_brain_history
from repository.chat.get_user_chats import get_user_chats
from repository.chat.update_chat import ChatUpdatableProperties, update_chat
from repository.user_identity.get_user_identity import get_user_identity

ZEP_API_URL = os.getenv("ZEP_API_URL")

session_id = str(uuid4())

try:
    memory = ZepMemory(
        session_id=session_id,
        url=ZEP_API_URL,
        memory_key="chat_history",
        return_messages=True
    )
except Exception as e:
    memory = None
    logger.error(e)

chat_router = APIRouter()


class NullableUUID(UUID):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> UUID | None:
        if v == "":
            return None
        try:
            return UUID(v)
        except ValueError:
            return None


def delete_chat_from_db(supabase_db: SupabaseDB, chat_id):
    try:
        supabase_db.delete_chat_history(chat_id)
    except Exception as e:
        print(e)
        pass
    try:
        supabase_db.delete_chat(chat_id)
    except Exception as e:
        print(e)
        pass


def check_user_limit(
    user: User,
):
    # if user.user_openai_api_key is None:
    date = time.strftime("%Y%m%d")
    max_requests_number = int(os.getenv("MAX_REQUESTS_NUMBER", 1000))

    user.increment_user_request_count(date)
    if int(user.requests_count) >= int(max_requests_number):
        raise HTTPException(
            status_code=429,  # pyright: ignore reportPrivateUsage=none
            # pyright: ignore reportPrivateUsage=none
            detail="You have reached the maximum number of requests for today.",
        )


# get all chats
@chat_router.get("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def get_chats(current_user: User = Depends(get_current_user)):
    """
    Retrieve all chats for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of all chats for the user.

    This endpoint retrieves all the chats associated with the current authenticated user. It returns a list of chat objects
    containing the chat ID and chat name for each chat.
    """
    is_admin = check_admin(current_user)
    if is_admin:
        chats = get_all_chats()
        return {"chats": chats}
    # pyright: ignore reportPrivateUsage=none
    chats = get_user_chats(current_user.id)
    return {"chats": chats}


# delete one chat
@chat_router.delete(
    "/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def delete_chat(chat_id: UUID):
    """
    Delete a specific chat by chat ID.
    """
    supabase_db = get_supabase_db()
    delete_chat_from_db(supabase_db=supabase_db, chat_id=chat_id)
    return {"message": f"{chat_id}  has been deleted."}


# update existing chat metadata
@chat_router.put(
    "/chat/{chat_id}/metadata", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def update_chat_metadata_handler(
    chat_data: ChatUpdatableProperties,
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Chat:
    """
    Update chat attributes
    """

    chat = get_chat_by_id(chat_id)  # pyright: ignore reportPrivateUsage=none
    if str(current_user.id) != chat.user_id:
        raise HTTPException(
            status_code=403,  # pyright: ignore reportPrivateUsage=none
            # pyright: ignore reportPrivateUsage=none
            detail="You should be the owner of the chat to update it.",
        )
    return update_chat(chat_id=chat_id, chat_data=chat_data)


# create new chat
@chat_router.post("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def create_chat_handler(
    chat_data: CreateChatProperties,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new chat with initial chat messages.
    """

    return create_chat(user_id=current_user.id, chat_data=chat_data)


# add new question to chat
@chat_router.post(
    "/chat/{chat_id}/question",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
    ],
    tags=["Chat"],
)
async def create_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    brain_id: NullableUUID
    | UUID
    | None = Query(..., description="The ID of the brain"),
    current_user: User = Depends(get_current_user),
) -> ChatHistory:
    """
    Add a new question to the chat.
    """

    brain_details = get_brain_details(brain_id)

    try:
        check_user_limit(current_user)
        LLMSettings()

        if not brain_id:
            brain_id = get_default_user_brain_or_create_new(
                current_user).brain_id

        personality = Personality(extraversion=brain_details.extraversion,
                                  neuroticism=brain_details.neuroticism, conscientiousness=brain_details.conscientiousness)
        
        model = os.getenv('MODEL', 'gpt-4')
        max_tokens = os.getenv('MAX_TOKENS', 512)
        temperature = os.getenv('TEMPERATURE', 0.9)
        openai_api_key = os.getenv('OPENAI_API_KEY', None)

        gpt_answer_generator = OpenAIBrainPicking(
            chat_id=str(chat_id),
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            brain_id=str(brain_id),
            personality=personality,
            memory=memory,
            prompt_id=chat_question.prompt_id,# pyright: ignore reportPrivateUsage=none
            openai_api_key=openai_api_key
        )

        chat_answer = gpt_answer_generator.generate_answer(  # pyright: ignore reportPrivateUsage=none
            chat_question.question
        )

        return chat_answer
    except HTTPException as e:
        raise e


# stream new question response from chat
@chat_router.post(
    "/chat/{chat_id}/question/stream",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
    ],
    tags=["Chat"],
)
async def create_stream_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    brain_id: NullableUUID
    | UUID
    | None = Query(..., description="The ID of the brain"),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:

    brain_details = get_brain_details(brain_id)

    personality = None
    if (
        brain_details.extraversion is not None
        and brain_details.neuroticism is not None
        and brain_details.conscientiousness is not None
    ):
        personality = Personality(extraversion=brain_details.extraversion,
                                  neuroticism=brain_details.neuroticism, conscientiousness=brain_details.conscientiousness)

    try:
        logger.info(f"Streaming request for {chat_question.model}")
        check_user_limit(current_user)
        if not brain_id:
            brain_id = get_default_user_brain_or_create_new(
                current_user).brain_id

        model = os.getenv('MODEL', 'gpt-4')
        max_tokens = os.getenv('MAX_TOKENS', 512)
        temperature = os.getenv('TEMPERATURE', 0.9)
        openai_api_key = os.getenv('OPENAI_API_KEY', None)

        gpt_answer_generator = OpenAIBrainPicking(
            chat_id=str(chat_id),
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            brain_id=str(brain_id),
            prompt_id=chat_question.prompt_id,# pyright: ignore reportPrivateUsage=none
            openai_api_key=openai_api_key,
            personality=personality,
            streaming=True,
        )

        print("streaming")
        return StreamingResponse(
            gpt_answer_generator.generate_stream(  # pyright: ignore reportPrivateUsage=none
                chat_question.question,
                memory=memory
            ),
            media_type="text/event-stream",
        )

    except HTTPException as e:
        raise e

# stream new question response to brain
@chat_router.post(
    "/chat/brain/{brain_id}/question/stream",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
    ],
    tags=["Chat"],
)
async def create_brain_stream_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    brain_id: UUID,
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:

    brain = Brain(id=brain_id)

    try:
        logger.info(f"Streaming request for {chat_question.model}")

        model = os.getenv('MODEL', 'gpt-4')
        max_tokens = os.getenv('MAX_TOKENS', 512)
        temperature = os.getenv('TEMPERATURE', 0.9)
        openai_api_key = os.getenv('OPENAI_API_KEY', None)

        gpt_answer_generator = OpenAIBrainPicking(
            chat_id=None,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            brain_id=str(brain_id),
            prompt_id=chat_question.prompt_id, # pyright: ignore reportPrivateUsage=none
            openai_api_key=openai_api_key,
            streaming=True,
        )

        print("streaming")
        return StreamingResponse(
            gpt_answer_generator.generate_brain_stream(  # pyright: ignore reportPrivateUsage=none
                chat_question.question
            ),
            media_type="text/event-stream",
        )

    except HTTPException as e:
        raise e


# get chat history
@chat_router.get(
    "/chat/{chat_id}/history", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def get_chat_history_handler(
    chat_id: UUID,
) -> List[ChatHistory]:
    # TODO: RBAC with current_user
    return get_chat_history(chat_id)  # pyright: ignore reportPrivateUsage=none


# get brain history
@chat_router.get(
    "/chat/{brain_id}/brain_history", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def get_brain_history_handler(
    brain_id: UUID,
) -> List[ChatHistory]:
    return get_brain_history(brain_id)


# choose nearest experts
@chat_router.post(
    "/chat/choose",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
    ],
    tags=["Chat"],
)
async def choose_nearest_experts(
    chat_question: ChatQuestion
) -> []:
    query = chat_question.question
    qdrant_db = get_qdrant_db()
    brain_id_scores = qdrant_db.get_nearest_brain_list(query=query, limit=5)
    print(brain_id_scores)

    recommended_brains = [{'name': get_brain_details(brain_score['brain_id']).name, **brain_score} for brain_score in brain_id_scores]
    return recommended_brains

# ChatWithNoAuthenticationNoHistory
@chat_router.post(
    "/chat/unauth/{brain_id}/question",
    tags=["Chat"]
)
async def chat_unauthorized(
    brain_id: NullableUUID,
    chat_question: ChatQuestion
):
    brain_details = get_brain_details(brain_id)

    try:
        personality = Personality(extraversion=brain_details.extraversion,
                                  neuroticism=brain_details.neuroticism, conscientiousness=brain_details.conscientiousness)
        
        model = os.getenv('MODEL', 'gpt-4')
        max_tokens = os.getenv('MAX_TOKENS', 512)
        temperature = os.getenv('TEMPERATURE', 0.9)
        openai_api_key = os.getenv('OPENAI_API_KEY', None)

        gpt_answer_generator = OpenAIBrainPicking(
            chat_id=None,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            brain_id=str(brain_id),
            personality=personality,
            memory=memory,
            prompt_id=chat_question.prompt_id,# pyright: ignore reportPrivateUsage=none
            openai_api_key=openai_api_key
        )

        chat_answer = gpt_answer_generator.generate_answer(  # pyright: ignore reportPrivateUsage=none
            chat_question.question
        )

        return chat_answer
    except HTTPException as e:
        raise e

# ChatWithNoAuthenticationNoHistory
@chat_router.post(
    "/chat/unauth/{brain_id}/question/stream",
    tags=["Chat"]
)
async def chat_unauthorized(
    brain_id: NullableUUID,
    chat_question: ChatQuestion
):
    brain_details = get_brain_details(brain_id)

    try:
        personality = Personality(extraversion=brain_details.extraversion,
                                  neuroticism=brain_details.neuroticism, conscientiousness=brain_details.conscientiousness)
        
        model = os.getenv('MODEL', 'gpt-4')
        max_tokens = os.getenv('MAX_TOKENS', 512)
        temperature = os.getenv('TEMPERATURE', 0.9)
        openai_api_key = os.getenv('OPENAI_API_KEY', None)

        gpt_answer_generator = OpenAIBrainPicking(
            chat_id=None,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            brain_id=str(brain_id),
            personality=personality,
            memory=memory,
            prompt_id=chat_question.prompt_id,# pyright: ignore reportPrivateUsage=none
            openai_api_key=openai_api_key,
            streaming=True
        )

        print("streaming")
        return StreamingResponse(
            gpt_answer_generator.generate_brain_stream(  # pyright: ignore reportPrivateUsage=none
                chat_question.question
            ),
            media_type="text/event-stream",
        )
    except HTTPException as e:
        raise e
