//! integration：走真实组装路径（SystemClock + Greeter）。

use __pkg_name__::{infra::SystemClock, service::Greeter};

#[test]
fn real_assembly_produces_greeting() {
    let greeter = Greeter::new(SystemClock);
    // 具体问候随系统时钟变化，只断言结构与名字
    assert!(greeter.greet("Ada").unwrap().ends_with(", Ada."));
}
