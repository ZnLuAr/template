#!/usr/bin/env python3
"""docs/ 健康检查。

规则：
- 错误（退出码 1）：文档间死链（docs/ 全部 .md，含锚点链接）；architecture/
  guides/reference/standards 下文档未登记；ADR 编号重复。
- 警告（不失败）：文档头部缺 status 标记；ADR 编号不连续。
- 豁免登记：docs/templates/、docs/context/（模板与恢复点；死链仍检查）。

仅标准库，在模板仓库与实例化项目中同构可用；可传目录参数检查任意文档树。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):  # Windows 管道下避免 GBK 乱码
        _stream.reconfigure(encoding="utf-8", errors="replace")

DOCS = Path(__file__).resolve().parent.parent / "docs"
EXEMPT_PARTS = {"templates", "context"}
LINK_RE = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)\s]*)?\)")
ADR_NUM_RE = re.compile(r"^(\d{4})-")


def check_links(docs: Path, files: list[Path], errors: list[str]) -> None:
    """全部文档的 .md 链接（含锚点）必须指向存在的文件；外链跳过。"""
    for p in files:
        rel = p.relative_to(docs).as_posix()
        for link in LINK_RE.findall(p.read_text(encoding="utf-8")):
            if link.startswith(("http://", "https://")):
                continue
            if not (p.parent / link).resolve().is_file():
                errors.append(f"死链：{rel} -> {link}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    docs = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DOCS
    index = docs / "index.md"
    if not index.is_file():
        print("check_docs: docs/index.md 不存在", file=sys.stderr)
        return 1

    md_files = sorted(docs.rglob("*.md"))
    check_links(docs, md_files, errors)

    index_links = LINK_RE.findall(index.read_text(encoding="utf-8"))
    indexed = {
        (docs / link).resolve()
        for link in index_links
        if not link.startswith(("http://", "https://"))
        and (docs / link).resolve().is_file()
    }

    for p in md_files:
        rel = p.relative_to(docs).as_posix()
        if p == index:
            continue
        if EXEMPT_PARTS & set(p.relative_to(docs).parts):
            continue
        if p.resolve() not in indexed:
            errors.append(f"未登记：{rel}")
        head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:6])
        if "status" not in head:
            warnings.append(f"缺 status 头部：{rel}")

    adr_dir = docs / "architecture" / "adr"
    if adr_dir.is_dir():
        nums: list[int] = []
        for f in sorted(adr_dir.glob("*.md")):
            m = ADR_NUM_RE.match(f.stem)
            if m:
                nums.append(int(m.group(1)))
        if len(nums) != len(set(nums)):
            errors.append(f"ADR 编号重复：{sorted(nums)}")
        if nums and sorted(nums) != list(range(1, len(nums) + 1)):
            warnings.append(f"ADR 编号不连续：{sorted(nums)}")

    for w in warnings:
        print(f"WARN {w}")
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    print(f"check_docs: {len(md_files)} 篇文档，{len(errors)} 错误，{len(warnings)} 警告")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
