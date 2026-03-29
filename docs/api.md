# REST API

All endpoints are prefixed with `/api`. Interactive documentation (Swagger) is available at `/api/docs` when the server is running.

## Topics

### `GET /api/topics`

Lists all topics with subtopic hierarchy.

**Response:** `200 OK`
```json
[
  {
    "id": "abc123",
    "name": "Transformers",
    "description": "Deep learning architecture",
    "created": "2026-03-21T15:00:00Z",
    "updated": "2026-03-21T15:00:00Z",
    "subtopics": [
      {"id": "def456", "name": "Attention Mechanism", ...}
    ]
  }
]
```

### `POST /api/topics`

Creates a topic.

**Body:**
```json
{"name": "Transformers", "description": "optional"}
```

**Response:** `201 Created`

### `GET /api/topics/{id}`

Returns a topic by ID.

### `PATCH /api/topics/{id}`

Updates name and/or description.

**Body:**
```json
{"name": "new name", "description": "new description"}
```

### `POST /api/topics/{id}/subtopics`

Creates a parent/child relationship.

**Body:**
```json
{"child_id": "subtopic_id"}
```

### `DELETE /api/topics/{id}/subtopics/{child_id}`

Removes a parent/child relationship.

## Flashcards

### `GET /api/flashcards`

Lists flashcards. Optional filter by topic.

**Query params:** `topic_id` (optional)

### `POST /api/flashcards`

Creates a flashcard.

**Body:**
```json
{
  "front": "Question",
  "back": "Answer",
  "topic_ids": ["abc123"],
  "resource_ids": ["xyz789"]
}
```

### `GET /api/flashcards/due`

Lists flashcards with `due_date <= now`. Optional filter by topic.

**Query params:** `topic_id` (optional)

### `PATCH /api/flashcards/{id}`

Updates front and/or back.

### `POST /api/flashcards/{id}/review`

Records a review and recalculates SM-2.

**Body:**
```json
{"quality": 4}
```

**Response:**
```json
{
  "flashcard_id": "abc123",
  "quality": 4,
  "interval_before": 1,
  "interval_after": 6,
  "ease_factor": 2.5,
  "repetitions": 2,
  "due_date": "2026-03-27T15:00:00Z"
}
```

## Resources

### `GET /api/resources`

Lists resources. Optional filter by topic.

**Query params:** `topic_id` (optional)

### `POST /api/resources`

Creates a resource.

**Body:**
```json
{
  "type": "link",
  "title": "Attention Is All You Need",
  "content_or_url": "https://arxiv.org/abs/1706.03762",
  "topic_ids": ["abc123"],
  "flashcard_ids": ["def456"]
}
```

**Valid types:** `pdf`, `video`, `link`, `markdown`

### `PATCH /api/resources/{id}`

Updates type, title, and/or content.

## Artifacts

### `GET /api/artifacts`

Lists artifacts. Optional filter by topic.

**Query params:** `topic_id` (optional)

### `POST /api/artifacts`

Creates an artifact.

**Body:**
```json
{
  "type": "summary",
  "title": "Summary: Transformers",
  "content": "# Transformers\n\nMarkdown content...",
  "topic_ids": ["abc123"]
}
```

**Valid types:** `summary`, `feynman`, `schema`, `notes`

### `PATCH /api/artifacts/{id}`

Updates type, title, and/or content.

## Health

### `GET /health`

(Note: this endpoint is at the root, not under /api)

Returns server status.

```json
{"status": "ok"}
```
