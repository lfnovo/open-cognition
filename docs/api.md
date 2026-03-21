# API REST

Todos os endpoints estão prefixados com `/api`. A documentação interativa (Swagger) está disponível em `/api/docs` quando o server está rodando.

## Tópicos

### `GET /api/topics`

Lista todos os tópicos com hierarquia de subtópicos.

**Response:** `200 OK`
```json
[
  {
    "id": "abc123",
    "name": "Transformers",
    "description": "Arquitetura de deep learning",
    "created": "2026-03-21T15:00:00Z",
    "updated": "2026-03-21T15:00:00Z",
    "subtopics": [
      {"id": "def456", "name": "Attention Mechanism", ...}
    ]
  }
]
```

### `POST /api/topics`

Cria um tópico.

**Body:**
```json
{"name": "Transformers", "description": "opcional"}
```

**Response:** `201 Created`

### `GET /api/topics/{id}`

Retorna um tópico pelo ID.

### `PATCH /api/topics/{id}`

Atualiza nome e/ou descrição.

**Body:**
```json
{"name": "novo nome", "description": "nova descrição"}
```

### `POST /api/topics/{id}/subtopics`

Cria relação pai/filho.

**Body:**
```json
{"child_id": "id_do_subtopico"}
```

### `DELETE /api/topics/{id}/subtopics/{child_id}`

Remove relação pai/filho.

## Flashcards

### `GET /api/flashcards`

Lista flashcards. Filtro opcional por tópico.

**Query params:** `topic_id` (opcional)

### `POST /api/flashcards`

Cria um flashcard.

**Body:**
```json
{
  "front": "Pergunta",
  "back": "Resposta",
  "topic_ids": ["abc123"],
  "resource_ids": ["xyz789"]
}
```

### `GET /api/flashcards/due`

Lista flashcards com `due_date <= agora`. Filtro opcional por tópico.

**Query params:** `topic_id` (opcional)

### `PATCH /api/flashcards/{id}`

Atualiza frente e/ou verso.

### `POST /api/flashcards/{id}/review`

Registra uma revisão e recalcula SM-2.

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

## Recursos

### `GET /api/resources`

Lista recursos. Filtro opcional por tópico.

**Query params:** `topic_id` (opcional)

### `POST /api/resources`

Cria um recurso.

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

**Tipos válidos:** `pdf`, `video`, `link`, `markdown`

### `PATCH /api/resources/{id}`

Atualiza tipo, título e/ou conteúdo.

## Artefatos

### `GET /api/artifacts`

Lista artefatos. Filtro opcional por tópico.

**Query params:** `topic_id` (opcional)

### `POST /api/artifacts`

Cria um artefato.

**Body:**
```json
{
  "type": "summary",
  "title": "Resumo: Transformers",
  "content": "# Transformers\n\nConteúdo em markdown...",
  "topic_ids": ["abc123"]
}
```

**Tipos válidos:** `summary`, `feynman`, `schema`, `notes`

### `PATCH /api/artifacts/{id}`

Atualiza tipo, título e/ou conteúdo.

## Health

### `GET /health`

Retorna status do server.

```json
{"status": "ok"}
```
