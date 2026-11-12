# 规范：Python

> status: stable · owner: ZnLuAr · updated: 2026-11-12

参考实现（模板中最完整的语言脚手架）。

## 布局

- 分层二选一（`--arch`，变体语义见 [../reference/layout.md](../reference/layout.md)）：cls `src/__pkg_name__/{entry,logic,model,infra}`（默认）或 hex `{entry,service,domain,infra}`；
- `tests/{unit,integration}` 镜像分层；
- 包名一律下划线小写（`__pkg_name__` 规范化）。

## 工具链

| 动作 | 命令 |
|---|---|
| 安装（包 + 开发依赖） | `pip install -e . --group dev`（pip ≥ 25.1；或 `uv sync`） |
| 测试 | `python -m pytest` |
| lint | `python -m ruff check src tests` |
| 格式化 | `python -m ruff format src tests` |
| 运行 CLI | `<project_name>`（安装后），或 `PYTHONPATH=src python -m __pkg_name__.entry.cli` |

ruff 规则集：`E F I UP B SIM RUF`，行宽 100。

## 代码

- 公开 API（函数签名、类属性）一律类型注解；内部可省；
- `if __name__ == "__main__"` 只出现在 entry；
- 接口用 `typing.Protocol`：hex 定义在 `domain/ports.py`（架构前提，service 只依赖协议）；cls 定义在 `model/`（如 `model/clock.py`，按需引入——logic 直接用 infra 类型，要替身测试或预知换实现时才抽）；
- 异常：规则层（model/domain）抛业务错误（`ValueError` 子类起步即可），entry 负责转成退出码或用户可读信息。

## 禁忌

- 规则层零 IO：model / domain 不 import 其他层，不触网络、时钟、文件系统（时间等外部信息经注入进入；hex 一律经端口，cls 接口按需）；
- infra 实例的构造只在 entry（logic / service 只接收注入）；
- 不用相对导入跨层（`from ..infra import x` 即越层信号）；
- 不绕过 `pyproject.toml` 散装配置（工具配置集中在此）。
