"""entry.cli 的集成测试：走真实组装路径（SystemClock + Greeter）。"""

from __pkg_name__.entry.cli import main


def test_cli_prints_greeting_for_name(capsys) -> None:
    exit_code = main(["Ada"])

    assert exit_code == 0
    out = capsys.readouterr().out
    # 具体问候随系统时钟变化，只断言结构与名字
    assert out.endswith(", Ada.\n")


def test_cli_defaults_to_world(capsys) -> None:
    exit_code = main([])

    assert exit_code == 0
    assert capsys.readouterr().out.endswith(".\n")
