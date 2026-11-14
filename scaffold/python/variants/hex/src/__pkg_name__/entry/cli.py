"""CLI 入口：解析参数、组装依赖、输出结果；不含业务规则。"""

from __future__ import annotations

import argparse

from __pkg_name__.infra.clock import SystemClock
from __pkg_name__.infra.greeting_log import InMemoryGreetingLog
from __pkg_name__.service.greeter import Greeter


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="__project_name__")
    parser.add_argument("name", nargs="?", default="world", help="要问候的名字")
    parser.add_argument(
        "--recent", type=int, default=0, metavar="N", help="问候后同时打印最近 N 条历史"
    )
    args = parser.parse_args(argv)

    greeter = Greeter(SystemClock(), InMemoryGreetingLog())  # 组装只发生在 entry
    greeting = greeter.greet(args.name)
    print(greeting.text)
    for item in greeter.recent(args.recent):
        print(item.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
