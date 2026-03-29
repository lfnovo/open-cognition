from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class SM2Result:
    interval: int
    ease_factor: float
    repetitions: int
    due_date: datetime


def calculate_sm2(
    quality: int,
    repetitions: int,
    ease_factor: float,
    interval: int,
) -> SM2Result:
    """Calculate next review parameters using the SM-2 algorithm."""
    assert 0 <= quality <= 5, f"Quality must be 0-5, got {quality}"

    # Update ease factor
    new_ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, new_ef)

    if quality >= 3:
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 6
        else:
            new_interval = round(interval * new_ef)
        new_repetitions = repetitions + 1
    else:
        new_interval = 1
        new_repetitions = 0

    due_date = datetime.now(timezone.utc) + timedelta(days=new_interval)

    return SM2Result(
        interval=new_interval,
        ease_factor=round(new_ef, 2),
        repetitions=new_repetitions,
        due_date=due_date,
    )
