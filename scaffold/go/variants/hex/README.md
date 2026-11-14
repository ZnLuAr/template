# __project_name__

> TODO: 一句话描述 __project_name__。

由项目模板实例化（hexagonal 分层：entry / service / domain / infra）。分层约定见 `docs/reference/layout.md`，AI 入口见 `CLAUDE.md`。

## 快速开始

```bash
go test ./...            # 测试
go vet ./...             # 静态检查
gofmt -w .               # 格式化

go run ./cmd/__project_name__ -name world             # 运行 CLI
go run ./cmd/__project_name__ -name Ada -recent 3     # 问候并回放最近 3 条历史
```

## 布局

```
cmd/__project_name__/   # entry：参数翻译、组装注入
internal/
├── service/   # use case 编排（Greet / Recent）
├── domain/    # 纯领域规则 + 端口定义（Clock 查询 / GreetingLog 命令），零 IO
└── infra/     # 端口实现（时钟、存储、外部系统）
```
