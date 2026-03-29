from open_cognition.models.doubt import DoubtCreate, DoubtResponse, DoubtUpdate
from open_cognition.repositories import doubt_repo, flashcard_repo
from open_cognition.utils import strip_table_prefix


def _to_response(record: dict) -> DoubtResponse:
    record = record.copy()
    record["id"] = strip_table_prefix(record["id"])
    return DoubtResponse(**record)


async def create_doubt(data: DoubtCreate) -> DoubtResponse:
    doubt_data = data.model_dump(exclude_none=True)

    # If flashcard_id provided, resolve topic from the card's belongs_to edges
    if data.flashcard_id and not data.topic_id:
        try:
            from surreal_basics import repo_query

            edges = await repo_query(
                "SELECT ->belongs_to->topic.* AS topics FROM type::thing('flashcard', $fid)",
                {"fid": data.flashcard_id},
            )
            if edges and edges[0].get("topics"):
                topic = edges[0]["topics"][0]
                if isinstance(topic, dict):
                    doubt_data["topic_id"] = strip_table_prefix(topic["id"])
                    doubt_data["topic_name"] = topic["name"]
        except Exception:
            pass

    # If topic_id provided but no topic_name, resolve name
    if data.topic_id and "topic_name" not in doubt_data:
        try:
            from open_cognition.services import topic_service

            topic = await topic_service.get_topic(data.topic_id)
            doubt_data["topic_name"] = topic.name
        except Exception:
            pass

    record = await doubt_repo.create_doubt(doubt_data)
    return _to_response(record)


async def get_doubts(
    topic_id: str | None = None, status: str | None = None
) -> list[DoubtResponse]:
    records = await doubt_repo.get_doubts_filtered(topic_id, status)
    return [_to_response(r) for r in records]


async def update_doubt(doubt_id: str, data: DoubtUpdate) -> DoubtResponse:
    record = await doubt_repo.update_doubt(
        doubt_id, data.model_dump(exclude_none=True)
    )
    return _to_response(record)


async def resolve_doubt(doubt_id: str) -> DoubtResponse:
    return await update_doubt(doubt_id, DoubtUpdate(status="resolved"))
