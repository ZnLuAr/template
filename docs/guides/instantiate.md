# 指南：实例化一个新项目

> status: stable · owner: ZnLuAr · updated: 2026-11-12

## 前置

- Python 3.11+（运行生成器，仅标准库）；
- 目标目录不存在（生成器拒绝覆盖非空目录）。

## 步骤

```bash
# 在模板仓库根目录运行（--arch 默认 cls）
python scripts/init.py --name my-project --lang python --target ../my-project

# 业务复杂的项目选 hexagonal 变体（hex / hexagonal 等价）
python scripts/init.py --name my-service --lang go --arch hex \
    --module-path github.com/znluar/my-service --target ../my-service
```

分层变体（ADR-0002）：`cls` = classic 三层式 `entry/logic/model/infra`（默认）；`hex` = hexagonal 四层 `entry/service/domain/infra`。选择依据见 [reference/layout.md](../reference/layout.md) 的「变体选择」。

生成后目录即一个自洽的新项目：语言骨架可立即跑测试，文档机制与 AI 入口已就位（生成器未携带 `scripts/init.py` 本身，新项目保持干净）。

完整参数与行为细节见 [reference/init.md](../reference/init.md)。

## 初始化后 10 分钟清单

1. `cd <target>`，通读合并后的 `CLAUDE.md`；
2. 跑一遍项目测试（README 的快速开始命令）；
3. 把 `docs/architecture/contract.md` 从模板改成本项目的真实契约（目标 / 不做 / 验收）；
4. `README.md` 与 `pyproject.toml`（或 Cargo.toml / package.json / go.mod）里的 TODO 描述补齐；
5. 需要时 `--git` 重新生成或手动 `git init`，登记远端。

## 常见故障

| 现象 | 处理 |
|---|---|
| `target already exists and is not empty` | 换目录或清空后重试；生成器不做覆盖 |
| `invalid --lang` | 取值：`python` / `go` / `node` / `rust` |
| `invalid --arch` | 取值：`cls` / `hex`（别名 `classic` / `hexagonal`） |
| 项目内 `check_docs.py` 报未登记 | 新增文档后在项目 `docs/index.md` 登记 |
