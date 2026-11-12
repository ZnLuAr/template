use __pkg_name__::{infra::SystemClock, logic::Greeter};

#[test]
fn greet_through_real_assembly() {
    // 走真实组装路径；具体问候随系统时钟变化，只断言结构。
    let greeting = Greeter::new(SystemClock).greet("Ada").unwrap();
    assert!(greeting.ends_with(", Ada."));
}
