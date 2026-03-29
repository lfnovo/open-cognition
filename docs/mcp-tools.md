# MCP Tools

open-cognition exposes 20 tools via MCP for integration with compatible LLMs (Claude Desktop, Claude Code, etc.).

## How to Use

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "open-cognition": {
      "command": "/path/to/uv",
      "args": ["run", "--directory", "/path/to/open-cognition", "python", "run_mcp.py"],
      "env": {
        "SURREAL_URL": "ws://localhost:8000/rpc",
        "SURREAL_USER": "root",
        "SURREAL_PASSWORD": "root",
        "SURREAL_NAMESPACE": "open-cognition",
        "SURREAL_DATABASE": "test"
      }
    }
  }
}
```

### Claude Code

Add `.mcp.json` at the root of the project where you will use it:

```json
{
  "mcpServers": {
    "open-cognition": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/open-cognition", "python", "run_mcp.py"],
      "env": { ... }
    }
  }
}
```

## Available Tools

### Topics

| Tool | Description |
|------|-------------|
| `get_topics()` | Lists all topics with subtopic hierarchy |
| `create_topic(name, description?, parent_ids?)` | Creates a topic, optionally as a subtopic |
| `update_topic(topic_id, name?, description?)` | Updates name or description |
| `relate_topics(parent_id, child_id)` | Creates a parent/child relationship between topics |

### Flashcards

| Tool | Description |
|------|-------------|
| `get_flashcards(topic_id?)` | Lists flashcards, optional filter by topic |
| `get_due_flashcards(topic_id?)` | Lists flashcards pending review (due_date <= now) |
| `create_flashcard(front, back, topic_ids, resource_ids?)` | Creates a flashcard |
| `create_flashcards_batch(cards)` | Creates multiple flashcards at once |
| `review_flashcard(flashcard_id, quality)` | Records a review and updates SM-2. Quality: 0/2/3/4/5 |

`cards` is a list of objects `{front, back, topic_ids, resource_ids?}`.

### Resources

| Tool | Description |
|------|-------------|
| `get_resources(topic_id?)` | Lists resources, optional filter by topic |
| `create_resource(type, title, content_or_url, topic_ids)` | Creates a resource |

Types: `pdf`, `video`, `link`, `markdown`.

### Artifacts

| Tool | Description |
|------|-------------|
| `get_artifacts(topic_id?)` | Lists artifacts, optional filter by topic |
| `create_artifact(type, title, content, topic_ids)` | Creates an artifact in markdown |

Types: `summary`, `feynman`, `schema`, `notes`.

### Doubts

| Tool | Description |
|------|-------------|
| `get_doubts(topic_id?, status?)` | Lists doubts, optional filter by topic and status |
| `create_doubt(content, flashcard_id?, topic_id?)` | Creates a doubt |
| `resolve_doubt(doubt_id)` | Marks a doubt as resolved |

### Struggling Cards

| Tool | Description |
|------|-------------|
| `get_struggling_cards(topic_id?)` | Lists cards with low ease factor / many errors |

### Study Session

| Tool | Description |
|------|-------------|
| `start_session(topic_id)` | Starts a session. Returns full context: cards, resources, artifacts |
| `end_session(topic_id, session_type, summary?, outputs?)` | Ends a session, persists outputs and records a log |
| `get_session_logs(topic_id?)` | Queries session history |

**Parameters for `end_session`:**
- `topic_id` — topic studied
- `session_type` — `study`, `feynman`, `review`, `import`
- `summary` — brief summary of what was covered (optional)
- `outputs` — outputs to persist (optional):
```json
{
  "flashcards": [{"front": "...", "back": "...", "topic_ids": [...]}],
  "resources": [{"type": "link", "title": "...", "content_or_url": "...", "topic_ids": [...]}],
  "artifacts": [{"type": "summary", "title": "...", "content": "...", "topic_ids": [...]}]
}
```

## Return Format

All tools return **human-readable strings** (not JSON), as they are consumed by LLMs. The REST API returns structured JSON for programmatic consumption.
