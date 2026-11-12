//! CLI 入口：只做参数翻译与组装，不含业务规则。

use __pkg_name__::{infra::SystemClock, service::Greeter};

fn main() {
    let name = std::env::args().nth(1).unwrap_or_else(|| "world".into());

    // 组装只发生在 entry：infra 注入 service。
    let greeter = Greeter::new(SystemClock);
    match greeter.greet(&name) {
        Ok(greeting) => println!("{greeting}"),
        Err(err) => {
            eprintln!("__project_name__: {err}");
            std::process::exit(2);
        }
    }
}
