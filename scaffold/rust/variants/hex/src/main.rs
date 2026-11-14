//! CLI 入口：只做参数翻译与组装，不含业务规则。

use __pkg_name__::infra::{InMemoryGreetingLog, SystemClock};
use __pkg_name__::service::Greeter;

fn main() {
    // 极简参数解析：第一个参数是名字；--recent N 表示问候后打印最近 N 条历史。
    let args: Vec<String> = std::env::args().skip(1).collect();
    let recent = match args.iter().position(|a| a == "--recent") {
        Some(i) => args.get(i + 1).and_then(|v| v.parse().ok()).unwrap_or(0),
        None => 0,
    };
    let name = if args.first().map(String::as_str) == Some("--recent") {
        "world".to_string()
    } else {
        args.first().cloned().unwrap_or_else(|| "world".into())
    };

    // 组装只发生在 entry：infra 适配器注入 service。
    let mut greeter = Greeter::new(SystemClock, InMemoryGreetingLog::new());
    match greeter.greet(&name) {
        Ok(greeting) => {
            println!("{}", greeting.text);
            for item in &greeter.recent(recent) {
                println!("{}", item.text);
            }
        }
        Err(err) => {
            eprintln!("__project_name__: {err}");
            std::process::exit(2);
        }
    }
}
