from surreal_basics import repo_create, repo_query, repo_relate, repo_select, repo_update

from open_cognition.utils import ensure_dict, ensure_list


async def create_resource(data: dict) -> dict:
    return ensure_dict(await repo_create("resource", data))


async def get_resource(resource_id: str) -> dict:
    return ensure_dict(await repo_select(f"resource:{resource_id}"))


async def get_all_resources() -> list[dict]:
    return ensure_list(await repo_select("resource"))


async def get_resources_by_topic(topic_id: str) -> list[dict]:
    return await repo_query(
        "SELECT * FROM resource WHERE ->belongs_to->topic CONTAINS type::thing('topic', $tid)",
        {"tid": topic_id},
    )


async def update_resource(resource_id: str, data: dict) -> dict:
    return ensure_dict(await repo_update("resource", resource_id, data))


async def relate_resource_to_topic(resource_id: str, topic_id: str) -> list[dict]:
    return await repo_relate(
        f"resource:{resource_id}", "belongs_to", f"topic:{topic_id}"
    )


async def relate_resource_to_flashcard(
    resource_id: str, flashcard_id: str
) -> list[dict]:
    return await repo_relate(
        f"resource:{resource_id}", "supports", f"flashcard:{flashcard_id}"
    )


async def get_resources_for_flashcard(flashcard_id: str) -> list[dict]:
    return await repo_query(
        "SELECT * FROM resource WHERE ->supports->flashcard CONTAINS type::thing('flashcard', $fid)",
        {"fid": flashcard_id},
    )
