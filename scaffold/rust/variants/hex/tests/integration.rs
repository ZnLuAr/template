//! integration：走真实组装路径（SystemClock + InMemoryGreetingLog + Greeter）。

use __pkg_name__::infra::{InMemoryGreetingLog, SystemClock};
use __pkg_name__::service::Greeter;

#[test]
fn real_assembly_produces_greeting() {
    let mut greeter = Greeter::new(SystemClock, InMemoryGreetingLog::new());
    // 具体问候随系统时钟变化，只断言结构与名字
    assert!(greeter.greet("Ada").unwrap().text.ends_with(", Ada."));
}

#[test]
fn real_assembly_records_history() {
    let mut greeter = Greeter::new(SystemClock, InMemoryGreetingLog::new());
    greeter.greet("Ada").unwrap();

    let recent = greeter.recent(3);
    // 同一次组装：历史里正是刚生成的那条
    assert_eq!(recent.len(), 1);
    assert!(recent[0].text.ends_with(", Ada."));
}
