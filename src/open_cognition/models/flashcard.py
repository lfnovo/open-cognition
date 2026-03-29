from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FlashcardCreate(BaseModel):
    front: str
    back: str
    topic_ids: list[str] = []
    resource_ids: list[str] = []


class FlashcardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None


class FlashcardResponse(BaseModel):
    id: str
    front: str
    back: str
    due_date: Optional[datetime] = None
    interval: int = 0
    ease_factor: float = 2.5
    repetitions: int = 0
    topics: list[str] = []
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
