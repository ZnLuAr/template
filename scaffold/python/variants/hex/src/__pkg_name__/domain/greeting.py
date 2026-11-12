"""Greeting 策略：纯领域规则。"""


def greeting_for(hour: int, name: str) -> str:
    """按一天中的时刻（0..23）生成问候语。

    Raises:
        ValueError: hour 越界。
    """
    if not 0 <= hour <= 23:
        raise ValueError(f"hour 必须在 0..23，收到 {hour}")
    if 5 <= hour < 12:
        part = "Good morning"
    elif 12 <= hour < 18:
        part = "Good afternoon"
    elif 18 <= hour < 23:
        part = "Good evening"
    else:
        part = "Good night"
    return f"{part}, {name}."
