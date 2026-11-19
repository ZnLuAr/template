# 参考：目录与分层约定

> status: stable · owner: ZnLuAr · updated: 2026-11-20

## 两个平面

**仓库平面**（模板仓库与实例化项目共用语义）：

```
├── README.md / CHANGELOG.md    入口与变更记录
├── CLAUDE.md / AGENTS.md       AI 薄路由（ADR-0003）
├── .claude/                    skills 与权限
├── docs/                       单一事实源（index 强制登记）
├── scaffold/                   语言种子（仅模板仓库有）
├── scripts/                    生成器与检查（项目侧只保留 check_docs.py）
└── .github/                    CI 与 PR 模板（实例化项目带所选语言的 ci.yml）
```

**代码平面**（每个 scaffold 内，双变体可选，ADR-0002）：变体目录在 `scaffold/<lang>/variants/<arch>/`，实例化时由 `--arch` 选择（`cls` 默认 / `hex`；全称 `classic` / `hexagonal` 兼容），未选变体不进入项目。

**cls — classic（三层式，默认）**：`entry / logic / model / infra`

```
entry      入口与 adapter：参数翻译、组装注入；无业务规则
logic      业务逻辑与编排：事务边界、副作用顺序
model      数据结构 + 纯规则 + 按需接口；零 IO
infra      外部系统与技术实现
tests/     镜像分层：unit → model/logic；integration → entry/infra
```

- 铁律（唯一）：model 零 IO、不 import 任何层——不触网络、时钟、文件系统；
- 惯例：组装只在 entry；logic 默认直接用 infra 类型（构造参数收 infra 类型，由 entry 注入）；
- 渐进接口：某依赖出现「想测它但不想碰真实实现」或「预知要换实现」时，抽成 model 里的接口（Protocol / interface / trait），infra 提供实现——接口是按需兑现的动作，不是 day-1 的架构前提。

**hex — hexagonal（四层）**：`entry / service / domain / infra`

```
entry      入口与 adapter：参数翻译、组装注入；无业务规则
service    use case 编排：事务边界、副作用顺序
domain     纯领域规则 + 端口定义；零 IO
infra      外部系统与技术实现；实现 domain 端口
tests/     镜像分层：unit → domain/service；integration → entry/infra
```

依赖铁律（单向）：`entry → service → domain`；`infra → domain`（只实现 domain 定义的端口）；其余方向禁止。

端口分两类（示例见 scaffold）：**查询型**（读外部状态，如 `Clock`）与**命令型**（写副作用，如 `GreetingLog`）——命令型是「可替换的外部世界」的主要形态，repository / gateway 皆属此类。**驱动侧端口**（use case 接口）单入口时可省略，entry 直接依赖 service 具体类型；出现第二种传输（HTTP / 队列）时把 use case 抽成 domain 接口，entry 退为 adapter 之一。

**两变体共性**：组装只发生在 entry；测试镜像分层；同一问候业务在两变体落地——cls 保持最薄形态，hex 含双类型端口与状态（刻意不对称，便于对照「hex 多买了什么」，见 ADR-0002）。

## 各语言落点对照

| 层（cls / hex 对应层） | python | go | node（TS） | rust |
|---|---|---|---|---|
| entry | `src/__pkg_name__/entry/` | `cmd/<name>/` | `src/entry/` | `src/main.rs`（+ `entry` 逻辑内联于 main） |
| logic / service | `logic/` 或 `service/` | `internal/{logic,service}/` | `src/{logic,service}/` | `src/{logic,service}/` |
| model / domain | `model/` 或 `domain/` | `internal/{model,domain}/` | `src/{model,domain}/` | `src/{model,domain}/` |
| infra | `infra/` | `internal/infra/` | `src/infra/` | `src/infra/` |

## 变体选择

| 场景 | 建议 |
|---|---|
| 小工具、CRUD 密集、技术栈统一 | `cls`（默认） |
| 业务规则复杂多变、依赖需长期可替换 | `hex` |

来自传统三层（handler / logic / model / db）习惯的项目选 `cls` 几乎零翻译成本：handlers→entry、logic→logic、model 可含行为函数、db/外部 API→infra。

## 占位符（仅存在于模板仓库，实例化时全部替换）

| 占位符 | 含义 | 替换值来源 |
|---|---|---|
| `__project_name__` | 项目显示名（可含连字符） | `--name` 原样 |
| `__pkg_name__` | 包 / crate / npm 安全名（小写下划线） | 由 `--name` 规范化 |
| `__module_path__` | Go module 路径 | `--module-path`，默认同 `--name` |

路径组件与文件内容中的占位符都会被替换；目录名含占位符时同步改名（如 `src/__pkg_name__/`）。

## 实例化项目的 CLAUDE.md

项目根 CLAUDE.md 不从模板根 CLAUDE.md 派生（两者受众不同）：`scripts/init.py` 用内嵌的项目骨架（硬边界 + 项目任务路由 + 事实源声明，行为参考在模板仓库的 `docs/reference/init.md`）加上所选语言**变体**的规则段拼装生成——语言规则段标题会标注本项目使用的分层变体。

