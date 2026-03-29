# Architecture

## Overview

```
┌─────────────────┐     ┌─────────────────┐
│   Claude (LLM)  │     │    UI Web        │
│   via Skill     │     │    HTMX/Jinja2   │
└────────┬────────┘     └────────┬─────────┘
         │                       │
    ┌────▼────┐            ┌─────▼─────┐
    │   MCP   │            │  Routes   │
    │  Tools  │            │  (FastAPI)│
    └────┬────┘            └─────┬─────┘
         │                       │
         └───────────┬───────────┘
                     │
              ┌──────▼──────┐
              │   Services  │
              │  (logic)    │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │ Repositories│
              │ (queries)   │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │  SurrealDB  │
              │ (surreal-   │
              │  basics)    │
              └─────────────┘
```

## Layers

### Routes (FastAPI)

REST endpoints under `/api/` that receive/return JSON. Prefixed with `/api` to avoid conflicting with the frontend HTML routes.

### Frontend Routes

HTML routes that serve Jinja2 + HTMX templates. They share the same services as the REST API.

### MCP Tools (FastMCP)

Tools exposed via the MCP protocol for any compatible LLM. They import services directly (same process, no HTTP). They return human-readable strings for LLMs, not JSON.

### Services

Business logic. Responsible for:
- Orchestrating operations (create flashcard + create belongs_to relations)
- Converting between internal models (SurrealDB records) and external models (Pydantic responses)
- SM-2 algorithm

### Repositories

SurrealQL queries via surreal-basics. Each entity has its own repository with CRUD operations and graph queries.

### Database (SurrealDB)

SurrealDB as a graph database. SCHEMAFULL tables with relations via `RELATE` (graph edges).

## Data Model

### Tables

| Table | Main Fields |
|-------|-------------|
| `topic` | name, description |
| `flashcard` | front, back, due_date, interval, ease_factor, repetitions |
| `resource` | type, title, content_or_url |
| `artifact` | type, title, content |
| `review_log` | flashcard_id, reviewed_at, quality, interval_before, interval_after |

Timestamps (`created`, `updated`) are added automatically by surreal-basics.

### Relations (Graph Edges)

```
topic  ──has_subtopic──►  topic        # hierarchy
flashcard ──belongs_to──► topic        # card belongs to topic(s)
resource  ──belongs_to──► topic        # resource belongs to topic(s)
resource  ──supports────► flashcard    # resource supports a card
artifact  ──belongs_to──► topic        # artifact belongs to topic(s)
```

Advantage over join tables: native graph queries (`->belongs_to->topic`), no JOINs.

### Indexes

- `idx_flashcard_due_date` — performance for the pending cards query
- `idx_review_log_flashcard` — review history per card
- `idx_review_log_reviewed_at` — temporal queries

## File Structure

```
open-cognition/
├── SKILL.md                          # Skill document for Claude
├── migrations/                       # SurrealQL migrations
├── src/open_cognition/
│   ├── main.py                       # FastAPI app + lifespan (auto-migrations)
│   ├── config.py                     # Loads .env
│   ├── utils.py                      # strip_table_prefix, ensure_dict/list
│   ├── models/                       # Pydantic schemas
│   ├── repositories/                 # SurrealQL queries
│   ├── services/                     # Business logic + SM-2
│   ├── routes/                       # REST endpoints (/api)
│   ├── frontend/
│   │   ├── routes.py                 # HTML routes
│   │   └── templates/                # Jinja2 + HTMX
│   └── mcp/
│       ├── server.py                 # FastMCP server
│       └── tools/                    # Tools by domain
└── tests/
```

## IDs

SurrealDB uses IDs in the format `table:id` (e.g., `topic:abc123`). Internally, all layers work with the clean ID (e.g., `abc123`):

- **Repositories**: add the `table:` prefix when sending queries to SurrealDB
- **Services**: remove the prefix with `strip_table_prefix()` when returning data
- **REST API**: receives and returns clean IDs (e.g., `abc123`)
- **UI**: displays IDs in the `table:id` format (e.g., `topic:abc123`) in copyable badges, to make it easier to reference for the LLM. The copied value includes the prefix.

## Migrations

SurrealQL migrations in `migrations/`, applied automatically on startup via `AsyncMigrationRunner` from surreal-basics. Tracking is stored in the `_sbl_migrations` table.
