from surreal_basics import repo_create, repo_delete, repo_query, repo_relate, repo_select, repo_update

from open_cognition.utils import ensure_dict, ensure_list


async def create_topic(data: dict) -> dict:
    return ensure_dict(await repo_create("topic", data))


async def get_topic(topic_id: str) -> dict:
    return ensure_dict(await repo_select(f"topic:{topic_id}"))


async def get_all_topics() -> list[dict]:
    return ensure_list(await repo_select("topic"))


async def update_topic(topic_id: str, data: dict) -> dict:
    return ensure_dict(await repo_update("topic", topic_id, data))


async def get_topics_with_subtopics() -> list[dict]:
    return ensure_list(
        await repo_query(
            "SELECT *, ->has_subtopic->topic.* AS subtopics FROM topic"
        )
    )


async def add_subtopic(parent_id: str, child_id: str) -> list[dict]:
    return await repo_relate(
        f"topic:{parent_id}", "has_subtopic", f"topic:{child_id}"
    )


async def remove_subtopic(parent_id: str, child_id: str) -> list[dict]:
    return await repo_query(
        "DELETE has_subtopic WHERE in = $parent AND out = $child",
        {"parent": f"topic:{parent_id}", "child": f"topic:{child_id}"},
    )


async def delete_topic(topic_id: str) -> None:
    # Remove all edges involving this topic
    full_id = f"topic:{topic_id}"
    await repo_query(
        "DELETE has_subtopic WHERE in = $id OR out = $id", {"id": full_id}
    )
    await repo_query(
        "DELETE belongs_to WHERE out = $id", {"id": full_id}
    )
    await repo_delete(full_id)
