# __project_name__

> TODO: 一句话描述 __project_name__。

由项目模板实例化（hexagonal 分层：entry / service / domain / infra）。分层约定见 `docs/reference/layout.md`，AI 入口见 `CLAUDE.md`。

## 快速开始

```bash
pip install -e . --group dev   # 包 + 开发依赖（pytest/ruff）；uv 用 uv sync
python -m pytest               # 测试
python -m ruff check src tests

__project_name__ world    # 运行 CLI（安装后）
```

## 布局

```
src/__pkg_name__/
├── entry/     # 入口与 adapter（CLI）
├── service/   # use case 编排
├── domain/    # 纯领域规则 + 端口定义（零 IO）
└── infra/     # 端口实现（时钟、存储、外部系统）
tests/
├── unit/          # domain、service（fake 替身）
└── integration/   # entry、infra
```
