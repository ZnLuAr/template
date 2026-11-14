# __project_name__

> TODO: 一句话描述 __project_name__。

由项目模板实例化（hexagonal 分层：entry / service / domain / infra）。分层约定见 `docs/reference/layout.md`，AI 入口见 `CLAUDE.md`。

## 快速开始

```bash
cargo test                          # 测试
cargo clippy -- -D warnings         # lint
cargo fmt                           # 格式化

cargo run -- Ada                    # 运行 CLI
cargo run -- Ada --recent 3         # 问候并回放最近 3 条历史
```

## 布局

```
src/
├── main.rs      # entry：参数翻译、组装注入
├── lib.rs       # 模块声明
├── service/     # use case 编排（greet / recent）
├── domain/      # 纯领域规则 + 端口定义（Clock 查询 / GreetingLog 命令），零 IO
└── infra/       # 端口实现（时钟、存储、外部系统）
tests/           # integration（走真实组装路径）
```
