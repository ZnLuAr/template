#!/usr/bin/env python3
"""实例化脚手架并用真实工具链验收（模板 CI 的本机同款命令）。

用法：
    python scripts/check_scaffold.py [--lang python|go|node|rust|all]

对所选语言 × 两变体（cls / hex）各实例化一个临时项目，依次执行
格式检查 → lint → 测试 → CLI 冒烟。命令以 docs/standards/<lang>.md 工具链表为准
（CLI 冒烟额外证明入口可组装运行——cargo test 不编译 main.rs，只有运行才覆盖）。
python 步骤在一次性 venv 里执行，不污染运行本脚本的解释器环境。
失败保留现场目录并退出 1；需要本机装有 go / node / cargo。

仅标准库，Python 3.11+。
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):  # Windows 管道下避免 GBK 乱码
        _stream.reconfigure(encoding="utf-8", errors="replace")

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parent
NAME = "demo-app"
STEP_TIMEOUT = 600  # 单步秒数上限：入口挂死（等 stdin / 死循环）时及时失败

_spec = importlib.util.spec_from_file_location("tmpl_init", SCRIPTS_DIR / "init.py")
assert _spec is not None and _spec.loader is not None
_init = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_init)  # 复用 LANGS / ARCHS / normalize_package，登记语言单一来源
LANGS, ARCHS = _init.LANGS, _init.ARCHS


def tool(cmd: str) -> str:
    """解析可执行文件全路径（Windows 下 npm 是 .cmd，裸名 subprocess 起不来）。"""
    path = shutil.which(cmd)
    if path is None:
        print(f"check_scaffold: 未找到 {cmd}，请先安装对应工具链", file=sys.stderr)
        sys.exit(2)
    return path


def make_venv(d: Path) -> Path | None:
    """在 d 建一次性 venv，返回其解释器路径；python 安装类步骤全部走它。"""
    r = subprocess.run(
        [sys.executable, "-m", "venv", str(d)],
        capture_output=True, encoding="utf-8", errors="replace",
    )
    if r.returncode != 0:
        print(f"创建 venv 失败:\n{r.stdout}{r.stderr}")
        return None
    bin_dir = "Scripts" if os.name == "nt" else "bin"
    return d / bin_dir / ("python.exe" if os.name == "nt" else "python")


def steps(lang: str, py: Path) -> list[tuple[str, list[str], bool]]:
    """(标签, 命令, 是否要求 stdout 为空)；cwd 为实例化后的项目根。"""
    py_s = str(py)
    if lang == "python":
        pkg = _init.normalize_package(NAME)
        return [
            ("升级 pip（--group 需 ≥ 25.1）", [py_s, "-m", "pip", "install", "--upgrade", "pip"], False),
            ("安装（含开发依赖）", [py_s, "-m", "pip", "install", "-e", ".", "--group", "dev"], False),
            ("格式检查", [py_s, "-m", "ruff", "format", "--check", "src", "tests"], False),
            ("lint", [py_s, "-m", "ruff", "check", "src", "tests"], False),
            ("测试", [py_s, "-m", "pytest"], False),
            ("CLI 冒烟", [py_s, "-m", f"{pkg}.entry.cli", "Ada"], False),
        ]
    if lang == "go":
        go, gofmt = tool("go"), tool("gofmt")
        return [
            ("格式检查", [gofmt, "-l", "."], True),
            ("vet", [go, "vet", "./..."], False),
            ("测试", [go, "test", "./..."], False),
            ("CLI 冒烟", [go, "run", f"./cmd/{NAME}", "-name", "Ada"], False),
        ]
    if lang == "node":
        node, npm = tool("node"), tool("npm")
        return [
            ("安装依赖", [npm, "install"], False),
            ("lint（biome check 含格式检查）", [npm, "run", "lint"], False),
            ("类型检查", [npm, "run", "typecheck"], False),
            ("测试", [npm, "test"], False),
            ("构建", [npm, "run", "build"], False),
            ("CLI 冒烟", [node, "dist/entry/cli.js", "Ada"], False),
        ]
    cargo = tool("cargo")
    return [
        ("格式检查", [cargo, "fmt", "--check"], False),
        ("lint（clippy）", [cargo, "clippy", "--", "-D", "warnings"], False),
        ("测试", [cargo, "test"], False),
        ("CLI 冒烟", [cargo, "run", "--", "Ada"], False),
    ]


def run(argv: list[str], cwd: Path) -> tuple[int, str, str]:
    """返回 (退出码, stdout, stderr)；超时按失败处理并给出去掉的提示。"""
    try:
        r = subprocess.run(
            argv, cwd=cwd, capture_output=True, encoding="utf-8", errors="replace",
            timeout=STEP_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 124, "", f"超时（>{STEP_TIMEOUT}s），疑挂起"
    return r.returncode, r.stdout or "", r.stderr or ""


def verify_lang(lang: str, tmp: Path) -> bool:
    lang_ok = True
    for arch in ARCHS:
        proj = tmp / f"{lang}-{arch}"
        print(f"\n== {lang} / {arch} ==")
        r = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "init.py"), "--name", NAME,
             "--lang", lang, "--arch", arch, "--target", str(proj)],
            capture_output=True, encoding="utf-8", errors="replace",
        )
        if r.returncode != 0:
            print(f"实例化失败:\n{r.stdout}{r.stderr}")
            return False
        venv = make_venv(tmp / f"venv-{lang}-{arch}") if lang == "python" else None
        if lang == "python" and venv is None:
            lang_ok = False
            continue
        arch_ok = True
        for label, argv, expect_empty in steps(lang, venv or Path(sys.executable)):
            code, out, err = run(argv, proj)
            # 空校验只看 stdout：stderr 允许出现告警（如工具链版本提示）
            if code != 0 or (expect_empty and out.strip() != ""):
                arch_ok = False
                print(f"  FAIL {label}（退出码 {code}）")
                detail = (out + err).strip()
                if detail:
                    print("  " + detail.replace("\n", "\n  "))
                break
            print(f"  ok   {label}")
        if arch_ok:  # 按变体清理：失败的现场（含 venv）保留供诊断
            shutil.rmtree(proj, ignore_errors=True)
            if venv is not None:
                shutil.rmtree(venv, ignore_errors=True)
        else:
            lang_ok = False
    return lang_ok


def main() -> int:
    parser = argparse.ArgumentParser(description="实例化脚手架并用真实工具链验收")
    parser.add_argument("--lang", default="all", choices=(*LANGS, "all"), help="验收哪种语言（默认全部）")
    args = parser.parse_args()

    langs = LANGS if args.lang == "all" else (args.lang,)
    tmp = Path(tempfile.mkdtemp(prefix="tmpl-e2e-"))
    failed = [lang for lang in langs if not verify_lang(lang, tmp)]
    if failed:
        print(f"\n失败语言：{', '.join(failed)}；现场目录：{tmp}", file=sys.stderr)
        return 1
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
