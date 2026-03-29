from fastapi import APIRouter

from open_cognition.models.topic import (
    SubtopicCreate,
    TopicCreate,
    TopicResponse,
    TopicUpdate,
    TopicWithSubtopics,
)
from open_cognition.services import topic_service

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=list[TopicWithSubtopics])
async def list_topics():
    return await topic_service.get_all_topics()


@router.post("", response_model=TopicResponse, status_code=201)
async def create_topic(data: TopicCreate):
    return await topic_service.create_topic(data)


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(topic_id: str):
    return await topic_service.get_topic(topic_id)


@router.patch("/{topic_id}", response_model=TopicResponse)
async def update_topic(topic_id: str, data: TopicUpdate):
    return await topic_service.update_topic(topic_id, data)


@router.post("/{topic_id}/subtopics", status_code=201)
async def add_subtopic(topic_id: str, data: SubtopicCreate):
    return await topic_service.add_subtopic(topic_id, data.child_id)


@router.delete("/{topic_id}/subtopics/{child_id}", status_code=204)
async def remove_subtopic(topic_id: str, child_id: str):
    await topic_service.remove_subtopic(topic_id, child_id)
