//! 命令型端口：问候历史的存储；infra 负责实现，service 只依赖此 trait。

use crate::domain::greeting::Greeting;

/// 问候历史的存储（真实实现见 infra，测试用 fake）。
pub trait GreetingLog {
    fn save(&mut self, greeting: Greeting);
    fn recent(&self, limit: usize) -> Vec<Greeting>;
}
