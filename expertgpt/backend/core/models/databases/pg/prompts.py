from enum import Enum
from uuid import UUID
from pydantic import BaseModel

class PromptStatusEnum(str, Enum):
    private = "private"
    public = "public"

class Prompt(BaseModel):
    id: UUID
    title: str
    content: str
    status: PromptStatusEnum = PromptStatusEnum.private

class CreatePromptProperties(BaseModel):
    """Properties that can be received on prompt creation"""
    title: str
    content: str
    status: PromptStatusEnum = PromptStatusEnum.private