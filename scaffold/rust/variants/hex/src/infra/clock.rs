//! SystemClock：domain::Clock 端口的实现，本目录唯一的系统时间触点。

use crate::domain::clock::Clock;
use std::time::{SystemTime, UNIX_EPOCH};

pub struct SystemClock;

impl Clock for SystemClock {
    fn current_hour(&self) -> u8 {
        // UTC 小时（标准库无本地时区）；需要本地时间的真实项目在此引入时区实现。
        let secs = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs())
            .unwrap_or(0);
        ((secs / 3600) % 24) as u8
    }
}
