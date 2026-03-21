from surreal_basics import repo_create, repo_query, repo_update

from open_cognition.utils import ensure_dict


async def create_doubt(data: dict) -> dict:
    return ensure_dict(await repo_create("doubt", data))


async def get_all_doubts() -> list[dict]:
    return await repo_query("SELECT * FROM doubt ORDER BY created DESC")


async def get_doubts_by_status(status: str) -> list[dict]:
    return await repo_query(
        "SELECT * FROM doubt WHERE status = $status ORDER BY created DESC",
        {"status": status},
    )


async def get_doubts_by_topic(topic_id: str) -> list[dict]:
    return await repo_query(
        "SELECT * FROM doubt WHERE topic_id = $tid ORDER BY created DESC",
        {"tid": topic_id},
    )


async def get_doubts_filtered(
    topic_id: str | None = None, status: str | None = None
) -> list[dict]:
    conditions = []
    params = {}
    if status:
        conditions.append("status = $status")
        params["status"] = status
    if topic_id:
        conditions.append("topic_id = $tid")
        params["tid"] = topic_id
    where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
    return await repo_query(
        f"SELECT * FROM doubt{where} ORDER BY created DESC", params
    )


async def update_doubt(doubt_id: str, data: dict) -> dict:
    return ensure_dict(await repo_update("doubt", doubt_id, data))
