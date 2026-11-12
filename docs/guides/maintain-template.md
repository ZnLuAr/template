# 指南：模板自身的维护

> status: stable · owner: ZnLuAr · updated: 2026-11-09

## 改动类型 → 必跑验证

| 改了什么 | 必跑 |
|---|---|
| 任何文件 | `python scripts/check_docs.py` |
| `scaffold/`、`scripts/` | 加上 `python -m unittest discover -s scripts/tests`（冒烟会真实实例化四种语言） |
| `docs/index.md` 结构 | `python scripts/check_docs.py`（死链与未登记都会被抓） |
| 分层 / 占位符约定 | 同步 `docs/reference/layout.md` + 相关 ADR + 各 scaffold 注释 |

## 同步契约（模板版）

| 改动 | 必须同步 |
|---|---|
| 加 / 删语言 scaffold | `docs/guides/add-language.md` 语义不变，但 README 语言列表、index、init.py 映射、冒烟用例、standards 五处联动 |
| 改实例化行为（init.py） | `docs/reference/init.md` + `docs/architecture/system-map.md` 数据流 |
| 改项目版 CLAUDE.md 骨架（`PROJECT_CLAUDE_TEMPLATE`） | `docs/reference/init.md` 行为描述 + `scripts/tests/` 冒烟断言 |
| 改文档机制规则（check_docs.py） | `docs/standards/general.md` 的文档规则节 |
| 任何面向使用者的变化 | `CHANGELOG.md` + 各 scaffold README 若受影响 |

## 原则

- 模板仓库不产生「临时试验文件」；试验一律实例化到外面的项目里做；
- 无法确定某改动是否破坏实例化时，以冒烟测试结果为准，不靠推断；
- 经验线索（踩坑、反复）按用户全局 `experience-protocol` 留原始记录，不直接升级成本仓库规则。
