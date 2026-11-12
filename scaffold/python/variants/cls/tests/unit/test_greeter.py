"""logic.Greeter 的单元测试：fake Clock 替身，不触真实时间。"""

from __pkg_name__.logic.greeter import Greeter


class FakeClock:
    def __init__(self, hour: int) -> None:
        self._hour = hour

    def current_hour(self) -> int:
        return self._hour


def test_greet_morning() -> None:
    assert Greeter(FakeClock(9)).greet("Ada") == "Good morning, Ada."


def test_greet_evening() -> None:
    assert Greeter(FakeClock(21)).greet("Ada") == "Good evening, Ada."
