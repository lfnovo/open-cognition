# Spaced Repetition — SM-2 Algorithm

open-cognition uses the SM-2 (SuperMemo 2) algorithm to calculate when each flashcard should be reviewed. It is the same algorithm as the original Anki.

## Principle

The core idea is simple: review a card **at the moment you are about to forget it**. Each successful review increases the interval until the next one. If you get it wrong, the interval resets.

## Parameters

Each flashcard maintains 4 parameters:

| Parameter | Initial Value | Description |
|-----------|---------------|-------------|
| `interval` | 0 | Days until the next review |
| `ease_factor` | 2.5 | Interval growth multiplier |
| `repetitions` | 0 | Consecutive successful reviews |
| `due_date` | now | Next review date |

## Quality Scale

After each review, the user rates the quality of their response on a scale from 0 to 5:

| Score | Label | Meaning |
|-------|-------|---------|
| 0 | Forgot | Total blackout |
| 1 | — | Wrong, but remembered upon seeing the answer |
| 2 | Wrong | Wrong, but the answer seemed familiar |
| 3 | Hard | Correct, with significant difficulty |
| 4 | Ok | Correct, with some hesitation |
| 5 | Easy | Immediate and confident answer |

In the UI, we expose 5 buttons: Forgot (0), Wrong (2), Hard (3), Ok (4), Easy (5).

## Algorithm

### 1. Update Ease Factor

Executed **always**, regardless of correct or incorrect answer:

```
new_EF = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
```

Where `q` is the quality score (0-5).

The EF never drops below **1.3**.

**Examples of EF variation:**

| Score | Variation | EF (starting from 2.5) |
|-------|-----------|------------------------|
| 5 | +0.10 | 2.60 |
| 4 | +0.00 | 2.50 |
| 3 | -0.14 | 2.36 |
| 2 | -0.32 | 2.18 |
| 1 | -0.54 | 1.96 |
| 0 | -0.80 | 1.70 |

### 2. Calculate New Interval

**If correct (score >= 3):**

```
if repetitions == 0: interval = 1 day
if repetitions == 1: interval = 6 days
if repetitions >= 2: interval = previous_interval * new_EF (rounded)
```

`repetitions` increments by 1.

**If incorrect (score < 3):**

```
interval = 1 day
repetitions = 0  (full reset)
```

The card returns to the beginning of the learning curve.

### 3. Calculate Due Date

```
due_date = now + interval days
```

## Full Example

New card, reviewed daily with quality 4 (Ok):

| Review | Score | Reps | EF | Interval | Next |
|--------|-------|------|----|----------|------|
| 1st | 4 | 0→1 | 2.50 | 1d | tomorrow |
| 2nd | 4 | 1→2 | 2.50 | 6d | +6 days |
| 3rd | 4 | 2→3 | 2.50 | 15d | +15 days |
| 4th | 4 | 3→4 | 2.50 | 38d | +38 days |
| 5th | 4 | 4→5 | 2.50 | 95d | +95 days |

If the user got it wrong on the 3rd review (score 2):

| Review | Score | Reps | EF | Interval | Next |
|--------|-------|------|----|----------|------|
| 3rd | 2 | →0 | 2.18 | 1d | tomorrow |
| 4th | 4 | 0→1 | 2.18 | 1d | tomorrow |
| 5th | 4 | 1→2 | 2.18 | 6d | +6 days |
| 6th | 4 | 2→3 | 2.18 | 13d | +13 days |

Note that the lower EF (2.18 vs 2.50) makes the intervals grow more slowly — the system learned that this card is harder.

## Ease Factor Effect

The EF is what makes the system adaptive per card:

- **High EF (2.6+)**: easy card → intervals grow fast → rare review
- **Medium EF (2.5)**: normal card → standard growth
- **Low EF (1.3-2.0)**: hard card → intervals grow slowly → frequent review

The minimum EF of 1.3 ensures that intervals eventually grow even for the hardest cards, but cards consistently answered incorrectly (quality < 3) will keep resetting to 1 day.

## Implementation

The algorithm is in `src/open_cognition/services/sm2_service.py`:

```python
from datetime import datetime, timedelta, timezone

def calculate_sm2(quality, repetitions, ease_factor, interval) -> SM2Result:
    # Update ease factor
    new_ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, new_ef)

    if quality >= 3:  # Correct
        if repetitions == 0: new_interval = 1
        elif repetitions == 1: new_interval = 6
        else: new_interval = round(interval * new_ef)
        new_repetitions = repetitions + 1
    else:  # Incorrect
        new_interval = 1
        new_repetitions = 0

    due_date = datetime.now(timezone.utc) + timedelta(days=new_interval)
    return SM2Result(new_interval, new_ef, new_repetitions, due_date)
```

## References

- [SuperMemo 2 Algorithm](https://super-memory.com/english/ol/sm2.htm) — original description by Piotr Wozniak
- [Anki Manual — Scheduling](https://docs.ankiweb.net/studying.html) — similar implementation in Anki
