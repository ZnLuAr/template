# 参考：scripts/init.py

> status: stable · owner: ZnLuAr · updated: 2026-11-12

## 用法

```bash
python scripts/init.py --name <name> --lang <lang> [--arch cls|hex] [--target <path>] [--module-path <path>] [--git]
```

| 参数 | 必填 | 说明 |
|---|---|---|
| `--name` | 是 | 项目名，`^[a-zA-Z][a-zA-Z0-9_-]*$` |
| `--lang` | 是 | `python` / `go` / `node` / `rust` |
| `--arch` | 否 | 分层变体：`cls`（classic 三层式，默认）或 `hex`（hexagonal 四层）；全称 `classic` / `hexagonal` 为兼容别名 |
| `--target` | 否 | 目标目录，默认 `../<name>`；必须不存在或为空 |
| `--module-path` | 否 | Go module 路径，默认同 `--name` |
| `--git` | 否 | 生成后 `git init` 并做首次提交（默认关闭：遵循「不擅自 commit」） |

## 行为细节

1. **复制语言无关资产**：`AGENTS.md`、`.claude/`、`.editorconfig`、`.github/PULL_REQUEST_TEMPLATE.md`、`scripts/check_docs.py`、`docs/` 子集（templates/、context/、standards/general.md + 所选语言、reference/layout.md）。
2. **复制 scaffold**：`scaffold/<lang>/` 工具链（排除 `variants/`）+ `scaffold/<lang>/variants/<arch>/`（所选分层骨架）+ `scaffold/_shared/`（CHANGELOG）。未选变体与生成器本身**不**进入新项目。
3. **生成项目侧文件**：`docs/index.md`（按实际保留文件生成，链接必然有效）、`docs/architecture/contract.md` 与 `system-map.md`（自 templates 填充 TODO）、`docs/architecture/adr/` 目录。
4. **生成 CLAUDE.md**：项目骨架（硬边界 + 项目原则 + 项目任务路由 + 事实源声明）由 init.py 内嵌模板生成（`PROJECT_CLAUDE_TEMPLATE`），追加所选变体 `scaffold/<lang>/variants/<arch>/CLAUDE.md` 正文作为「语言规则」段（段标题标注变体）。
5. **替换与改名**：内容与路径中的三枚占位符全部替换；含占位符的目录组件改名。
6. **收尾**：按 `--git` 决定是否初始化仓库；打印生成清单与「初始化后 10 分钟清单」。

## 退出码

`0` 成功；`2` 参数或前置校验失败（目录已存在、名字非法、语言或变体不支持）。
