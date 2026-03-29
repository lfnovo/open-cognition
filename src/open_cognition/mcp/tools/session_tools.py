from open_cognition.mcp.server import mcp
from open_cognition.models.artifact import ArtifactCreate
from open_cognition.models.flashcard import FlashcardCreate
from open_cognition.models.resource import ResourceCreate
from open_cognition.models.session_log import SessionLogCreate
from open_cognition.services import (
    artifact_service,
    flashcard_service,
    resource_service,
    session_log_service,
    topic_service,
)


@mcp.tool()
async def start_session(topic_id: str) -> str:
    """Start a study session for a topic. Returns full context: topic info,
    existing flashcards, resources, and artifacts."""
    topic = await topic_service.get_topic(topic_id)
    cards = await flashcard_service.get_flashcards(topic_id)
    resources = await resource_service.get_resources(topic_id)
    artifacts = await artifact_service.get_artifacts(topic_id)

    lines = [f"# Study Session: {topic.name}\n"]
    if topic.description:
        lines.append(f"{topic.description}\n")

    lines.append(f"## Existing Flashcards ({len(cards)})")
    for c in cards:
        lines.append(f"- Q: {c.front} | A: {c.back}")

    lines.append(f"\n## Resources ({len(resources)})")
    for r in resources:
        lines.append(f"- [{r.type}] {r.title}: {r.content_or_url}")

    lines.append(f"\n## Artifacts ({len(artifacts)})")
    for a in artifacts:
        lines.append(f"- [{a.type}] {a.title}")

    return "\n".join(lines)


@mcp.tool()
async def end_session(
    topic_id: str,
    session_type: str = "study",
    summary: str | None = None,
    outputs: dict | None = None,
) -> str:
    """End a study session, persist outputs and log the session.
    - topic_id: the topic studied
    - session_type: 'study', 'feynman', 'review', or 'import'
    - summary: brief description of what was covered
    - outputs: {flashcards: [...], resources: [...], artifacts: [...]}"""
    # Validate topic exists before creating any outputs
    from surreal_basics import SurrealDBQueryError

    try:
        topic = await topic_service.get_topic(topic_id)
    except (KeyError, IndexError, SurrealDBQueryError):
        return f"Error: topic '{topic_id}' not found. Cannot end session."

    outputs = outputs or {}
    results = []

    fc_count = 0
    for fc in outputs.get("flashcards", []):
        if "topic_ids" not in fc or not fc["topic_ids"]:
            fc["topic_ids"] = [topic_id]
        card = await flashcard_service.create_flashcard(FlashcardCreate(**fc))
        results.append(f"Flashcard: {card.front}")
        fc_count += 1

    res_count = 0
    for res in outputs.get("resources", []):
        if "topic_ids" not in res or not res["topic_ids"]:
            res["topic_ids"] = [topic_id]
        r = await resource_service.create_resource(ResourceCreate(**res))
        results.append(f"Resource: {r.title}")
        res_count += 1

    art_count = 0
    for art in outputs.get("artifacts", []):
        if "topic_ids" not in art or not art["topic_ids"]:
            art["topic_ids"] = [topic_id]
        a = await artifact_service.create_artifact(ArtifactCreate(**art))
        results.append(f"Artifact: {a.title}")
        art_count += 1

    # Log the session
    log = await session_log_service.create_session_log(
        SessionLogCreate(
            topic_id=topic_id,
            topic_name=topic.name,
            session_type=session_type,
            summary=summary,
            flashcards_created=fc_count,
            artifacts_created=art_count,
            resources_created=res_count,
        )
    )

    output_lines = [f"Session logged (id: {log.id})"]
    if results:
        output_lines.append(f"Created:\n" + "\n".join(f"- {r}" for r in results))

    return "\n".join(output_lines)


@mcp.tool()
async def get_session_logs(topic_id: str | None = None) -> str:
    """Get session history, optionally filtered by topic ID."""
    logs = await session_log_service.get_session_logs(topic_id)
    if not logs:
        return "No session logs found."
    lines = []
    for log in logs:
        date = log.created.strftime("%Y-%m-%d %H:%M") if log.created else "?"
        lines.append(f"- [{log.session_type}] **{log.topic_name}** ({date})")
        if log.summary:
            lines.append(f"  {log.summary}")
        outputs = []
        if log.flashcards_created:
            outputs.append(f"{log.flashcards_created} cards")
        if log.artifacts_created:
            outputs.append(f"{log.artifacts_created} artifacts")
        if log.resources_created:
            outputs.append(f"{log.resources_created} resources")
        if outputs:
            lines.append(f"  Outputs: {', '.join(outputs)}")
    return "\n".join(lines)
