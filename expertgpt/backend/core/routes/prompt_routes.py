from uuid import UUID

from auth import AuthBearer
from fastapi import APIRouter, Depends
from models.prompt import Prompt, CreatePromptProperties, PromptUpdatableProperties
from pg.prompt import create_prompt
from pg.prompt import get_prompt_by_id
from pg.prompt import get_public_prompts
from pg.prompt import update_prompt_by_id

prompt_router = APIRouter()


@prompt_router.get("/prompts", dependencies=[Depends(AuthBearer())], tags=["Prompt"])
async def get_prompts() -> list[Prompt]:
    """
    Retrieve all public prompt
    """

    return get_public_prompts()


@prompt_router.get(
    "/prompts/{prompt_id}", dependencies=[Depends(AuthBearer())], tags=["Prompt"]
)
async def get_prompt(prompt_id: UUID) -> Prompt | None:
    """
    Retrieve a prompt by its id
    """

    return get_prompt_by_id(prompt_id)


@prompt_router.put(
    "/prompts/{prompt_id}", dependencies=[Depends(AuthBearer())], tags=["Prompt"]
)
async def update_prompt(
    prompt_id: UUID, prompt: PromptUpdatableProperties
) -> Prompt | None:
    """
    Update a prompt by its id
    """

    return update_prompt_by_id(prompt_id, prompt)


@prompt_router.post("/prompts", dependencies=[Depends(AuthBearer())], tags=["Prompt"])
async def create_prompt_route(prompt: CreatePromptProperties) -> Prompt | None:
    """
    Create a prompt by its id
    """

    return create_prompt(prompt)
