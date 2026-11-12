# 规范：通用（跨语言）

> status: stable · owner: ZnLuAr · updated: 2026-11-12

语言细节见各语言规范：`python.md` / `go.md` / `typescript.md` / `rust.md`（模板含四篇，实例化项目仅保留所用语言）；分层与目录见 [../reference/layout.md](../reference/layout.md)。

## Commit

- 遵循 Conventional Commits（`feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:` / `build:` / `ci:`），subject 可用中文；
- 一个 commit 一个意图；生成产物不与手写改动混排；
- 未经明确要求不 commit、不推送。

## 测试

- 新功能与 bug 修复必须带测试：unit 覆盖规则与业务层（cls：model/logic，hex：domain/service，用 fake 替身），integration 覆盖 entry/infra；
- 修复 bug 先写复现用例再修；
- 交付时如实报告跑过的命令与结果，零匹配不等于通过。

## Review 自查（交付 / PR 前）

- [ ] 测试已运行并通过（列出命令）
- [ ] 对照下方同步契约表，该更新的文档已更新
- [ ] 新增文档已登记 `docs/index.md`，`check_docs.py` 通过
- [ ] 分层合规：按本项目变体（cls：model 零 IO；hex：`entry → service → domain`、`infra → domain`，见 `docs/reference/layout.md`）
- [ ] 模板仓库内无占位符残留、无业务代码混入
- [ ] 规则没有「顺手」抄进 CLAUDE.md 正文（本体只在 docs/，见 ADR-0003）

## 文档同步契约表

| 改动 | 必须同步 |
|---|---|
| 分层 / 依赖方向 | `docs/reference/layout.md`、`system-map.md`、相关 ADR |
| 公开接口（API / CLI / 配置项） | `docs/reference/` 对应篇 + `CHANGELOG.md` |
| 目录 / 工具链命令 | `docs/standards/<lang>.md` + 对应 scaffold README |
| 实例化行为 | `docs/reference/init.md` + `system-map.md` 数据流 |
| 重要取舍 | 新 ADR（从 `docs/templates/adr.md` 起） |
| 面向使用者可见变化 | `CHANGELOG.md` |

## 行文约定

- 文档用中文；代码、路径、术语保留原文；
- 每篇文档标题下保持 `> status: … · owner: … · updated: YYYY-MM-DD` 头部行；
- 文档中的结论区分事实 / 推断 / 待验证；系统地图注明最近核实日期。
