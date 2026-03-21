# MCP Tools

O open-cognition expõe 13 tools via MCP para integração com LLMs compatíveis (Claude Desktop, Claude Code, etc.).

## Como usar

### Claude Desktop

Adicione ao `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "open-cognition": {
      "command": "/caminho/para/uv",
      "args": ["run", "--directory", "/caminho/para/open-cognition", "python", "run_mcp.py"],
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

Adicione `.mcp.json` na raiz do projeto onde vai usar:

```json
{
  "mcpServers": {
    "open-cognition": {
      "command": "uv",
      "args": ["run", "--directory", "/caminho/para/open-cognition", "python", "run_mcp.py"],
      "env": { ... }
    }
  }
}
```

## Tools Disponíveis

### Tópicos

| Tool | Descrição |
|------|-----------|
| `get_topics()` | Lista todos os tópicos com hierarquia de subtópicos |
| `create_topic(name, description?, parent_ids?)` | Cria tópico, opcionalmente como subtópico |
| `update_topic(topic_id, name?, description?)` | Atualiza nome ou descrição |
| `relate_topics(parent_id, child_id)` | Cria relação pai/filho entre tópicos |

### Flashcards

| Tool | Descrição |
|------|-----------|
| `get_flashcards(topic_id?)` | Lista flashcards, filtro opcional por tópico |
| `get_due_flashcards(topic_id?)` | Lista flashcards pendentes de revisão (due_date <= agora) |
| `create_flashcard(front, back, topic_ids, resource_ids?)` | Cria um flashcard |
| `create_flashcards_batch(cards)` | Cria múltiplos flashcards de uma vez |
| `review_flashcard(flashcard_id, quality)` | Registra revisão e atualiza SM-2. Quality: 0/2/3/4/5 |

`cards` é uma lista de objetos `{front, back, topic_ids, resource_ids?}`.

### Recursos

| Tool | Descrição |
|------|-----------|
| `get_resources(topic_id?)` | Lista recursos, filtro opcional por tópico |
| `create_resource(type, title, content_or_url, topic_ids)` | Cria recurso |

Tipos: `pdf`, `video`, `link`, `markdown`.

### Artefatos

| Tool | Descrição |
|------|-----------|
| `get_artifacts(topic_id?)` | Lista artefatos, filtro opcional por tópico |
| `create_artifact(type, title, content, topic_ids)` | Cria artefato em markdown |

Tipos: `summary`, `feynman`, `schema`, `notes`.

### Sessão de Estudo

| Tool | Descrição |
|------|-----------|
| `start_session(topic_id)` | Inicia sessão. Retorna contexto completo: cards, recursos, artefatos |
| `end_session(topic_id, session_type, summary?, outputs?)` | Encerra sessão, persiste outputs e registra log |
| `get_session_logs(topic_id?)` | Consulta histórico de sessões |

**Parâmetros de `end_session`:**
- `topic_id` — tópico estudado
- `session_type` — `study`, `feynman`, `review`, `import`
- `summary` — resumo breve do que foi coberto (opcional)
- `outputs` — outputs a persistir (opcional):
```json
{
  "flashcards": [{"front": "...", "back": "...", "topic_ids": [...]}],
  "resources": [{"type": "link", "title": "...", "content_or_url": "...", "topic_ids": [...]}],
  "artifacts": [{"type": "summary", "title": "...", "content": "...", "topic_ids": [...]}]
}
```

## Formato de Retorno

Todas as tools retornam **strings legíveis** (não JSON), pois são consumidas por LLMs. A API REST retorna JSON estruturado para consumo programático.
