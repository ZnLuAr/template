#!/usr/bin/env python3
"""从项目模板实例化一个新项目。

用法：
    python scripts/init.py --name my-project --lang python --arch cls --target ../my-project

行为（细节见 docs/reference/init.md）：
1. 复制语言无关资产（AGENTS.md / .claude / .editorconfig / PR 模板 / check_docs.py / docs 子集）；
2. 复制 scaffold/<lang>（工具链）与 scaffold/<lang>/variants/<arch>（分层骨架）及 scaffold/_shared 到项目根；
3. 生成项目侧 docs/index.md、architecture/{contract,system-map,adr/_template}.md；
4. 生成 CLAUDE.md：内嵌项目骨架 + 追加所选变体的语言规则段；
5. 替换全部占位符（内容与路径）；
6. 可选 git init + 首次提交（--git）。

仅标准库，Python 3.11+。
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):  # Windows 管道下避免 GBK 乱码
        _stream.reconfigure(encoding="utf-8", errors="replace")

LANGS = ("python", "go", "node", "rust")
LANG_STANDARD = {"python": "python", "go": "go", "node": "typescript", "rust": "rust"}
LANG_TITLE = {
    "python": "Python",
    "go": "Go",
    "node": "TypeScript / Node",
    "rust": "Rust",
}
# 分层变体：cls = classic（三层式 entry/logic/model/infra）；hex = hexagonal（四层 entry/service/domain/infra）
# 全称 classic / hexagonal 作为别名保留，方便文档与命令互查
ARCHS = ("cls", "hex")
ARCH_ALIASES = {"cls": "cls", "classic": "cls", "hex": "hex", "hexagonal": "hex"}
NAME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")

ROOT_ASSETS = (
    "AGENTS.md",
    ".claude",
    ".editorconfig",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "scripts/check_docs.py",
)
DOC_ASSETS = (
    "docs/templates",
    "docs/context",
    "docs/reference/layout.md",
    "docs/standards/general.md",
)
PROJECT_ONLY_SKILLS = (".claude/skills/new-project",)  # 模板专属，不进项目
# .claude 下不进项目的内容：settings.local.json 是本机私有（权限批准产生的本地文件）
CLAUDE_LOCAL_IGNORE = ("settings.local.json",)

# 项目版 CLAUDE.md 骨架（行为声明见 docs/reference/init.md）
PROJECT_CLAUDE_TEMPLATE = """# CLAUDE.md — {name}

本项目由项目模板实例化：分层约定与文档机制来自模板，业务规则归本仓库。

## 硬边界

- 代码分层规则（classic / hexagonal 双变体，本项目所用变体见下方语言规则段）见 `docs/reference/layout.md`；违反视为缺陷。
- 新增 `docs/` 文档必须登记 `docs/index.md`，`python scripts/check_docs.py` 校验。
- 未经用户明确要求不 commit。

## 项目原则

- **一命令验收**：改动交付前必须通过语言规则段的测试与 lint 命令，加上 `python scripts/check_docs.py`；失败先修根因，不带病交付。装了 just 时 `just check` 一键聚合。
- **0.x 早期不兼容自由**：当更优的长期设计需要不兼容变更时果断做，不为兼容性保留复杂度；升到 1.0 前重审此条。

## 任务路由

| 要做的事 | 先读 |
|---|---|
| 了解结构与分层 | `docs/reference/layout.md` |
| 本语言规范与命令 | `docs/standards/{standard}.md` |
| 写或改文档 | `docs/index.md`、`docs/standards/general.md`（含同步契约表） |
| 重要取舍 | 写 ADR：`docs/architecture/adr/`（从 `_template.md` 开始） |
| 恢复上次会话 | `docs/context/` 最新恢复摘要 |

## 事实源声明

本文件与 AGENTS.md 只做路由；规则本体在 `docs/`，人与 AI 共读同一份。全局工作方式（L0 层）由用户 ai-work-config 提供，本仓库不重复。
"""


def fail(msg: str) -> None:
    print(f"init: {msg}", file=sys.stderr)
    sys.exit(2)


def normalize_package(name: str) -> str:
    return re.sub(r"[-.]+", "_", name).lower()


def copy_asset(root: Path, target: Path, rel: str, ignore: tuple[str, ...] = ()) -> None:
    src, dst = root / rel, target / rel
    if src.is_dir():
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignore) if ignore else None)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def unpack_dir(src: Path, dst: Path, exclude: set[str] = frozenset()) -> None:
    """把 src 的直接子项复制进 dst（scaffold 解包到项目根，不保留 scaffold 路径）。

    目录同名则递归合并（.github/ 由根资产先建、语言侧补 workflows）；
    文件同名视为实例化冲突，报错退出而非静默覆盖。
    """
    dst.mkdir(parents=True, exist_ok=True)
    for item in sorted(src.iterdir()):
        if item.name in exclude:
            continue
        to = dst / item.name
        if item.is_dir():
            unpack_dir(item, to)
        else:
            if to.exists():
                fail(f"实例化冲突：{to} 已存在，拒绝覆盖（检查 scaffold 与根资产的重叠）")
            shutil.copy2(item, to)


def transform(target: Path, values: dict[str, str]) -> None:
    """替换文件内容与路径中的占位符。深度倒序处理，保证父目录改名不使子路径失效。"""
    paths = sorted(target.rglob("*"), key=lambda p: len(p.parts), reverse=True)
    for path in paths:
        if path.is_file():
            try:
                with open(path, encoding="utf-8", newline="") as f:
                    text = f.read()
            except UnicodeDecodeError:
                text = None  # 二进制资源：跳过内容替换，路径改名仍生效
            if text is not None:
                new = text
                for old, val in values.items():
                    new = new.replace(old, val)
                if new != text:
                    with open(path, "w", encoding="utf-8", newline="") as f:
                        f.write(new)
        new_name = path.name
        for old, val in values.items():
            new_name = new_name.replace(old, val)
        if new_name != path.name:
            path.rename(path.with_name(new_name))


def build_claude_md(root: Path, target: Path, name: str, lang: str, arch: str) -> None:
    lang_md = (root / "scaffold" / lang / "variants" / arch / "CLAUDE.md").read_text(
        encoding="utf-8"
    )
    lines = lang_md.splitlines(keepends=True)
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].startswith("# "):
        i += 1
    body = "".join(lines[i:]).strip("\n")

    merged = (
        PROJECT_CLAUDE_TEMPLATE.format(
            name=name, standard=LANG_STANDARD[lang], title=LANG_TITLE[lang]
        ).rstrip()
        + f"\n\n---\n\n## 语言规则：{LANG_TITLE[lang]}（{arch} 分层变体）\n\n"
        + body
        + "\n"
    )
    (target / "CLAUDE.md").write_text(merged, encoding="utf-8")


def write_project_index(target: Path, lang: str) -> None:
    standard = LANG_STANDARD[lang]
    today = date.today().isoformat()
    content = f"""# 文档总索引

> status: stable · owner: TODO · updated: {today}

本文件是 `docs/` 的唯一入口：**每篇文档必须在此登记**，由 `scripts/check_docs.py` 校验（未登记文档、死链都会报错）。

## architecture — 架构与决策

- [contract.md](architecture/contract.md) — 项目契约（实例化后第一件事：改成真实契约）
- [system-map.md](architecture/system-map.md) — 系统地图（随项目成长维护）
- [adr/_template.md](architecture/adr/_template.md) — 新 ADR 从此开始

## reference — 稳定参考

- [layout.md](reference/layout.md) — 目录与分层约定（来自模板）

## standards — 规范

- [general.md](standards/general.md) — 通用规范：commit、review 自查、测试、文档同步契约表
- [{standard}.md](standards/{standard}.md) — 本项目语言规范

## templates — 文档模板

- [adr.md](templates/adr.md) · [contract.md](templates/contract.md) · [design.md](templates/design.md) · [system-map.md](templates/system-map.md) · [context.md](templates/context.md)

## context — 会话恢复点

- [context/README.md](context/README.md) — 恢复摘要的用法与命名约定
"""
    (target / "docs" / "index.md").write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="从项目模板实例化新项目")
    parser.add_argument("--name", required=True, help="项目名，字母开头，可含数字、-、_")
    parser.add_argument("--lang", required=True, choices=LANGS, help="语言脚手架")
    parser.add_argument(
        "--arch",
        default="cls",
        type=lambda s: ARCH_ALIASES.get(s.lower(), s),
        choices=ARCHS,
        help="分层变体：cls/classic（三层式 entry/logic/model/infra，默认）或 hex/hexagonal（四层 entry/service/domain/infra）",
    )
    parser.add_argument("--target", help="目标目录（默认 ../<name>），必须不存在或为空")
    parser.add_argument("--module-path", help="Go module 路径（默认同 --name）")
    parser.add_argument("--git", action="store_true", help="git init 并做首次提交")
    args = parser.parse_args()

    name = args.name
    if not NAME_RE.match(name):
        fail(f"非法项目名 {name!r}：需匹配 {NAME_RE.pattern}")
    lang = args.lang
    arch = args.arch

    root = Path(__file__).resolve().parent.parent
    target = Path(args.target).resolve() if args.target else root.parent / name
    if target.exists() and any(target.iterdir()):
        fail(f"目标目录已存在且非空：{target}")

    values = {
        "__project_name__": name,
        "__pkg_name__": normalize_package(name),
        "__module_path__": args.module_path or name,
    }

    target.mkdir(parents=True)
    for rel in ROOT_ASSETS:
        copy_asset(root, target, rel, ignore=CLAUDE_LOCAL_IGNORE if rel == ".claude" else ())
    for rel in DOC_ASSETS:
        copy_asset(root, target, rel)
    copy_asset(root, target, f"docs/standards/{LANG_STANDARD[lang]}.md")
    unpack_dir(root / "scaffold" / lang, target, exclude={"variants"})  # 工具链到项目根
    unpack_dir(root / "scaffold" / lang / "variants" / arch, target)  # 所选分层变体
    unpack_dir(root / "scaffold" / "_shared", target)

    # 项目侧文档结构
    arch_docs = target / "docs" / "architecture"
    arch_docs.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "docs/templates/contract.md", arch_docs / "contract.md")
    shutil.copy2(root / "docs/templates/system-map.md", arch_docs / "system-map.md")
    (arch_docs / "adr").mkdir()
    shutil.copy2(root / "docs/templates/adr.md", arch_docs / "adr" / "_template.md")
    write_project_index(target, lang)
    build_claude_md(root, target, name, lang, arch)

    for rel in PROJECT_ONLY_SKILLS:
        shutil.rmtree(target / rel, ignore_errors=True)

    transform(target, values)

    if args.git:
        subprocess.run(["git", "init"], cwd=target, check=True, capture_output=True)
        subprocess.run(["git", "add", "-A"], cwd=target, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "chore: instantiate from project template"],
            cwd=target, check=True, capture_output=True,
        )

    print(f"已生成：{target}")
    print("初始化 10 分钟清单：")
    print(f"  cd {target}")
    print("  1. 通读 CLAUDE.md；2. 跑一遍测试；3. 把 docs/architecture/contract.md 改成真实契约")
    print("  4. 补 README 与构建配置里的 TODO；5. 需要时 git init 登记远端")
    return 0


if __name__ == "__main__":
    sys.exit(main())
