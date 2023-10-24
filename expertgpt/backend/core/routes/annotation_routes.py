from uuid import UUID
from fastapi import APIRouter, Depends, Query
from auth.auth_bearer import AuthBearer

from models.annotation import AnnotationMessage
from models.brains import Brain

annotation_router = APIRouter()

# generate annotation
@annotation_router.post(
    "/annotation",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
    ],
    tags=["Annotation"],
)
async def generate_annotation(
    text: str,
    brain_id: UUID
) -> AnnotationMessage:
    """
    Generate annotation.
    """
    brain = Brain(id=brain_id)
    return brain.generate_annotation(text)
    