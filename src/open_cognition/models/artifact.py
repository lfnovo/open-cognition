from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class ArtifactCreate(BaseModel):
    type: Literal["summary", "feynman", "schema", "notes"]
    title: str
    content: str
    topic_ids: list[str] = []


class ArtifactUpdate(BaseModel):
    type: Optional[Literal["summary", "feynman", "schema", "notes"]] = None
    title: Optional[str] = None
    content: Optional[str] = None


class TopicInfo(BaseModel):
    id: str
    name: str


class ArtifactResponse(BaseModel):
    id: str
    type: str
    title: str
    content: str
    topics: list[str] = []
    topic_details: list[TopicInfo] = []
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
