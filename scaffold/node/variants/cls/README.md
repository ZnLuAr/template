# __project_name__

> TODO: 一句话描述 __project_name__。

由项目模板实例化（classic 分层：entry / logic / model / infra）。分层约定见 `docs/reference/layout.md`，AI 入口见 `CLAUDE.md`。

## 快速开始

```bash
npm install
npm test               # 测试（vitest）
npm run typecheck      # 类型检查
npm run lint           # biome

npm run build && node dist/entry/cli.js Ada    # 运行 CLI
```

## 布局

```
src/
├── entry/     # 入口与 adapter（CLI）
├── logic/     # 业务逻辑与编排
├── model/     # 数据 + 纯规则 + 按需接口（零 IO）
└── infra/     # 外部系统实现（时钟、存储、外部 API）
tests/
└── unit/          # model、logic（fake 替身）
```
