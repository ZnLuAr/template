# 规范：Rust

> status: stable · owner: ZnLuAr · updated: 2026-11-14

## 布局

- `src/lib.rs` 声明模块，entry 逻辑内联于 `main.rs` 时保持其薄；业务模块二选一（`--arch`，变体语义见 [../reference/layout.md](../reference/layout.md)）：cls `logic / model / infra`（默认）或 hex `service / domain / infra`；
- unit 测试与代码同文件（`#[cfg(test)]`，Rust 惯例）；`tests/` 放 integration。

## 工具链

| 动作 | 命令 |
|---|---|
| 测试 | `cargo test` |
| lint | `cargo clippy -- -D warnings` |
| 格式化 | `cargo fmt` |
| 运行 | `cargo run -- <args>` |

## 代码

- edition 2024，MSRV 1.85；
- 接口是 trait：hex 定义在 `domain`（架构前提，查询与命令两类端口都定义于此，示例 `Clock` / `GreetingLog`）；cls 定义在 `model`（按需引入）；业务层用泛型 `Greeter<C: Clock>` 或 `dyn` 持有，二选一在实现处注明理由；
- 层模块在 `mod.rs` 用 `pub use` 再导出对外类型（如 `logic::Greeter`、`infra::SystemClock`），main / tests 用层边界短路径；层内跨模块用完整路径（`crate::domain::greeting::Greeting`）；
- 可恢复错误一律 `Result<T, E>`：规则层错误起步用 `String`/错误枚举，entry 转译后可用 `thiserror`（引入依赖时同步 `standards/rust.md`）；
- `unwrap`/`expect` 只允许出现在测试与 entry 的「不可能失败」分支，并注明不变量。

## 禁忌

- 规则层零 IO：model / domain 不依赖任何兄弟模块、不触环境（时间经 `Clock` 接口注入；`SystemClock` 的 UTC 实现属 infra）；
- infra 实例的构造只在 main（业务层只接收注入；hex 下 service 不 import infra）；
- 不忽略 clippy 警告式提交（`#[allow]` 需注释原因）。
