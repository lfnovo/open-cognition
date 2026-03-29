from open_cognition.mcp.server import mcp
from open_cognition.models.topic import TopicCreate, TopicUpdate
from open_cognition.services import topic_service


@mcp.tool()
async def get_topics() -> str:
    """List all topics with their subtopic hierarchy."""
    topics = await topic_service.get_all_topics()
    if not topics:
        return "No topics found."
    lines = []
    for t in topics:
        lines.append(f"- {t.name} (id: {t.id})")
        if t.description:
            lines.append(f"  Description: {t.description}")
        if t.subtopics:
            for s in t.subtopics:
                lines.append(f"  - {s.name} (id: {s.id})")
    return "\n".join(lines)


@mcp.tool()
async def create_topic(
    name: str, description: str | None = None, parent_ids: list[str] | None = None
) -> str:
    """Create a new topic, optionally as a subtopic of existing topics."""
    topic = await topic_service.create_topic(
        TopicCreate(name=name, description=description)
    )
    if parent_ids:
        for pid in parent_ids:
            await topic_service.add_subtopic(pid, topic.id)
    return f"Created topic '{topic.name}' (id: {topic.id})"


@mcp.tool()
async def update_topic(
    topic_id: str, name: str | None = None, description: str | None = None
) -> str:
    """Update a topic's name or description."""
    topic = await topic_service.update_topic(
        topic_id, TopicUpdate(name=name, description=description)
    )
    return f"Updated topic '{topic.name}' (id: {topic.id})"


@mcp.tool()
async def relate_topics(parent_id: str, child_id: str) -> str:
    """Create a parent-child relationship between two topics."""
    await topic_service.add_subtopic(parent_id, child_id)
    return f"Related topic {child_id} as subtopic of {parent_id}"


