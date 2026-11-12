# 文档总索引

> status: stable · owner: ZnLuAr · updated: 2026-11-12

本文件是 `docs/` 的唯一入口：**每篇文档必须在此登记**，由 `scripts/check_docs.py` 校验（未登记文档、死链、ADR 编号问题都会报错）。

推荐阅读路线：新维护者 → [standards/general.md](standards/general.md) → [architecture/system-map.md](architecture/system-map.md) → [guides/maintain-template.md](guides/maintain-template.md)。

## architecture — 架构与决策

- [contract.md](architecture/contract.md) — 模板的项目契约：目标、不做、所有权、验收
- [system-map.md](architecture/system-map.md) — 系统地图：组件、数据流、维护入口
- [adr/0001-selectable-scaffold-template.md](architecture/adr/0001-selectable-scaffold-template.md) — 选装式模板形态
- [adr/0002-layering-variants.md](architecture/adr/0002-layering-variants.md) — 代码分层双变体可选（cls 三层式 / hex 四层）
- [adr/0003-docs-as-single-source-of-truth.md](architecture/adr/0003-docs-as-single-source-of-truth.md) — docs/ 作为人机共读的单一事实源

## guides — 操作指南（how-to）

- [instantiate.md](guides/instantiate.md) — 实例化一个新项目
- [add-language.md](guides/add-language.md) — 新增一种语言脚手架
- [maintain-template.md](guides/maintain-template.md) — 模板自身的维护流程

## reference — 稳定参考

- [layout.md](reference/layout.md) — 目录与分层约定（仓库平面 + 代码平面双变体 + 占位符）
- [init.md](reference/init.md) — `scripts/init.py` 参数与行为细节

## standards — 规范

- [general.md](standards/general.md) — 通用规范：commit、review 自查、测试、文档同步契约表
- [python.md](standards/python.md) — Python 规范
- [go.md](standards/go.md) — Go 规范
- [typescript.md](standards/typescript.md) — TypeScript / Node 规范
- [rust.md](standards/rust.md) — Rust 规范

## templates — 文档模板

- [adr.md](templates/adr.md) — 新建 ADR 从此开始
- [contract.md](templates/contract.md) — 项目契约模板（实例化后落在 docs/architecture/）
- [design.md](templates/design.md) — 设计文档模板
- [system-map.md](templates/system-map.md) — 系统地图模板
- [context.md](templates/context.md) — 会话恢复摘要模板（对齐全局 ai-work-config）

## context — 会话恢复点

- [context/README.md](context/README.md) — 恢复摘要的用法与命名约定
