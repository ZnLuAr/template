# Python 脚手架 · hexagonal 分层（实例化时合并进项目根 CLAUDE.md 的「语言规则」段）

- 布局：`src/<pkg>/{entry,service,domain,infra}`，`tests/{unit,integration}` 镜像分层。
- 依赖铁律：`entry → service → domain`；infra 只实现 `domain/ports.py` 的端口（查询型如 `Clock`，命令型如 `GreetingLog`）；domain 零 IO、不 import 其他层；组装只在 entry。
- 规范本体：`docs/standards/python.md`（工具链、命名、禁忌）。
- 常用命令：测试 `python -m pytest`；lint `python -m ruff check src tests`；格式化 `python -m ruff format src tests`。
- 公开 API 一律类型注解；新功能与 bug 修复必须带测试。
