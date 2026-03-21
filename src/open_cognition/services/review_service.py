from datetime import datetime, timezone

from loguru import logger

from open_cognition.models.review import ReviewRequest, ReviewResponse, StrugglingCardResponse
from open_cognition.repositories import flashcard_repo, review_repo
from open_cognition.services.sm2_service import calculate_sm2
from open_cognition.utils import strip_table_prefix


async def review_flashcard(flashcard_id: str, data: ReviewRequest) -> ReviewResponse:
    flashcard = await flashcard_repo.get_flashcard(flashcard_id)

    current_interval = flashcard.get("interval", 0)
    current_ef = flashcard.get("ease_factor", 2.5)
    current_reps = flashcard.get("repetitions", 0)

    result = calculate_sm2(
        quality=data.quality,
        repetitions=current_reps,
        ease_factor=current_ef,
        interval=current_interval,
    )

    await flashcard_repo.update_flashcard(
        flashcard_id,
        {
            "interval": result.interval,
            "ease_factor": result.ease_factor,
            "repetitions": result.repetitions,
            "due_date": result.due_date,
        },
    )

    await review_repo.create_review_log(
        {
            "flashcard_id": f"flashcard:{flashcard_id}",
            "reviewed_at": datetime.now(timezone.utc),
            "quality": data.quality,
            "interval_before": current_interval,
            "interval_after": result.interval,
        }
    )

    logger.info(
        f"Reviewed flashcard {flashcard_id}: q={data.quality}, "
        f"interval {current_interval}->{result.interval}d"
    )

    return ReviewResponse(
        flashcard_id=flashcard_id,
        quality=data.quality,
        interval_before=current_interval,
        interval_after=result.interval,
        ease_factor=result.ease_factor,
        repetitions=result.repetitions,
        due_date=result.due_date,
    )


async def get_struggling_cards(
    topic_id: str | None = None, limit: int = 10
) -> list[StrugglingCardResponse]:
    from surreal_basics import repo_query

    records = await review_repo.get_struggling_cards(limit=50)

    # Only include cards that were actually answered incorrectly (quality < 3)
    records = [r for r in records if r.get("errors", 0) > 0]

    results = []
    for r in records:
        fc_id = strip_table_prefix(r["flashcard_id"])
        try:
            card = await flashcard_repo.get_flashcard(fc_id)
        except Exception:
            continue

        # Resolve topic name
        topic_name = None
        edges = await repo_query(
            "SELECT ->belongs_to->topic.* AS topics FROM type::thing('flashcard', $fid)",
            {"fid": fc_id},
        )
        if edges and edges[0].get("topics"):
            first_topic = edges[0]["topics"][0]
            if isinstance(first_topic, dict):
                topic_name = first_topic.get("name")
                # Filter by topic if requested
                if topic_id:
                    topic_ids = [
                        strip_table_prefix(t["id"])
                        for t in edges[0]["topics"]
                        if isinstance(t, dict)
                    ]
                    if topic_id not in topic_ids:
                        continue

        results.append(
            StrugglingCardResponse(
                flashcard_id=fc_id,
                front=card["front"],
                back=card["back"],
                topic_name=topic_name,
                total_reviews=r["total_reviews"],
                errors=r["errors"],
                avg_quality=round(r["avg_quality"], 2),
            )
        )
        if len(results) >= limit:
            break

    return results
