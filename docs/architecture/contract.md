# 项目契约：template

> status: accepted · owner: ZnLuAr · updated: 2026-11-12

沿用 ai-work-config `core/workflow.md` §2 的契约形状。

## 目标

- 任何新项目在 10 分钟内从本模板实例化出：分层代码骨架、全套文档机制、AI 上下文入口。
- 分层语义跨语言一致：同一套分层约定在 python / go / node / rust 中同构落地；两种变体（cls 三层式 / hex 四层，见 ADR-0002）在每种语言中同构提供，实例化时可选。
- 文档人机共读：规则本体只写一份，AI 入口（CLAUDE.md / AGENTS.md）只做路由。

## 不做

- 不承载任何业务功能；`scaffold/` 示例代码仅演示分层。
- 不做前端专用模板（已有 `frontend-template-next`）；node 脚手架面向 Node 工具与服务。
- 不支持单项目多语言实例化（组件化 monorepo 留待演进，见 ADR-0001 后果）。
- 不重复全局 ai-work-config 已有的工作流规则。

## 所有权

| 部分 | 归属 |
|---|---|
| 分层语义、占位符约定 | `docs/reference/layout.md` + ADR |
| 语言细节 | `docs/standards/<lang>.md` + `scaffold/<lang>/` |
| 实例化行为 | `scripts/init.py` + `docs/reference/init.md` |
| 文档健康 | `scripts/check_docs.py` + `docs/index.md` |

## 影响面

- 代码：`scaffold/`、`scripts/`
- 文档：全部 `docs/`
- AI 协议：CLAUDE.md、AGENTS.md、`.claude/`
- 实例化产物：新项目的目录结构、初始文档、CLAUDE.md 内容

## 验收

- `python scripts/check_docs.py` 通过；`python -m unittest discover -s scripts/tests` 通过（含四种语言实例化冒烟）。
- 实例化出的项目：测试可运行、无占位符残留、check_docs 通过、CLAUDE.md 有效且无模板专属段落。
