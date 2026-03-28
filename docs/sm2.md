# Spaced Repetition — Algoritmo SM-2

O open-cognition usa o algoritmo SM-2 (SuperMemo 2) para calcular quando cada flashcard deve ser revisado. É o mesmo algoritmo do Anki original.

## Princípio

A ideia central é simples: revise um card **no momento em que você está prestes a esquecê-lo**. Cada revisão bem-sucedida aumenta o intervalo até a próxima. Se você erra, o intervalo reseta.

## Parâmetros

Cada flashcard mantém 4 parâmetros:

| Parâmetro | Valor Inicial | Descrição |
|-----------|---------------|-----------|
| `interval` | 0 | Dias até a próxima revisão |
| `ease_factor` | 2.5 | Multiplicador de crescimento do intervalo |
| `repetitions` | 0 | Revisões consecutivas bem-sucedidas |
| `due_date` | agora | Próxima data de revisão |

## Escala de Qualidade

Após cada revisão, o usuário avalia a qualidade da resposta numa escala de 0 a 5:

| Nota | Label | Significado |
|------|-------|-------------|
| 0 | Esqueci | Blackout total |
| 1 | — | Errado, mas lembrou ao ver a resposta |
| 2 | Errei | Errado, mas a resposta parecia familiar |
| 3 | Difícil | Correto, com dificuldade significativa |
| 4 | Ok | Correto, com alguma hesitação |
| 5 | Fácil | Resposta imediata e confiante |

Na UI, expomos 5 botões: Esqueci (0), Errei (2), Difícil (3), Ok (4), Fácil (5).

## Algoritmo

### 1. Atualizar Ease Factor

Executado **sempre**, independente de acerto ou erro:

```
novo_EF = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
```

Onde `q` é a nota de qualidade (0-5).

O EF nunca desce abaixo de **1.3**.

**Exemplos de variação do EF:**

| Nota | Variação | EF (partindo de 2.5) |
|------|----------|---------------------|
| 5 | +0.10 | 2.60 |
| 4 | +0.00 | 2.50 |
| 3 | -0.14 | 2.36 |
| 2 | -0.32 | 2.18 |
| 1 | -0.54 | 1.96 |
| 0 | -0.80 | 1.70 |

### 2. Calcular Novo Intervalo

**Se acertou (nota >= 3):**

```
se repetitions == 0: intervalo = 1 dia
se repetitions == 1: intervalo = 6 dias
se repetitions >= 2: intervalo = intervalo_anterior * novo_EF (arredondado)
```

`repetitions` incrementa em 1.

**Se errou (nota < 3):**

```
intervalo = 1 dia
repetitions = 0  (reset total)
```

O card volta ao início da curva de aprendizagem.

### 3. Calcular Due Date

```
due_date = agora + intervalo dias
```

## Exemplo Completo

Card novo, revisado diariamente com qualidade 4 (Ok):

| Revisão | Nota | Reps | EF | Intervalo | Próxima |
|---------|------|------|----|-----------|---------|
| 1a | 4 | 0→1 | 2.50 | 1d | amanhã |
| 2a | 4 | 1→2 | 2.50 | 6d | +6 dias |
| 3a | 4 | 2→3 | 2.50 | 15d | +15 dias |
| 4a | 4 | 3→4 | 2.50 | 38d | +38 dias |
| 5a | 4 | 4→5 | 2.50 | 95d | +95 dias |

Se na 3a revisão o usuário errasse (nota 2):

| Revisão | Nota | Reps | EF | Intervalo | Próxima |
|---------|------|------|----|-----------|---------|
| 3a | 2 | →0 | 2.18 | 1d | amanhã |
| 4a | 4 | 0→1 | 2.18 | 1d | amanhã |
| 5a | 4 | 1→2 | 2.18 | 6d | +6 dias |
| 6a | 4 | 2→3 | 2.18 | 13d | +13 dias |

Note que o EF mais baixo (2.18 vs 2.50) faz os intervalos crescerem mais devagar — o sistema aprendeu que esse card é mais difícil.

## Efeito do Ease Factor

O EF é o que torna o sistema adaptativo por card:

- **EF alto (2.6+)**: card fácil → intervalos crescem rápido → revisão rara
- **EF médio (2.5)**: card normal → crescimento padrão
- **EF baixo (1.3-2.0)**: card difícil → intervalos crescem devagar → revisão frequente

O EF mínimo de 1.3 garante que os intervalos eventualmente crescem mesmo para os cards mais difíceis, porém cards consistentemente respondidos de forma incorreta (quality < 3) continuarão resetando para 1 dia.

## Implementação

O algoritmo está em `src/open_cognition/services/sm2_service.py`:

```python
from datetime import datetime, timedelta, timezone

def calculate_sm2(quality, repetitions, ease_factor, interval) -> SM2Result:
    # Atualiza ease factor
    new_ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, new_ef)

    if quality >= 3:  # Acertou
        if repetitions == 0: new_interval = 1
        elif repetitions == 1: new_interval = 6
        else: new_interval = round(interval * new_ef)
        new_repetitions = repetitions + 1
    else:  # Errou
        new_interval = 1
        new_repetitions = 0

    due_date = datetime.now(timezone.utc) + timedelta(days=new_interval)
    return SM2Result(new_interval, new_ef, new_repetitions, due_date)
```

## Referências

- [SuperMemo 2 Algorithm](https://super-memory.com/english/ol/sm2.htm) — descrição original por Piotr Wozniak
- [Anki Manual — Scheduling](https://docs.ankiweb.net/studying.html) — implementação similar no Anki
