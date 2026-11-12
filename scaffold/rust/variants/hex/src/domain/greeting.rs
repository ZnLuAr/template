//! Greeting 策略：纯领域规则。

/// 按一天中的时刻（0..23）生成问候语；hour 越界返回错误。
pub fn greeting_for(hour: u8, name: &str) -> Result<String, String> {
    match hour {
        5..=11 => Ok(format!("Good morning, {name}.")),
        12..=17 => Ok(format!("Good afternoon, {name}.")),
        18..=22 => Ok(format!("Good evening, {name}.")),
        23 | 0..=4 => Ok(format!("Good night, {name}.")),
        _ => Err(format!("hour 必须在 0..23，收到 {hour}")),
    }
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
            assert_eq!(greeting_for(hour, "Ada").unwrap(), format!("{part}, Ada."));
        }
    }

    #[test]
    fn rejects_invalid_hour() {
        for hour in [24u8, 255] {
            assert!(greeting_for(hour, "Ada").is_err());
        }
    }
}
