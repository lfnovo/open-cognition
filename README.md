# open-cognition

AI-powered learning system with spaced repetition. Study with LLMs, capture knowledge, review with science-backed methods.

## The Problem

When you study with AI (Claude, ChatGPT, etc.), the knowledge gets lost. You learn in one place, take notes in another, create flashcards in a third, and review in isolation. There's no system connecting the dots.

## How it Works

open-cognition bridges the gap between AI-assisted learning and retention:

1. **Study with your LLM** — Claude acts as your Socratic sparring partner via MCP
2. **Capture outputs** — flashcards, summaries, resources, and artifacts are saved automatically
3. **Organize in a knowledge graph** — topics and subtopics you control
4. **Review with spaced repetition** — SM-2 algorithm (same foundation as Anki)
5. **Deepen with Feynman technique** — structured sessions that identify and close knowledge gaps

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

That's it. No database server required — open-cognition uses an embedded local database file by default. Your data stays on your machine.

### Install and Run

```bash
# Run directly (no clone needed)
uvx open-cognition serve
```

Open http://localhost:8080 and start learning.

### Using with Claude Desktop

This is where open-cognition shines. Connect it to Claude Desktop and get a learning partner that knows your knowledge graph.

#### 1. Set up the MCP Server

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "open-cognition": {
      "command": "uvx",
      "args": ["open-cognition", "mcp"]
    }
  }
}
```

That's it — `uvx` handles installation and dependencies automatically.

#### 2. Add the Skill

Download [SKILL.md](https://raw.githubusercontent.com/lfnovo/open-cognition/main/SKILL.md) and add it to your Claude Desktop skills, or include it in your project's `.claude/skills/` folder.

The skill instructs Claude to:
- Be a **Socratic sparring partner** during study sessions — not a lecturer
- Use the **Feynman technique** to identify and close knowledge gaps
- Create high-quality flashcards following strict rules (atomic, active recall, concise)
- Never create topics or cards without your approval
- Track your doubts and struggling cards

#### 3. Start Learning

Talk to Claude naturally:

- *"Let's study Transformers"* → starts a session, loads your existing knowledge
- *"Create flashcards from what we discussed"* → proposes cards for your approval
- *"Let's do a Feynman session on Attention"* → structured gap-finding protocol
- *"What doubts do I have open?"* → reviews pending questions
- *"Which cards am I struggling with?"* → identifies weak spots

## Features

### Web UI

- **Dashboard** — due cards count, struggling cards, quick actions
- **Topics** — create, edit, delete, hierarchical subtopics
- **Review session** — flashcard review with SM-2, quality buttons, progress tracking
- **Artifacts** — markdown + mermaid rendering in modal viewer
- **Resources** — links, PDFs, videos organized by topic
- **Doubts** — capture questions during review, work them later with the LLM
- **Struggling cards** — analytics on most-errored flashcards
- **Copyable IDs** — click any entity ID to copy (e.g., `topic:abc123`) for LLM reference

### MCP Tools (18 tools)

| Category | Tools |
|----------|-------|
| Topics | get_topics, create_topic, update_topic, relate_topics |
| Flashcards | get_flashcards, get_due_flashcards, create_flashcard, create_flashcards_batch, review_flashcard, get_struggling_cards |
| Resources | get_resources, create_resource |
| Artifacts | get_artifacts, create_artifact |
| Doubts | get_doubts, create_doubt, resolve_doubt |
| Sessions | start_session, end_session, get_session_logs |

### Spaced Repetition (SM-2)

The same algorithm behind Anki. Cards you answer correctly get longer intervals; cards you miss reset to 1 day. The ease factor adapts per card — easy cards space out faster, hard cards stay frequent.

See [docs/sm2.md](docs/sm2.md) for the full algorithm with formulas and examples.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OC_HOST` | `0.0.0.0` | Web server host |
| `OC_PORT` | `8080` | Web server port |
| `OC_DATA_DIR` | `~/.open-cognition` | Data directory |
| `SURREAL_URL` | — | SurrealDB connection URL (optional — uses embedded DB if not set) |
| `SURREAL_USER` | `root` | SurrealDB username |
| `SURREAL_PASSWORD` | `root` | SurrealDB password |
| `SURREAL_NAMESPACE` | `open-cognition` | SurrealDB namespace |
| `SURREAL_DATABASE` | `test` | SurrealDB database |

You can set these in a `.env` file or as environment variables.

### External SurrealDB (optional)

By default, open-cognition stores everything in a local file. If you prefer a standalone SurrealDB server (for multi-device access, backups, or production):

```bash
# Via Docker
docker compose up -d

# Or point to your existing instance
export SURREAL_URL=ws://localhost:8000/rpc
```

## CLI

```bash
uvx open-cognition serve [--host HOST] [--port PORT]   # Start the web app
uvx open-cognition mcp                                  # Start the MCP server
uvx open-cognition --version                            # Show version
uvx open-cognition --help                               # Show help
```

## Architecture

```
Claude (LLM) ──► MCP Tools ──┐
                              ├──► Services ──► Repositories ──► SurrealDB
Web UI (HTMX) ──► API Routes ┘
```

MCP tools and API routes share the same services layer. The LLM and the web UI see the same data.

See [docs/architecture.md](docs/architecture.md) for details.

## Development

```bash
git clone https://github.com/lfnovo/open-cognition.git
cd open-cognition
uv sync
open-cognition serve
```

Run tests:
```bash
uv run pytest
```

## Documentation

- [Architecture](docs/architecture.md) — layers, data model, graph relations
- [Concepts](docs/concepts.md) — topics, flashcards, resources, artifacts, sessions, doubts
- [SM-2 Algorithm](docs/sm2.md) — spaced repetition formulas and examples
- [API Reference](docs/api.md) — REST endpoints
- [MCP Tools](docs/mcp-tools.md) — tools for LLM integration

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + FastAPI |
| Database | SurrealDB (embedded file or server) |
| Frontend | HTMX + Jinja2 + Tailwind CSS |
| MCP | FastMCP |
| LLM | Claude (via skill + MCP) |

## License

MIT
