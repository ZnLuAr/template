# __project_name__

> TODO: 一句话描述 __project_name__。

由项目模板实例化（classic 分层：entry / logic / model / infra）。分层约定见 `docs/reference/layout.md`，AI 入口见 `CLAUDE.md`。

## 快速开始

```bash
cargo test                          # 测试
cargo clippy -- -D warnings         # lint
cargo fmt                           # 格式化

cargo run -- Ada                    # 运行 CLI
```

## 布局

```
src/
├── main.rs      # entry：参数翻译、组装注入
├── lib.rs       # 模块声明
├── logic/       # 业务逻辑与编排
├── model/       # 数据 + 纯规则 + 按需接口（零 IO）
└── infra/       # 外部系统实现（时钟、存储、外部 API）
tests/           # integration（走真实组装路径）
```
