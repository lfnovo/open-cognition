from surreal_basics import repo_create, repo_query

from open_cognition.utils import ensure_dict


async def create_session_log(data: dict) -> dict:
    return ensure_dict(await repo_create("session_log", data))


async def get_all_session_logs() -> list[dict]:
    return await repo_query(
        "SELECT * FROM session_log ORDER BY created DESC"
    )


async def get_session_logs_by_topic(topic_id: str) -> list[dict]:
    return await repo_query(
        "SELECT * FROM session_log WHERE topic_id = $tid ORDER BY created DESC",
        {"tid": topic_id},
    )
