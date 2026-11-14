//! InMemoryGreetingLog：domain::GreetingLog 端口的内存实现。
//! 演示用；换文件 / DB 存储时新写 adapter 即可，domain 与 service 不动。

use crate::domain::greeting::Greeting;
use crate::domain::greeting_log::GreetingLog;

pub struct InMemoryGreetingLog {
    items: Vec<Greeting>,
}

impl InMemoryGreetingLog {
    pub fn new() -> Self {
        Self { items: Vec::new() }
    }
}

impl Default for InMemoryGreetingLog {
    fn default() -> Self {
        Self::new()
    }
}

impl GreetingLog for InMemoryGreetingLog {
    fn save(&mut self, greeting: Greeting) {
        self.items.push(greeting);
    }

    fn recent(&self, limit: usize) -> Vec<Greeting> {
        if limit == 0 {
            return Vec::new();
        }
        self.items.iter().rev().take(limit).cloned().collect()
    }
}
