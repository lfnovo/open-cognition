# Conceitos

## Tópico

O nó central do grafo de conhecimento. Representa uma área de estudo que o usuário está construindo.

**Exemplos:** "Transformers", "Attention Mechanism", "Backpropagation", "TIR — Taxa Interna de Retorno"

**Características:**
- Relação N:N consigo mesmo — um tópico pode ser subtópico de vários outros
- A granularidade é definida pelo usuário
- Tópicos nunca são criados silenciosamente pelo LLM — sempre com aprovação

**Bom tópico:** específico o suficiente para ter um conjunto coerente de flashcards, mas amplo o suficiente para não ser um único card. "Gradient Descent" é um tópico. "Momentum em Gradient Descent" pode ser um subtópico.

## Flashcard

Artefato de prática com frente (pergunta) e verso (resposta). Associado a pelo menos um tópico.

**Regras de formulação:**
- Um conceito por card
- Frente como pergunta ativa ("Por que..." não "O que é...")
- Verso conciso (máximo 3 linhas)
- Contexto mínimo na frente para evitar ambiguidade

**Campos de spaced repetition:**
- `due_date` — quando o card deve ser revisado
- `interval` — dias até a próxima revisão
- `ease_factor` — multiplicador de crescimento do intervalo (inicia em 2.5)
- `repetitions` — quantas vezes foi revisado com sucesso consecutivamente

Ver [SM-2](sm2.md) para detalhes do algoritmo.

## Recurso

Fonte de referência associada a tópicos e opcionalmente a flashcards específicos.

**Tipos:** `pdf`, `video`, `link`, `markdown`

**Uso no sistema:**
- Consultados durante revisão — quando o usuário erra um card, os recursos associados aparecem como apoio
- Um recurso pode ser associado a múltiplos tópicos e múltiplos cards

**Distinção de artefato:** um paper é um recurso. O resumo gerado a partir desse paper é um artefato.

## Artefato

Output estruturado gerado numa sessão de estudo. Sempre em markdown.

**Tipos:**
- `summary` — resumo de um tópico ou sessão
- `feynman` — registro de uma sessão Feynman (gaps, consolidação)
- `schema` — esquema conceitual, mapa, framework
- `notes` — notas gerais

**Características:**
- Podem conter diagramas mermaid
- Associados ao tópico da sessão onde foram criados
- Visualizáveis em modal com markdown renderizado na UI

## Sessão

Contexto efêmero de estudo. Tem um tópico de escopo e acontece numa conversa com o LLM.

**Características:**
- A sessão em si **não é persistida** — só seus outputs (cards, artefatos, recursos)
- `start_session` carrega o contexto completo do tópico para o LLM
- `end_session` persiste todos os outputs em batch
- Uma sessão pode produzir zero outputs — isso é válido

## Sessão Feynman

Versão estruturada da sessão de estudo baseada na Técnica Feynman. Protocolo em 4 estados:

1. **Calibração** — usuário explica o conceito livremente
2. **Sondagem de Gaps** — LLM identifica e explora pontos fracos
3. **Consolidação** — usuário refaz a explicação com os gaps fechados
4. **Encerramento** — síntese, artefato markdown, flashcards para gaps em aberto

## Sessão de Revisão

Fluxo na UI web onde o usuário revisa flashcards pendentes:

1. Card aparece com a frente (pergunta)
2. Usuário tenta lembrar e clica "Mostrar resposta"
3. Resposta aparece
4. Usuário avalia: Esqueci (0) / Errei (2) / Difícil (3) / Ok (4) / Fácil (5)
5. SM-2 calcula o próximo `due_date`
6. Se errou, recursos de apoio aparecem
7. Artefatos do tópico ficam acessíveis na sidebar

## Grafo de Conhecimento

A estrutura de tópicos forma um grafo direcionado (não necessariamente uma árvore — um tópico pode ter múltiplos pais). As relações são:

```
Avaliação de Investimentos
├── TIR
├── VPL
├── TMA
└── Valor do Dinheiro no Tempo

Python
└── Decorators
```

O grafo é do usuário — o LLM propõe, mas o humano aprova toda reorganização.
