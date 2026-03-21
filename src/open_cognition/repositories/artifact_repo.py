from surreal_basics import repo_create, repo_query, repo_relate, repo_select, repo_update

from open_cognition.utils import ensure_dict, ensure_list


async def create_artifact(data: dict) -> dict:
    return ensure_dict(await repo_create("artifact", data))


async def get_artifact(artifact_id: str) -> dict:
    return ensure_dict(await repo_select(f"artifact:{artifact_id}"))


async def get_all_artifacts() -> list[dict]:
    return ensure_list(await repo_select("artifact"))


async def get_all_artifacts_with_topics() -> list[dict]:
    return await repo_query(
        "SELECT *, ->belongs_to->topic.* AS topic_details FROM artifact"
    )


async def get_artifacts_by_topic_with_topics(topic_id: str) -> list[dict]:
    return await repo_query(
        "SELECT *, ->belongs_to->topic.* AS topic_details FROM artifact WHERE ->belongs_to->topic CONTAINS type::thing('topic', $tid)",
        {"tid": topic_id},
    )


async def get_artifacts_by_topic(topic_id: str) -> list[dict]:
    return await repo_query(
        "SELECT * FROM artifact WHERE ->belongs_to->topic CONTAINS type::thing('topic', $tid)",
        {"tid": topic_id},
    )


async def update_artifact(artifact_id: str, data: dict) -> dict:
    return ensure_dict(await repo_update("artifact", artifact_id, data))


async def relate_artifact_to_topic(artifact_id: str, topic_id: str) -> list[dict]:
    return await repo_relate(
        f"artifact:{artifact_id}", "belongs_to", f"topic:{topic_id}"
    )
