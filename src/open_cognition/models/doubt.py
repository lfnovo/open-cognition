from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class DoubtCreate(BaseModel):
    content: str
    flashcard_id: Optional[str] = None
    topic_id: Optional[str] = None


class DoubtUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[Literal["open", "resolved"]] = None


class DoubtResponse(BaseModel):
    id: str
    content: str
    status: str = "open"
    flashcard_id: Optional[str] = None
    topic_id: Optional[str] = None
    topic_name: Optional[str] = None
    created: Optional[datetime] = None
