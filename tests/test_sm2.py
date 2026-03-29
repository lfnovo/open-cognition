from open_cognition.services.sm2_service import calculate_sm2


def test_first_review_correct():
    result = calculate_sm2(quality=4, repetitions=0, ease_factor=2.5, interval=0)
    assert result.interval == 1
    assert result.repetitions == 1


def test_second_review_correct():
    result = calculate_sm2(quality=4, repetitions=1, ease_factor=2.5, interval=1)
    assert result.interval == 6
    assert result.repetitions == 2


def test_third_review_correct():
    result = calculate_sm2(quality=4, repetitions=2, ease_factor=2.5, interval=6)
    assert result.interval == 15  # round(6 * 2.5)
    assert result.repetitions == 3


def test_incorrect_resets():
    result = calculate_sm2(quality=1, repetitions=5, ease_factor=2.5, interval=30)
    assert result.interval == 1
    assert result.repetitions == 0


def test_ease_factor_minimum():
    result = calculate_sm2(quality=0, repetitions=0, ease_factor=1.3, interval=0)
    assert result.ease_factor == 1.3


def test_perfect_increases_ease():
    result = calculate_sm2(quality=5, repetitions=2, ease_factor=2.5, interval=6)
    assert result.ease_factor == 2.6


def test_quality_3_borderline():
    result = calculate_sm2(quality=3, repetitions=0, ease_factor=2.5, interval=0)
    assert result.interval == 1
    assert result.repetitions == 1
    assert result.ease_factor == 2.36
