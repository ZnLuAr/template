//! Greeter 业务逻辑：编排规则与外部能力，不关心具体实现。

use crate::model::clock::Clock;
use crate::model::greeting::greeting_for;

/// 问候业务逻辑；clock 由 entry 注入。
pub struct Greeter<C: Clock> {
    clock: C,
}

impl<C: Clock> Greeter<C> {
    pub fn new(clock: C) -> Self {
        Self { clock }
    }

    /// 按当前时刻问候。
    pub fn greet(&self, name: &str) -> Result<String, String> {
        greeting_for(self.clock.current_hour(), name)
    }
}

#[cfg(test)]
mod tests {
    use super::Greeter;

    struct FakeClock(u8);

    impl crate::model::clock::Clock for FakeClock {
        fn current_hour(&self) -> u8 {
            self.0
        }
    }

    #[test]
    fn greet_uses_clock_hour() {
        assert_eq!(
            Greeter::new(FakeClock(9)).greet("Ada").unwrap(),
            "Good morning, Ada."
        );
        assert_eq!(
            Greeter::new(FakeClock(21)).greet("Ada").unwrap(),
            "Good evening, Ada."
        );
    }
}
