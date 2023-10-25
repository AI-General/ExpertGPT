from uuid import UUID
from fastapi import APIRouter, Depends, Query
from auth.auth_bearer import AuthBearer

from models.annotation import AnnotationMessage, AnnotationQuery
from models.brains import Brain

annotation_router = APIRouter()

# generate annotation
@annotation_router.post(
    "/annotation/{brain_id}",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
    ],
    tags=["Annotation"],
)
async def generate_annotation(
    brain_id: UUID,
    annotation_query: AnnotationQuery
) -> AnnotationMessage:
    """
    Generate annotation.
    """
    brain = Brain(id=brain_id)
    return_value = brain.generate_annotation(annotation_query.text)
    return return_value

    