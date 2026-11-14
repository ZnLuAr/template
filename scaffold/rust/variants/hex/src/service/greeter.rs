//! Greeter use case：编排领域规则与端口，不关心具体实现。

use crate::domain::clock::Clock;
use crate::domain::greeting::Greeting;
use crate::domain::greeting::greeting_for;
use crate::domain::greeting_log::GreetingLog;

/// 问候 use case：应用规则生成问候并记录历史；clock 与 log 由 entry 注入。
pub struct Greeter<C: Clock, L: GreetingLog> {
    clock: C,
    log: L,
}

impl<C: Clock, L: GreetingLog> Greeter<C, L> {
    pub fn new(clock: C, log: L) -> Self {
        Self { clock, log }
    }

    /// 按当前时刻问候，并把结果记入历史。
    pub fn greet(&mut self, name: &str) -> Result<Greeting, String> {
        let greeting = greeting_for(self.clock.current_hour(), name)?;
        self.log.save(greeting.clone());
        Ok(greeting)
    }

    /// 返回最近 limit 条问候，新的在前。
    pub fn recent(&self, limit: usize) -> Vec<Greeting> {
        self.log.recent(limit)
    }
}

#[cfg(test)]
mod tests {
    use super::Greeter;
    use crate::domain::clock::Clock;
    use crate::domain::greeting::Greeting;
    use crate::domain::greeting_log::GreetingLog;

    struct FakeClock(u8);

    impl Clock for FakeClock {
        fn current_hour(&self) -> u8 {
            self.0
        }
    }

    struct FakeLog {
        saved: Vec<Greeting>,
    }

    impl GreetingLog for FakeLog {
        fn save(&mut self, greeting: Greeting) {
            self.saved.push(greeting);
        }

        fn recent(&self, limit: usize) -> Vec<Greeting> {
            if limit == 0 {
                return Vec::new();
            }
            self.saved.iter().rev().take(limit).cloned().collect()
        }
    }

    #[test]
    fn greet_applies_rule_and_records_history() {
        let mut greeter = Greeter::new(FakeClock(9), FakeLog { saved: Vec::new() });
        let greeting = greeter.greet("Ada").unwrap();

        assert_eq!(greeting.text, "Good morning, Ada.");
        // 编排可见：规则被应用，副作用被记录。
        assert_eq!(greeter.recent(1), vec![greeting]);
    }

    #[test]
    fn recent_reads_through_log_port() {
        let mut greeter = Greeter::new(FakeClock(9), FakeLog { saved: Vec::new() });
        greeter.greet("Ada").unwrap();
        greeter.greet("Grace").unwrap();

        let recent = greeter.recent(1);
        assert_eq!(recent.len(), 1);
        assert_eq!(recent[0].name, "Grace");
    }
}
