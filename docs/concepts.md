# Concepts

## Topic

The central node of the knowledge graph. Represents an area of study that the user is building.

**Examples:** "Transformers", "Attention Mechanism", "Backpropagation", "IRR — Internal Rate of Return"

**Characteristics:**
- N:N relationship with itself — a topic can be a subtopic of multiple others
- Granularity is defined by the user
- Topics are never silently created by the LLM — always with approval

**Good topic:** specific enough to have a coherent set of flashcards, but broad enough not to be a single card. "Gradient Descent" is a topic. "Momentum in Gradient Descent" could be a subtopic.

## Flashcard

A practice artifact with a front (question) and back (answer). Associated with at least one topic.

**Formulation rules:**
- One concept per card
- Front as an active question ("Why..." not "What is...")
- Concise back (maximum 3 lines)
- Minimal context on the front to avoid ambiguity

**Spaced repetition fields:**
- `due_date` — when the card should be reviewed
- `interval` — days until the next review
- `ease_factor` — interval growth multiplier (starts at 2.5)
- `repetitions` — how many times it was reviewed successfully consecutively

See [SM-2](sm2.md) for algorithm details.

## Resource

A reference source associated with topics and optionally with specific flashcards.

**Types:** `pdf`, `video`, `link`, `markdown`

**Usage in the system:**
- Consulted during review — when the user gets a card wrong, the associated resources appear as support
- A resource can be associated with multiple topics and multiple cards

**Distinction from artifact:** a paper is a resource. The summary generated from that paper is an artifact.

## Artifact

Structured output generated during a study session. Always in markdown.

**Types:**
- `summary` — summary of a topic or session
- `feynman` — record of a Feynman session (gaps, consolidation)
- `schema` — conceptual schema, map, framework
- `notes` — general notes

**Characteristics:**
- Can contain mermaid diagrams
- Associated with the topic of the session where they were created
- Viewable in a modal with rendered markdown in the UI

## Doubt

A conceptual question the user wants to explore deeper. Can arise during card review or standalone.

**Characteristics:**
- Can be linked to a flashcard (when it arises during review) and/or a topic
- Has status: `open` (pending) or `resolved` (worked through)
- When linked to a card, the topic is inherited automatically
- Open doubts are a natural entry point for study sessions

## Session

An ephemeral study context. Has a scoping topic and takes place in a conversation with the LLM.

**Characteristics:**
- The session itself **is not persisted** — only its outputs (cards, artifacts, resources)
- `start_session` loads the complete topic context for the LLM
- `end_session` persists all outputs in batch
- A session can produce zero outputs — that is valid

## Feynman Session

A structured version of the study session based on the Feynman Technique. Protocol with 4 states:

1. **Calibration** — user explains the concept freely
2. **Gap Probing** — LLM identifies and explores weak points
3. **Consolidation** — user redoes the explanation with the gaps closed
4. **Closing** — synthesis, markdown artifact, flashcards for open gaps

## Review Session

A flow in the web UI where the user reviews pending flashcards:

1. Card appears with the front (question)
2. User tries to recall and clicks "Show answer"
3. Answer appears
4. User rates: Forgot (0) / Wrong (2) / Hard (3) / Ok (4) / Easy (5)
5. SM-2 calculates the next `due_date`
6. If wrong, supporting resources appear
7. Topic artifacts are accessible in the sidebar

## Knowledge Graph

The topic structure forms a directed graph (not necessarily a tree — a topic can have multiple parents). The relations are:

```
Investment Evaluation
├── IRR
├── NPV
├── MAR
└── Time Value of Money

Python
└── Decorators
```

The graph belongs to the user — the LLM proposes, but the human approves every reorganization.
