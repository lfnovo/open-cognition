from open_cognition.models.session_log import (
    SessionLogCreate,
    SessionLogResponse,
)
from open_cognition.repositories import session_log_repo
from open_cognition.utils import strip_table_prefix


def _to_response(record: dict) -> SessionLogResponse:
    record = record.copy()
    record["id"] = strip_table_prefix(record["id"])
    return SessionLogResponse(**record)


async def create_session_log(data: SessionLogCreate) -> SessionLogResponse:
    record = await session_log_repo.create_session_log(data.model_dump())
    return _to_response(record)


async def get_session_logs(
    topic_id: str | None = None,
) -> list[SessionLogResponse]:
    if topic_id:
        records = await session_log_repo.get_session_logs_by_topic(topic_id)
    else:
        records = await session_log_repo.get_all_session_logs()
    return [_to_response(r) for r in records]
