from typing import List, Optional
from pydantic import BaseModel

class Annotation(BaseModel):
    origin: str
    type: str
    comments: Optional[str]
    analysis: Optional[str]

class AnnotationMessage(BaseModel):
    status_code: int
    message: str = ''
    annotations: List[Annotation] = []