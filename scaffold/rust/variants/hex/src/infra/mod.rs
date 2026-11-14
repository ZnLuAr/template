//! infra：外部系统与端口的实现。

pub mod clock;
pub mod greeting_log;

pub use clock::SystemClock;
pub use greeting_log::InMemoryGreetingLog;
