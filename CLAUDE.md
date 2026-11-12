# CLAUDE.md — 选装式项目模板

本仓库是**选装式项目模板**：只维护模板、脚手架和生成器，不开发业务功能。`scaffold/` 里的示例代码只为演示分层语义（同一 Greeter 示例在四种语言 × 两种分层变体中同构落地）。

## 硬边界

- 不在本仓库直接开发业务项目；新项目一律用 `scripts/init.py` 实例化（见 `docs/guides/instantiate.md`）。
- 任何改动交付前必须通过：
  - `python scripts/check_docs.py`
  - `python -m unittest discover -s scripts/tests`
- 新增 `docs/` 文档必须登记进 `docs/index.md`，否则 check_docs 失败。
- 未经用户明确要求不 commit。

## 模板仓库专用规则

- 改 `scaffold/` 或 `scripts/` 后，必须跑生成器冒烟测试（`scripts/tests/` 会实例化各语言并校验占位符与文档链接）。
- 改目录或分层约定 → 同步 `docs/reference/layout.md` 与相关 ADR。
- 新增语言脚手架 → 按 `docs/guides/add-language.md` 清单执行。
- 模板自身的维护流程见 `docs/guides/maintain-template.md`。

## 任务路由

| 要做的事 | 先读 |
|---|---|
| 实例化新项目 | `docs/guides/instantiate.md`、`docs/reference/init.md` |
| 新增语言脚手架 | `docs/guides/add-language.md` |
| 改目录 / 分层约定 | `docs/reference/layout.md`、`docs/architecture/adr/` |
| 写或改文档 | `docs/index.md`、`docs/standards/general.md`（含同步契约表） |
| 维护模板自身 | `docs/guides/maintain-template.md` |
| 恢复上次会话 | `docs/context/` 最新恢复摘要 |

## 事实源声明

本文件与 AGENTS.md 只做路由；规则本体在 `docs/`，人与 AI 共读同一份。全局工作方式（L0 层）由用户 ai-work-config 提供，本仓库不重复。
