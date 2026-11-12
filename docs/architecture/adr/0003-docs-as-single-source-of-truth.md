# ADR-0003：docs/ 是人机共读的单一事实源，AI 入口只做路由

> status: accepted · date: 2026-11-09 · owner: ZnLuAr

## 背景

面向 AI 的项目说明存在多入口现实：CLAUDE.md（Claude Code）、AGENTS.md（其他代理工具）、CONTRIBUTING（人类）。若各自维护内容，必然漂移。同时用户已确认 AI 体系兼容范围：Claude Code + AGENTS.md。

## 决策

- **规则本体只在 `docs/` 写一份**（standards / reference / architecture），人与 AI 读同一份；
- CLAUDE.md 与 AGENTS.md 是**薄路由**：使命、硬边界、任务路由表（「要做 X → 先读 Y」），总长控制在百行内；AGENTS.md 仅指向 CLAUDE.md 与 docs/index.md；
- 可复用流程落在 `.claude/skills/`（new-project、docs-sync、restore-context），不塞进 CLAUDE.md 正文；
- 实例化时生成器用内嵌的项目骨架（硬边界 + 项目任务路由 + 事实源声明）拼装项目 CLAUDE.md，语言规则段来自 `scaffold/<lang>/CLAUDE.md`，其规范本体只在 `docs/standards/<lang>.md` 维护。

加载层级与 ai-work-config 的关系：

| 层 | 载体 | 内容 |
|---|---|---|
| L0 全局 | 用户 ai-work-config + `~/.claude/CLAUDE.md` | 跨项目工作方式（模板不重复） |
| L1 仓库根 | 项目 CLAUDE.md / AGENTS.md | 使命、硬边界、任务路由 |
| L2 语言段 | CLAUDE.md 语言段 → `standards/<lang>.md` | 语言布局、命令、禁忌 |
| L3 流程 | `.claude/skills/` | 任务剧本 |

## 后果

**正面**

- 永远不存在「CLAUDE.md 和 CONTRIBUTING 说法不一致」；文档修一处即全端生效；
- AI 上下文按需加载，根入口不随项目规模膨胀。

**负面与代价**

- 写规则时必须克制「顺手在 CLAUDE.md 里再写一遍」的冲动——review 自查清单已列入此项；
- AGENTS.md 兼容是薄指针，依赖工具愿意跟随链接读文件（主流代理均可）。
