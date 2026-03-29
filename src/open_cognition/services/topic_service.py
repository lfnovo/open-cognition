from open_cognition.models.topic import (
    TopicCreate,
    TopicResponse,
    TopicUpdate,
    TopicWithSubtopics,
)
from open_cognition.repositories import topic_repo
from open_cognition.utils import strip_table_prefix


def _to_response(record: dict) -> TopicResponse:
    record = record.copy()
    record["id"] = strip_table_prefix(record["id"])
    return TopicResponse(**record)


async def create_topic(data: TopicCreate) -> TopicResponse:
    record = await topic_repo.create_topic(data.model_dump(exclude_none=True))
    return _to_response(record)


async def get_topic(topic_id: str) -> TopicResponse:
    record = await topic_repo.get_topic(topic_id)
    return _to_response(record)


async def get_all_topics() -> list[TopicWithSubtopics]:
    records = await topic_repo.get_topics_with_subtopics()
    results = []
    for r in records:
        r = r.copy()
        r["id"] = strip_table_prefix(r["id"])
        subtopics = []
        for s in r.get("subtopics") or []:
            if isinstance(s, dict):
                s = s.copy()
                s["id"] = strip_table_prefix(s["id"])
                subtopics.append(TopicResponse(**s))
        r["subtopics"] = subtopics
        results.append(TopicWithSubtopics(**r))
    return results


async def update_topic(topic_id: str, data: TopicUpdate) -> TopicResponse:
    record = await topic_repo.update_topic(
        topic_id, data.model_dump(exclude_none=True)
    )
    return _to_response(record)


async def add_subtopic(parent_id: str, child_id: str) -> dict:
    await topic_repo.add_subtopic(parent_id, child_id)
    return {"status": "ok"}


async def remove_subtopic(parent_id: str, child_id: str) -> dict:
    await topic_repo.remove_subtopic(parent_id, child_id)
    return {"status": "ok"}


async def delete_topic(topic_id: str) -> None:
    await topic_repo.delete_topic(topic_id)
