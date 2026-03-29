from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class SessionLogCreate(BaseModel):
    topic_id: str
    topic_name: str
    session_type: Literal["study", "feynman", "review", "import"]
    summary: Optional[str] = None
    flashcards_created: int = 0
    artifacts_created: int = 0
    resources_created: int = 0


class SessionLogResponse(BaseModel):
    id: str
    topic_id: str
    topic_name: str
    session_type: str
    summary: Optional[str] = None
    flashcards_created: int = 0
    artifacts_created: int = 0
    resources_created: int = 0
    created: Optional[datetime] = None
