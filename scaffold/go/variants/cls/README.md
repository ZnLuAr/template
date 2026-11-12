# __project_name__

> TODO: 一句话描述 __project_name__。

由项目模板实例化（classic 分层：entry / logic / model / infra）。分层约定见 `docs/reference/layout.md`，AI 入口见 `CLAUDE.md`。

## 快速开始

```bash
go test ./...            # 测试
go vet ./...             # 静态检查
gofmt -w .               # 格式化

go run ./cmd/__project_name__ -name world    # 运行 CLI
```

## 布局

```
cmd/__project_name__/   # entry：参数翻译、组装注入
internal/
├── logic/     # 业务逻辑与编排
├── model/     # 数据 + 纯规则 + 按需接口（零 IO）
└── infra/     # 外部系统实现（时钟、存储、外部 API）
```
