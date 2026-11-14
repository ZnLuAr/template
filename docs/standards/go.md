# 规范：Go

> status: stable · owner: ZnLuAr · updated: 2026-11-14

## 布局

- entry 落在 `cmd/<name>/`（薄 main：flag 解析 + 组装）；
- 业务层二选一（`--arch`，变体语义见 [../reference/layout.md](../reference/layout.md)）：cls `internal/{logic,model,infra}`（默认）或 hex `internal/{service,domain,infra}`，跨包可见性靠 `internal` 兜底；
- `tests` 不设独立目录：`*_test.go` 与被测包同目录。

## 工具链

| 动作 | 命令 |
|---|---|
| 测试 | `go test ./...` |
| vet | `go vet ./...` |
| 格式化 | `gofmt -w .` |
| 运行 | `go run ./cmd/<name>` |

golangci-lint 可选自配，基线是 vet + gofmt。

## 代码

- 错误用 `error` 返回值传播，规则与业务层（model/domain、logic/service）不 panic；
- entry 的错误分支输出诊断与 usage 后 `os.Exit(2)`，不以 0 退出；
- wrap 用 `%w`；错误消息小写开头、不带标点；
- 接口是小接口，方法收窄到所需：hex 定义在 `domain`（架构前提，查询与命令两类端口都定义于此，示例 `Clock` / `GreetingLog`）；cls 定义在 `model`（按需——Go 无接口几乎无法做替身测试，预见要测的依赖尽早抽，比 Python 的后抽更前置）；
- 构造函数 `NewXxx` 返回接口或具体类型保持一致：infra 返回具体类型，业务层构造参数收接口（hex）或接口 / infra 具体类型（cls）；
- 表驱动测试优先；fake 实现放被测包的 `_test.go` 内。

## 禁忌

- 规则层零 IO：`internal/model`（cls）/ `internal/domain`（hex）不 import 任何兄弟层；
- infra 实例的构造只在 `cmd/`（业务层只接收注入；hex 下 service 不 import infra）；
- 不用全局可变状态在层间传数据；
- `go.mod` module 路径来自 `--module-path`，不手工改占位符语义。
