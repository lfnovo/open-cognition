from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TopicCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TopicResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


class TopicWithSubtopics(TopicResponse):
    subtopics: list[TopicResponse] = []


class SubtopicCreate(BaseModel):
    child_id: str
