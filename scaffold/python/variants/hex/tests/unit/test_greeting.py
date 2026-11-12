"""domain.greeting 的表驱动测试。"""

import pytest

from __pkg_name__.domain.greeting import greeting_for


@pytest.mark.parametrize(
    ("hour", "expected_part"),
    [
        (0, "Good night"),
        (4, "Good night"),
        (5, "Good morning"),
        (11, "Good morning"),
        (12, "Good afternoon"),
        (17, "Good afternoon"),
        (18, "Good evening"),
        (22, "Good evening"),
        (23, "Good night"),
    ],
)
def test_greeting_for_matches_expected_part(hour: int, expected_part: str) -> None:
    assert greeting_for(hour, "Ada") == f"{expected_part}, Ada."


@pytest.mark.parametrize("hour", [-1, 24, 99])
def test_greeting_for_rejects_invalid_hour(hour: int) -> None:
    with pytest.raises(ValueError, match="hour"):
        greeting_for(hour, "Ada")
