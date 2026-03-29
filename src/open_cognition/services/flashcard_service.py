from open_cognition.models.flashcard import (
    FlashcardCreate,
    FlashcardResponse,
    FlashcardUpdate,
)
from open_cognition.repositories import flashcard_repo
from open_cognition.utils import strip_table_prefix


def _to_response(record: dict) -> FlashcardResponse:
    record = record.copy()
    record["id"] = strip_table_prefix(record["id"])
    return FlashcardResponse(**record)


async def create_flashcard(data: FlashcardCreate) -> FlashcardResponse:
    topic_ids = data.topic_ids
    resource_ids = data.resource_ids
    flashcard_data = data.model_dump(exclude={"topic_ids", "resource_ids"})

    record = await flashcard_repo.create_flashcard(flashcard_data)
    fc_id = strip_table_prefix(record["id"])

    for tid in topic_ids:
        await flashcard_repo.relate_flashcard_to_topic(fc_id, tid)

    for rid in resource_ids:
        await flashcard_repo.relate_resource_to_flashcard(rid, fc_id)

    response = _to_response(record)
    response.topics = topic_ids
    return response


async def get_flashcards(topic_id: str | None = None) -> list[FlashcardResponse]:
    if topic_id:
        records = await flashcard_repo.get_flashcards_by_topic(topic_id)
    else:
        records = await flashcard_repo.get_all_flashcards()
    return [_to_response(r) for r in records]


async def get_due_flashcards(
    topic_id: str | None = None,
) -> list[FlashcardResponse]:
    records = await flashcard_repo.get_due_flashcards(topic_id)
    return [_to_response(r) for r in records]


async def update_flashcard(
    flashcard_id: str, data: FlashcardUpdate
) -> FlashcardResponse:
    record = await flashcard_repo.update_flashcard(
        flashcard_id, data.model_dump(exclude_none=True)
    )
    return _to_response(record)
