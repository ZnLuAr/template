# TypeScript / Node 脚手架 · hexagonal 分层（实例化时合并进项目根 CLAUDE.md 的「语言规则」段）

- 布局：`src/{entry,service,domain,infra}`；`tests/unit` 镜像分层；ESM、Node ≥ 20。
- 依赖铁律：`entry → service → domain`；infra 只实现 domain 的 interface（查询型如 `Clock`，命令型如 `GreetingLog`）；domain 不 import `node:*` 模块；组装只在 entry。
- 规范本体：`docs/standards/typescript.md`（strict、biome、错误约定）。
- 常用命令：测试 `npm test`；lint `npm run lint`；类型检查 `npm run typecheck`；构建 `npm run build`。
- 公开函数显式返回类型；新功能与 bug 修复必须带测试。
