"""service.Greeter 的单元测试：fake Clock / GreetingLog 替身，service 全程无真实 IO。"""

from __pkg_name__.domain.greeting import Greeting
from __pkg_name__.service.greeter import Greeter


class FakeClock:
    def __init__(self, hour: int) -> None:
        self._hour = hour

    def current_hour(self) -> int:
        return self._hour


class FakeLog:
    def __init__(self) -> None:
        self.saved: list[Greeting] = []

    def save(self, greeting: Greeting) -> None:
        self.saved.append(greeting)

    def recent(self, limit: int) -> list[Greeting]:
        return list(reversed(self.saved[-limit:])) if limit > 0 else []


def test_greet_applies_rule_and_records_history() -> None:
    log = FakeLog()
    greeting = Greeter(FakeClock(9), log).greet("Ada")

    assert greeting.text == "Good morning, Ada."
    assert log.saved == [greeting]  # 编排可见：规则被应用，副作用被记录


def test_recent_reads_through_log_port() -> None:
    greeter = Greeter(FakeClock(9), FakeLog())
    greeter.greet("Ada")
    greeter.greet("Grace")

    assert [g.name for g in greeter.recent(1)] == ["Grace"]
