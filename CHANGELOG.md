# Changelog

本文件格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本语义遵循 SemVer。

## [0.1.0] - 2026-11-09

### 新增

- 选装式模板结构：`scaffold/` 菜单（python / go / node / rust）+ `scripts/init.py` 实例化生成器
- 跨语言代码分层双变体可选（ADR-0002）：`--arch cls` 三层式 entry/logic/model/infra（默认）或 `--arch hex` 四层 entry/service/domain/infra；全称 classic / hexagonal 兼容
- 文档机制：`docs/` 分区、总索引强制登记、ADR、同步契约表、`scripts/check_docs.py` 健康检查
- AI 上下文体系：CLAUDE.md / AGENTS.md 薄入口、分语言子树规则合并、`.claude/skills`（new-project / docs-sync / restore-context，三决策前置 + Done when 验收结构）
- 项目版 CLAUDE.md 项目原则：一命令验收（测试 + lint + check_docs，`just check` 聚合）、0.x 早期不兼容自由
- CI：文档检查 + 生成器冒烟测试（实例化各语言并校验占位符与文档链接）
