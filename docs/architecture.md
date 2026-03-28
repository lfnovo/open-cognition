# Arquitetura

## Visão Geral

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
              │  (lógica)   │
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

## Camadas

### Routes (FastAPI)

Endpoints REST em `/api/` que recebem/retornam JSON. Prefixados com `/api` para não conflitar com as rotas HTML do frontend.

### Frontend Routes

Rotas HTML que servem templates Jinja2 + HTMX. Compartilham os mesmos services que a API REST.

### MCP Tools (FastMCP)

Tools expostas via protocolo MCP para qualquer LLM compatível. Importam os services diretamente (mesmo processo, sem HTTP). Retornam strings legíveis para LLMs, não JSON.

### Services

Lógica de negócio. Responsáveis por:
- Orquestrar operações (criar flashcard + criar relações belongs_to)
- Converter entre modelos internos (SurrealDB records) e externos (Pydantic responses)
- Algoritmo SM-2

### Repositories

Queries SurrealQL via surreal-basics. Cada entidade tem seu repositório com operações CRUD e queries de grafo.

### Banco de Dados (SurrealDB)

SurrealDB como banco de grafos. Tabelas SCHEMAFULL com relações via `RELATE` (graph edges).

## Modelo de Dados

### Tabelas

| Tabela | Campos principais |
|--------|-------------------|
| `topic` | name, description |
| `flashcard` | front, back, due_date, interval, ease_factor, repetitions |
| `resource` | type, title, content_or_url |
| `artifact` | type, title, content |
| `review_log` | flashcard_id, reviewed_at, quality, interval_before, interval_after |

Timestamps (`created`, `updated`) são adicionados automaticamente pelo surreal-basics.

### Relações (Graph Edges)

```
topic  ──has_subtopic──►  topic        # hierarquia
flashcard ──belongs_to──► topic        # card pertence a tópico(s)
resource  ──belongs_to──► topic        # recurso pertence a tópico(s)
resource  ──supports────► flashcard    # recurso apoia um card
artifact  ──belongs_to──► topic        # artefato pertence a tópico(s)
```

Vantagem sobre tabelas de junção: queries de grafo nativas (`->belongs_to->topic`), sem JOINs.

### Índices

- `idx_flashcard_due_date` — performance na query de cards pendentes
- `idx_review_log_flashcard` — histórico de revisões por card
- `idx_review_log_reviewed_at` — queries temporais

## Estrutura de Arquivos

```
open-cognition/
├── SKILL.md                          # Skill document para o Claude
├── migrations/                       # SurrealQL migrations
├── src/open_cognition/
│   ├── main.py                       # FastAPI app + lifespan (auto-migrations)
│   ├── config.py                     # Carrega .env
│   ├── utils.py                      # strip_table_prefix, ensure_dict/list
│   ├── models/                       # Pydantic schemas
│   ├── repositories/                 # Queries SurrealQL
│   ├── services/                     # Lógica de negócio + SM-2
│   ├── routes/                       # Endpoints REST (/api)
│   ├── frontend/
│   │   ├── routes.py                 # Rotas HTML
│   │   └── templates/                # Jinja2 + HTMX
│   └── mcp/
│       ├── server.py                 # FastMCP server
│       └── tools/                    # Tools por domínio
└── tests/
```

## IDs

SurrealDB usa IDs no formato `table:id` (ex: `topic:abc123`). Internamente, todas as camadas trabalham com o ID limpo (ex: `abc123`):

- **Repositories**: adicionam o prefixo `table:` ao enviar queries para o SurrealDB
- **Services**: removem o prefixo com `strip_table_prefix()` ao retornar dados
- **API REST**: recebe e retorna IDs limpos (ex: `abc123`)
- **UI**: exibe IDs no formato `table:id` (ex: `topic:abc123`) nos badges copiáveis, para facilitar referência ao LLM. O valor copiado inclui o prefixo.

## Migrations

Migrations SurrealQL em `migrations/`, aplicadas automaticamente no startup via `AsyncMigrationRunner` do surreal-basics. O tracking fica na tabela `_sbl_migrations`.
