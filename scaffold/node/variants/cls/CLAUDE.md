# TypeScript / Node 脚手架 · classic 分层（实例化时合并进项目根 CLAUDE.md 的「语言规则」段）

- 布局：`src/{entry,logic,model,infra}`；`tests/unit` 镜像分层；ESM、Node ≥ 20。
- 铁律：model 零 IO、不 import 任何层、不 import `node:*`。惯例：组装只在 entry；logic 默认直接用 infra 类型，要替身测试或换实现时抽 model 接口（渐进条款见 `docs/reference/layout.md`）。
- 规范本体：`docs/standards/typescript.md`（strict、biome、错误约定）。
- 常用命令：测试 `npm test`；lint `npm run lint`；类型检查 `npm run typecheck`；构建 `npm run build`。
- 公开函数显式返回类型；新功能与 bug 修复必须带测试。
