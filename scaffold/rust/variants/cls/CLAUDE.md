# Rust 脚手架 · classic 分层（实例化时合并进项目根 CLAUDE.md 的「语言规则」段）

- 布局：`src/lib.rs` 声明 `logic / model / infra` 模块；entry 内联于 `src/main.rs`（保持薄）；unit 测试与代码同文件（`#[cfg(test)]`），`tests/` 放 integration。
- 铁律：model 零 IO、不依赖任何兄弟模块。惯例：组装只在 main；logic 默认直接用 infra 类型，要替身测试或换实现时抽 model trait（渐进条款见 `docs/reference/layout.md`）。
- 规范本体：`docs/standards/rust.md`（clippy、Result 传播、trait 接口）。
- 常用命令：测试 `cargo test`；lint `cargo clippy -- -D warnings`；格式化 `cargo fmt`；运行 `cargo run -- <name>`。
- 可恢复错误一律 `Result`；`unwrap` 只允许出现在测试与注明不变量的 entry 分支。
