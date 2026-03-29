from datetime import datetime, timezone

from surreal_basics import repo_create, repo_query, repo_relate, repo_select, repo_update

from open_cognition.utils import ensure_dict, ensure_list


async def create_flashcard(data: dict) -> dict:
    if "due_date" not in data:
        data["due_date"] = datetime.now(timezone.utc)
    return ensure_dict(await repo_create("flashcard", data))


async def get_flashcard(flashcard_id: str) -> dict:
    return ensure_dict(await repo_select(f"flashcard:{flashcard_id}"))


async def get_all_flashcards() -> list[dict]:
    return ensure_list(await repo_select("flashcard"))


async def get_flashcards_by_topic(topic_id: str) -> list[dict]:
    return await repo_query(
        "SELECT * FROM flashcard WHERE ->belongs_to->topic CONTAINS type::thing('topic', $tid)",
        {"tid": topic_id},
    )


async def get_due_flashcards(topic_id: str | None = None) -> list[dict]:
    now = datetime.now(timezone.utc)
    if topic_id:
        return await repo_query(
            "SELECT * FROM flashcard WHERE due_date <= $now AND ->belongs_to->topic CONTAINS type::thing('topic', $tid) ORDER BY due_date ASC",
            {"now": now, "tid": topic_id},
        )
    return await repo_query(
        "SELECT * FROM flashcard WHERE due_date <= $now ORDER BY due_date ASC",
        {"now": now},
    )


async def update_flashcard(flashcard_id: str, data: dict) -> dict:
    return ensure_dict(await repo_update("flashcard", flashcard_id, data))


async def relate_flashcard_to_topic(flashcard_id: str, topic_id: str) -> list[dict]:
    return await repo_relate(
        f"flashcard:{flashcard_id}", "belongs_to", f"topic:{topic_id}"
    )


async def relate_resource_to_flashcard(
    resource_id: str, flashcard_id: str
) -> list[dict]:
    return await repo_relate(
        f"resource:{resource_id}", "supports", f"flashcard:{flashcard_id}"
    )
