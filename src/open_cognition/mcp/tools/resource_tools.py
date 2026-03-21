from open_cognition.mcp.server import mcp
from open_cognition.models.resource import ResourceCreate
from open_cognition.services import resource_service


@mcp.tool()
async def get_resources(topic_id: str | None = None) -> str:
    """List resources, optionally filtered by topic ID."""
    resources = await resource_service.get_resources(topic_id)
    if not resources:
        return "No resources found."
    lines = []
    for r in resources:
        lines.append(f"- [{r.type}] **{r.title}** (id: {r.id})")
        lines.append(f"  {r.content_or_url}")
    return "\n".join(lines)


@mcp.tool()
async def create_resource(
    type: str, title: str, content_or_url: str, topic_ids: list[str]
) -> str:
    """Create a resource (pdf, video, link, or markdown) linked to topics."""
    resource = await resource_service.create_resource(
        ResourceCreate(
            type=type, title=title, content_or_url=content_or_url, topic_ids=topic_ids
        )
    )
    return f"Created resource '{resource.title}' (id: {resource.id}, type: {resource.type})"
