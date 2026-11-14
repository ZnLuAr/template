//! Greeting 实体与生成规则：纯领域规则。

/// 一条已生成的问候（领域对象，携带规则输入与输出）。
#[derive(Clone, Debug, PartialEq)]
pub struct Greeting {
    pub hour: u8,
    pub name: String,
    pub text: String,
}

/// 按一天中的时刻（0..23）生成问候；hour 越界返回错误。
pub fn greeting_for(hour: u8, name: &str) -> Result<Greeting, String> {
    let part = match hour {
        5..=11 => "Good morning",
        12..=17 => "Good afternoon",
        18..=22 => "Good evening",
        23 | 0..=4 => "Good night",
        _ => return Err(format!("hour 必须在 0..23，收到 {hour}")),
    };
    Ok(Greeting {
        hour,
        name: name.to_string(),
        text: format!("{part}, {name}."),
    })
}

#[cfg(test)]
mod tests {
    use super::greeting_for;

    #[test]
    fn matches_expected_parts() {
        let cases = [
            (0u8, "Good night"),
            (4, "Good night"),
            (5, "Good morning"),
            (11, "Good morning"),
            (12, "Good afternoon"),
            (17, "Good afternoon"),
            (18, "Good evening"),
            (22, "Good evening"),
            (23, "Good night"),
        ];
        for (hour, part) in cases {
            assert_eq!(
                greeting_for(hour, "Ada").unwrap().text,
                format!("{part}, Ada.")
            );
        }
    }

    #[test]
    fn carries_rule_inputs() {
        let greeting = greeting_for(9, "Ada").unwrap();
        assert_eq!((greeting.hour, greeting.name.as_str()), (9, "Ada"));
    }

    #[test]
    fn rejects_invalid_hour() {
        for hour in [24u8, 255] {
            assert!(greeting_for(hour, "Ada").is_err());
        }
    }
}
