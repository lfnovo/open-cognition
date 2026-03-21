from surreal_basics import repo_create, repo_query

from open_cognition.utils import ensure_dict


async def create_review_log(data: dict) -> dict:
    return ensure_dict(await repo_create("review_log", data))


async def get_reviews_for_flashcard(flashcard_id: str) -> list[dict]:
    return await repo_query(
        "SELECT * FROM review_log WHERE flashcard_id = $fc_id ORDER BY reviewed_at DESC",
        {"fc_id": f"flashcard:{flashcard_id}"},
    )


async def get_struggling_cards(limit: int = 10) -> list[dict]:
    return await repo_query(
        """
        SELECT
            flashcard_id,
            count() AS total_reviews,
            math::sum(IF quality < 3 THEN 1 ELSE 0 END) AS errors,
            math::mean(quality) AS avg_quality
        FROM review_log
        GROUP BY flashcard_id
        ORDER BY avg_quality ASC
        LIMIT $limit
        """,
        {"limit": limit},
    )
