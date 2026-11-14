# 规范：TypeScript / Node

> status: stable · owner: ZnLuAr · updated: 2026-11-14

面向 Node 工具与服务；前端专用模板见 `frontend-template-next`（本模板不含）。

## 布局

- 分层二选一（`--arch`，变体语义见 [../reference/layout.md](../reference/layout.md)）：cls `src/{entry,logic,model,infra}`（默认）或 hex `src/{entry,service,domain,infra}`；
- `tests/unit`（vitest）镜像分层，integration 视需要；
- ESM（`"type": "module"`），Node ≥ 20。

## 工具链

| 动作 | 命令 |
|---|---|
| 测试 | `npm test`（vitest run） |
| lint + 格式化 | `npm run lint` / `npm run fmt`（biome） |
| 类型检查 | `npm run typecheck`（覆盖 `src` 与 `tests`，`tsconfig.test.json`） |
| 构建 | `npm run build`（tsc → dist/） |

biome formatter：2 空格缩进、行宽 100（与 ruff 一致，配置见 `biome.json`）。

## 代码

- `strict: true`；公开函数显式返回类型；
- 接口：hex 定义在 `domain`（架构前提，service 依赖接口，infra `implements`；查询与命令两类端口都定义于此，示例 `Clock` / `GreetingLog`）；cls 定义在 `model`（按需引入——strict 模式下 fake 必须 `implements` 接口，要写替身测试时抽）；
- 错误：规则层（model/domain）抛 `Error` 子类并携带可判别字段；entry 捕获后转退出码；
- 模块导入用相对路径跨层引用（`.js` 后缀遵循 NodeNext），违反依赖规则即违规信号。

## 禁忌

- 规则层零 IO：model / domain 不 import `node:*` 模块、不 import 其他层（时间、进程、文件系统经注入进入）；
- 不用 `any`；边界确需时用 `unknown` + 收窄，并注明原因；
- 依赖只进 `package.json` 声明，不散装引入 CDN / 全局脚本。
