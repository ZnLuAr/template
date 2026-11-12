"""Greeter 业务逻辑：编排规则与外部能力，不关心具体实现。"""

from __pkg_name__.model.clock import Clock
from __pkg_name__.model.greeting import greeting_for


class Greeter:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock

    def greet(self, name: str) -> str:
        return greeting_for(self._clock.current_hour(), name)
