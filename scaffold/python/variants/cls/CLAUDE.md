# Python 脚手架 · classic 分层（实例化时合并进项目根 CLAUDE.md 的「语言规则」段）

- 布局：`src/<pkg>/{entry,logic,model,infra}`，`tests/{unit,integration}` 镜像分层。
- 铁律：model 零 IO、不 import 任何层。惯例：组装只在 entry；logic 默认直接用 infra 类型，要替身测试或换实现时抽 model 接口（渐进条款见 `docs/reference/layout.md`）。
- 规范本体：`docs/standards/python.md`（工具链、命名、禁忌）。
- 常用命令：测试 `python -m pytest`；lint `python -m ruff check src tests`；格式化 `python -m ruff format src tests`。
- 公开 API 一律类型注解；新功能与 bug 修复必须带测试。
