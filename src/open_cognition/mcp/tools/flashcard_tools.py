from open_cognition.mcp.server import mcp
from open_cognition.models.flashcard import FlashcardCreate
from open_cognition.models.review import ReviewRequest
from open_cognition.services import flashcard_service, review_service


@mcp.tool()
async def get_flashcards(topic_id: str | None = None) -> str:
    """List flashcards, optionally filtered by topic ID."""
    cards = await flashcard_service.get_flashcards(topic_id)
    if not cards:
        return "No flashcards found."
    lines = []
    for c in cards:
        lines.append(f"- **Q:** {c.front}")
        lines.append(f"  **A:** {c.back}")
        lines.append(f"  (id: {c.id}, due: {c.due_date}, reps: {c.repetitions})")
    return "\n".join(lines)


@mcp.tool()
async def get_due_flashcards(topic_id: str | None = None) -> str:
    """List flashcards that are due for review (due_date <= now), optionally filtered by topic ID."""
    cards = await flashcard_service.get_due_flashcards(topic_id)
    if not cards:
        return "No flashcards due for review."
    lines = [f"{len(cards)} card(s) due for review:\n"]
    for c in cards:
        lines.append(f"- **Q:** {c.front}")
        lines.append(f"  (id: {c.id}, interval: {c.interval}d, reps: {c.repetitions})")
    return "\n".join(lines)


@mcp.tool()
async def create_flashcard(
    front: str,
    back: str,
    topic_ids: list[str],
    resource_ids: list[str] | None = None,
) -> str:
    """Create a single flashcard linked to topics and optionally to resources."""
    card = await flashcard_service.create_flashcard(
        FlashcardCreate(
            front=front, back=back, topic_ids=topic_ids, resource_ids=resource_ids or []
        )
    )
    return f"Created flashcard (id: {card.id}): {front}"


@mcp.tool()
async def create_flashcards_batch(cards: list[dict]) -> str:
    """Create multiple flashcards at once.
    Each card should have: front, back, topic_ids, resource_ids (optional)."""
    created = []
    for c in cards:
        if "resource_ids" not in c or c.get("resource_ids") is None:
            c["resource_ids"] = []
        card = await flashcard_service.create_flashcard(FlashcardCreate(**c))
        created.append(card)
    return f"Created {len(created)} flashcards:\n" + "\n".join(
        f"- {c.front} (id: {c.id})" for c in created
    )


@mcp.tool()
async def review_flashcard(flashcard_id: str, quality: int) -> str:
    """Record a flashcard review and update spaced repetition schedule.
    Quality scale: 0-5 where 0=forgot completely, 1=incorrect but recognized answer, 2=incorrect but seemed familiar, 3=correct with difficulty, 4=correct with hesitation, 5=perfect response. Scores below 3 count as incorrect and reset the card.
    Returns the updated schedule."""
    result = await review_service.review_flashcard(
        flashcard_id, ReviewRequest(quality=quality)
    )
    return (
        f"Reviewed card {result.flashcard_id}: quality={result.quality}\n"
        f"Interval: {result.interval_before}d → {result.interval_after}d\n"
        f"Next review: {result.due_date.strftime('%Y-%m-%d')}\n"
        f"EF: {result.ease_factor}, Reps: {result.repetitions}"
    )


@mcp.tool()
async def get_struggling_cards(topic_id: str | None = None, limit: int = 10) -> str:
    """Get flashcards with lowest average review quality (most struggled with).
    Useful to identify knowledge gaps and cards that need attention."""
    cards = await review_service.get_struggling_cards(topic_id, limit)
    if not cards:
        return "No struggling cards found (not enough review history yet)."
    lines = [f"{len(cards)} card(s) you're struggling with:\n"]
    for c in cards:
        lines.append(f"- **Q:** {c.front}")
        lines.append(f"  **A:** {c.back}")
        context = [f"avg quality: {c.avg_quality}", f"{c.errors}/{c.total_reviews} errors"]
        if c.topic_name:
            context.append(f"topic: {c.topic_name}")
        lines.append(f"  ({', '.join(context)}, id: {c.flashcard_id})")
    return "\n".join(lines)
