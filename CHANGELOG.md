# Changelog

本文件格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本语义遵循 SemVer。

## [Unreleased]

### 新增

- CI 脚手架实编 matrix（四语言 × 两变体，真实工具链格式 / lint / 测试 / CLI 冒烟，`scripts/check_scaffold.py` 本机同款入口）；实例化项目自带与语言规范命令对齐的 `.github/workflows/ci.yml`（check_docs + 格式检查 + lint + 测试）
- hex 示例升级：双类型端口（Clock 查询 / GreetingLog 命令）与状态、greet / recent 两个 use case，演示完整依赖倒置；ADR-0002 同构条款改为「刻意不对称」

### 修复

- rust 两变体缺层模块 `pub use` 再导出导致 main / tests 短路径解析失败的存量编译断裂（初始提交即存在，结构性门禁不编译代码故未暴露）；约定写入 rust.md，冒烟测试钉住
- init.py 实例化语义：scaffold 与根资产同名目录合并（`.github/`），同名文件报错拒绝静默覆盖

## [0.1.0] - 2026-11-09

### 新增

- 选装式模板结构：`scaffold/` 菜单（python / go / node / rust）+ `scripts/init.py` 实例化生成器
- 跨语言代码分层双变体可选（ADR-0002）：`--arch cls` 三层式 entry/logic/model/infra（默认）或 `--arch hex` 四层 entry/service/domain/infra；全称 classic / hexagonal 兼容
- 文档机制：`docs/` 分区、总索引强制登记、ADR、同步契约表、`scripts/check_docs.py` 健康检查
- AI 上下文体系：CLAUDE.md / AGENTS.md 薄入口、分语言子树规则合并、`.claude/skills`（new-project / docs-sync / restore-context，三决策前置 + Done when 验收结构）
- 项目版 CLAUDE.md 项目原则：一命令验收（测试 + lint + check_docs，`just check` 聚合）、0.x 早期不兼容自由
- CI：文档检查 + 生成器冒烟测试（实例化各语言并校验占位符与文档链接）
