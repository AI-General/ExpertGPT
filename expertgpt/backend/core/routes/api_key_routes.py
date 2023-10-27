from secrets import token_hex
from typing import List
from uuid import uuid4

from asyncpg.exceptions import UniqueViolationError
from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends
from logger import get_logger
from pg.api_key import create_api_key, delete_api_key, get_api_keys_by_user_id
from models.api_key import ApiKey, ApiKeyInfo
from models.settings import get_supabase_db
from models.users import User

logger = get_logger(__name__)

api_key_router = APIRouter()

@api_key_router.post(
    "/api-key",
    response_model=ApiKey,
    dependencies=[Depends(AuthBearer())],
    tags=["API Key"],
)
async def create_api_key_route(current_user: User = Depends(get_current_user)):
    """
    Create new API key for the current user.

    - `current_user`: The current authenticated user.
    - Returns the newly created API key.

    This endpoint generates a new API key for the current user. The API key is stored in the database and associated with
    the user. It returns the newly created API key.
    """
    create_api_key(current_user)


@api_key_router.delete(
    "/api-key/{key_id}", dependencies=[Depends(AuthBearer())], tags=["API Key"]
)
async def delete_api_key_route(key_id: str, current_user: User = Depends(get_current_user)):
    """
    Delete (deactivate) an API key for the current user.

    - `key_id`: The ID of the API key to delete.

    This endpoint deactivates and deletes the specified API key associated with the current user. The API key is marked
    as inactive in the database.

    """
    delete_api_key(key_id, current_user.id)

    return {"message": "API key deleted."}


@api_key_router.get(
    "/api-keys",
    response_model=List[ApiKeyInfo],
    dependencies=[Depends(AuthBearer())],
    tags=["API Key"],
)
async def get_api_keys(current_user: User = Depends(get_current_user)):
    """
    Get all active API keys for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of active API keys with their IDs and creation times.

    This endpoint retrieves all the active API keys associated with the current user. It returns a list of API key objects
    containing the key ID and creation time for each API key.
    """
    return get_api_keys_by_user_id(current_user.id)
