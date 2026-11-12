"""SystemClock：domain.Clock 端口的实现，本包内唯一的系统时间触点。"""

from datetime import datetime


class SystemClock:
    def current_hour(self) -> int:
        return datetime.now().hour
