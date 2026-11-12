//! 端口定义：infra 负责实现，service 只依赖此 trait。

/// 当前时刻的来源（真实实现见 infra，测试用 fake）。
pub trait Clock {
    fn current_hour(&self) -> u8;
}
