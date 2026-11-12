"""CLI 入口：解析参数、组装依赖、输出结果；不含业务规则。"""

from __future__ import annotations

import argparse

from __pkg_name__.infra.clock import SystemClock
from __pkg_name__.service.greeter import Greeter


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="__project_name__")
    parser.add_argument("name", nargs="?", default="world", help="要问候的名字")
    args = parser.parse_args(argv)

    greeter = Greeter(SystemClock())  # 组装只发生在 entry：infra 注入 service
    print(greeter.greet(args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
