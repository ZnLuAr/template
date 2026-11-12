"""check_docs.py 行为测试：全量死链、锚点链接、未登记、豁免目录。"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
CHECK = SCRIPTS_DIR / "check_docs.py"


def run_check(docs: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECK), str(docs)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


class CheckDocsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="tmpl-checkdocs-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, rel: str, text: str) -> None:
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def test_clean_tree_passes(self) -> None:
        self._write("index.md", "# 索引\n\n- [a.md](standards/a.md)\n- [b.md](standards/b.md)\n")
        self._write(
            "standards/a.md",
            "# A\n\n> status: stable\n\n见 [索引](../index.md#索引) 与 [b](b.md#节)。\n",
        )
        self._write("standards/b.md", "# B\n\n> status: stable\n")
        r = run_check(self.tmp)
        self.assertEqual(r.returncode, 0, f"{r.stdout}\n{r.stderr}")

    def test_dead_link_in_any_doc(self) -> None:
        self._write("index.md", "# 索引\n\n- [a.md](standards/a.md)\n")
        self._write("standards/a.md", "# A\n\n> status: stable\n\n缺 [b.md](b.md)。\n")
        r = run_check(self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("死链：standards/a.md -> b.md", r.stderr)

    def test_anchor_link_counts_and_resolves(self) -> None:
        self._write("index.md", "# 索引\n\n- [a.md](standards/a.md#目标)\n")
        self._write("standards/a.md", "# A\n\n> status: stable\n")
        r = run_check(self.tmp)
        self.assertEqual(r.returncode, 0, f"{r.stdout}\n{r.stderr}")

    def test_unregistered_reported(self) -> None:
        self._write("index.md", "# 索引\n")
        self._write("standards/a.md", "# A\n\n> status: stable\n")
        r = run_check(self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("未登记：standards/a.md", r.stderr)

    def test_exempt_dir_skips_registration_but_not_links(self) -> None:
        self._write("index.md", "# 索引\n")
        self._write("templates/t.md", "# T\n\n死链 [x.md](x.md)。\n")
        r = run_check(self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("死链：templates/t.md -> x.md", r.stderr)
        self.assertNotIn("未登记：templates/t.md", r.stderr)


if __name__ == "__main__":
    unittest.main()
