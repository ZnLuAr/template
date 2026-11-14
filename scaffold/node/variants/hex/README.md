# __project_name__

> TODO: 一句话描述 __project_name__。

由项目模板实例化（hexagonal 分层：entry / service / domain / infra）。分层约定见 `docs/reference/layout.md`，AI 入口见 `CLAUDE.md`。

## 快速开始

```bash
npm install
npm test               # 测试（vitest）
npm run typecheck      # 类型检查
npm run lint           # biome

npm run build && node dist/entry/cli.js Ada             # 运行 CLI
npm run build && node dist/entry/cli.js Ada --recent 3  # 问候并回放最近 3 条历史
```

## 布局

```
src/
├── entry/     # 入口与 adapter（CLI）
├── service/   # use case 编排（greet / recent）
├── domain/    # 纯领域规则 + 端口定义（Clock 查询 / GreetingLog 命令），零 IO
└── infra/     # 端口实现（时钟、存储、外部系统）
tests/
└── unit/          # domain、service（fake 替身）
```
