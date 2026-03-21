from open_cognition.models.resource import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from open_cognition.repositories import resource_repo
from open_cognition.utils import strip_table_prefix


def _to_response(record: dict) -> ResourceResponse:
    record = record.copy()
    record["id"] = strip_table_prefix(record["id"])
    return ResourceResponse(**record)


async def create_resource(data: ResourceCreate) -> ResourceResponse:
    topic_ids = data.topic_ids
    flashcard_ids = data.flashcard_ids
    resource_data = data.model_dump(exclude={"topic_ids", "flashcard_ids"})

    record = await resource_repo.create_resource(resource_data)
    res_id = strip_table_prefix(record["id"])

    for tid in topic_ids:
        await resource_repo.relate_resource_to_topic(res_id, tid)

    for fid in flashcard_ids:
        await resource_repo.relate_resource_to_flashcard(res_id, fid)

    response = _to_response(record)
    response.topics = topic_ids
    return response


async def get_resources(topic_id: str | None = None) -> list[ResourceResponse]:
    if topic_id:
        records = await resource_repo.get_resources_by_topic(topic_id)
    else:
        records = await resource_repo.get_all_resources()
    return [_to_response(r) for r in records]


async def update_resource(resource_id: str, data: ResourceUpdate) -> ResourceResponse:
    record = await resource_repo.update_resource(
        resource_id, data.model_dump(exclude_none=True)
    )
    return _to_response(record)


async def get_resources_for_flashcard(flashcard_id: str) -> list[ResourceResponse]:
    records = await resource_repo.get_resources_for_flashcard(flashcard_id)
    return [_to_response(r) for r in records]
