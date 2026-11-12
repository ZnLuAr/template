# Go 脚手架 · classic 分层（实例化时合并进项目根 CLAUDE.md 的「语言规则」段）

- 布局：entry 在 `cmd/<name>/`（薄 main），业务层在 `internal/{logic,model,infra}`；`*_test.go` 与被测包同目录。
- 铁律：`internal/model` 零 IO、不 import 任何兄弟层。惯例：组装只在 `cmd/`；logic 默认直接用 infra 类型，要替身测试或换实现时抽 model 窄接口（渐进条款见 `docs/reference/layout.md`）。
- 规范本体：`docs/standards/go.md`（错误传播、接口收窄、表驱动测试）。
- 常用命令：测试 `go test ./...`；vet `go vet ./...`；格式化 `gofmt -w .`；运行 `go run ./cmd/<name>`。
- 新功能与 bug 修复必须带测试；错误用 `error` 返回值，不 panic。
