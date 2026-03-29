from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class ResourceCreate(BaseModel):
    type: Literal["pdf", "video", "link", "markdown"]
    title: str
    content_or_url: str
    topic_ids: list[str] = []
    flashcard_ids: list[str] = []


class ResourceUpdate(BaseModel):
    type: Optional[Literal["pdf", "video", "link", "markdown"]] = None
    title: Optional[str] = None
    content_or_url: Optional[str] = None


class ResourceResponse(BaseModel):
    id: str
    type: str
    title: str
    content_or_url: str
    topics: list[str] = []
    created: Optional[datetime] = None
    updated: Optional[datetime] = None
