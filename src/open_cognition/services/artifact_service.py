from open_cognition.models.artifact import (
    ArtifactCreate,
    ArtifactResponse,
    ArtifactUpdate,
    TopicInfo,
)
from open_cognition.repositories import artifact_repo
from open_cognition.utils import strip_table_prefix


def _to_response(record: dict) -> ArtifactResponse:
    record = record.copy()
    record["id"] = strip_table_prefix(record["id"])
    # Parse topic_details if present (from graph query)
    raw_topics = record.pop("topic_details", None) or []
    topic_details = []
    for t in raw_topics:
        if isinstance(t, dict) and "id" in t and "name" in t:
            topic_details.append(
                TopicInfo(id=strip_table_prefix(t["id"]), name=t["name"])
            )
    record["topic_details"] = topic_details
    return ArtifactResponse(**record)


async def create_artifact(data: ArtifactCreate) -> ArtifactResponse:
    topic_ids = data.topic_ids
    artifact_data = data.model_dump(exclude={"topic_ids"})

    record = await artifact_repo.create_artifact(artifact_data)
    art_id = strip_table_prefix(record["id"])

    for tid in topic_ids:
        await artifact_repo.relate_artifact_to_topic(art_id, tid)

    response = _to_response(record)
    response.topics = topic_ids
    return response


async def get_artifacts(topic_id: str | None = None) -> list[ArtifactResponse]:
    if topic_id:
        records = await artifact_repo.get_artifacts_by_topic(topic_id)
    else:
        records = await artifact_repo.get_all_artifacts()
    return [_to_response(r) for r in records]


async def get_artifacts_with_topics(
    topic_id: str | None = None,
) -> list[ArtifactResponse]:
    if topic_id:
        records = await artifact_repo.get_artifacts_by_topic_with_topics(topic_id)
    else:
        records = await artifact_repo.get_all_artifacts_with_topics()
    return [_to_response(r) for r in records]


async def update_artifact(artifact_id: str, data: ArtifactUpdate) -> ArtifactResponse:
    record = await artifact_repo.update_artifact(
        artifact_id, data.model_dump(exclude_none=True)
    )
    return _to_response(record)
