from open_cognition.mcp.server import mcp
from open_cognition.models.doubt import DoubtCreate
from open_cognition.services import doubt_service


@mcp.tool()
async def get_doubts(topic_id: str | None = None, status: str | None = "open") -> str:
    """List user doubts/questions, optionally filtered by topic and status (open/resolved)."""
    doubts = await doubt_service.get_doubts(topic_id, status)
    if not doubts:
        return "No doubts found."
    lines = []
    for d in doubts:
        status_icon = "?" if d.status == "open" else "v"
        lines.append(f"- [{status_icon}] {d.content} (id: {d.id})")
        context = []
        if d.topic_name:
            context.append(f"topic: {d.topic_name}")
        if d.flashcard_id:
            context.append(f"card: {d.flashcard_id}")
        if context:
            lines.append(f"  {', '.join(context)}")
    return "\n".join(lines)


@mcp.tool()
async def create_doubt(
    content: str,
    flashcard_id: str | None = None,
    topic_id: str | None = None,
) -> str:
    """Create a doubt or question to explore later. Optionally link to a flashcard and/or topic."""
    doubt = await doubt_service.create_doubt(
        DoubtCreate(content=content, flashcard_id=flashcard_id, topic_id=topic_id)
    )
    return f"Doubt saved (id: {doubt.id}): {doubt.content}"


@mcp.tool()
async def resolve_doubt(doubt_id: str) -> str:
    """Mark a doubt as resolved."""
    doubt = await doubt_service.resolve_doubt(doubt_id)
    return f"Doubt resolved (id: {doubt.id}): {doubt.content}"
