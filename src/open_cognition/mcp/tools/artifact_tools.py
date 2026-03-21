from open_cognition.mcp.server import mcp
from open_cognition.models.artifact import ArtifactCreate
from open_cognition.services import artifact_service


@mcp.tool()
async def get_artifacts(topic_id: str | None = None) -> str:
    """List artifacts, optionally filtered by topic ID."""
    artifacts = await artifact_service.get_artifacts(topic_id)
    if not artifacts:
        return "No artifacts found."
    lines = []
    for a in artifacts:
        lines.append(f"- [{a.type}] **{a.title}** (id: {a.id})")
        lines.append(f"  {a.content[:200]}{'...' if len(a.content) > 200 else ''}")
    return "\n".join(lines)


@mcp.tool()
async def create_artifact(
    type: str, title: str, content: str, topic_ids: list[str]
) -> str:
    """Create an artifact (summary, feynman, schema, or notes) linked to topics. Content should be markdown."""
    artifact = await artifact_service.create_artifact(
        ArtifactCreate(type=type, title=title, content=content, topic_ids=topic_ids)
    )
    return f"Created artifact '{artifact.title}' (id: {artifact.id}, type: {artifact.type})"
