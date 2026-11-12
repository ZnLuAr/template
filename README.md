# 选装式项目模板

> status: stable · owner: ZnLuAr · updated: 2026-11-12

选装式项目模板：为工作目录下的每个新项目提供统一的分层结构、文档机制和 AI 上下文体系。本仓库自身**不开发业务**，只维护模板、脚手架和生成器。

## 它解决什么

| 要求 | 机制 | 入口 |
|---|---|---|
| 明确且合理的分层 | 仓库平面 + 代码平面双变体（cls 三层式 / hex 四层，实例化时 `--arch` 可选） | [docs/reference/layout.md](docs/reference/layout.md) |
| 支持多种语言 | `scaffold/` 语言脚手架菜单 + `scripts/init.py` 实例化生成器 | [docs/guides/instantiate.md](docs/guides/instantiate.md) |
| 完善的文档机制 | `docs/` 分区 + 总索引强制登记 + ADR + 同步契约表 + 检查脚本 | [docs/index.md](docs/index.md) |
| 供 AI 阅读的提示词体系 | CLAUDE.md / AGENTS.md 薄入口 + 分层按需加载 + skills | [CLAUDE.md](CLAUDE.md) |

## 快速开始

需要 Python 3.11+（仅用于运行生成器）：

```bash
python scripts/init.py --name my-project --lang python --target ../my-project   # --arch 默认 cls
cd ../my-project && python -m pytest
```

分层变体（[ADR-0002](docs/architecture/adr/0002-layering-variants.md)）：`cls` = classic 三层式（默认）；`hex` = hexagonal 四层（业务复杂、依赖需长期可替换时选它）。

支持语言：`python` · `go` · `node`（TypeScript）· `rust`。新增语言见 [docs/guides/add-language.md](docs/guides/add-language.md)。

## 目录总览

```
template/
├── README.md / CHANGELOG.md     # 本说明 / 变更记录
├── CLAUDE.md / AGENTS.md        # AI 入口（薄路由，事实源在 docs/）
├── .claude/                     # skills（实例化、文档同步、上下文恢复）+ 权限
├── docs/                        # 文档机制：索引、架构、指南、参考、规范、模板、恢复点
├── scaffold/                    # 各语言脚手架种子（python / go / node / rust，各含 cls / hex 分层变体）
├── scripts/                     # init.py 生成器、check_docs.py 检查、生成器测试
└── .github/                     # CI（文档检查 + 生成器冒烟）、PR 模板
```

## 设计决策

- [ADR-0001](docs/architecture/adr/0001-selectable-scaffold-template.md)：选装式独立项目形态（与工作目录下现有兄弟仓库一致）
- [ADR-0002](docs/architecture/adr/0002-layering-variants.md)：代码分层双变体可选（cls 三层式 / hex 四层）
- [ADR-0003](docs/architecture/adr/0003-docs-as-single-source-of-truth.md)：docs/ 是人机共读的单一事实源，AI 入口只做路由

## 与全局配置的关系

跨项目的工作方式由用户的 `ai-work-config`（L0 全局层）提供；本模板只提供 L1 仓库层与 L2 子树层的项目侧内容，不重复全局规则。

## 状态

v0.1.0（见 [CHANGELOG.md](CHANGELOG.md)）。License 待定。
