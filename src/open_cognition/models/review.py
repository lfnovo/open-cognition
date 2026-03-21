from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    quality: int = Field(..., ge=0, le=5)


class ReviewResponse(BaseModel):
    flashcard_id: str
    quality: int
    interval_before: int
    interval_after: int
    ease_factor: float
    repetitions: int
    due_date: datetime


class StrugglingCardResponse(BaseModel):
    flashcard_id: str
    front: str
    back: str
    topic_name: Optional[str] = None
    total_reviews: int
    errors: int
    avg_quality: float
