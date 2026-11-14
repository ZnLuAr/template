"""init.py 生成器冒烟测试：实例化四种语言并校验关键结构、占位符与文档健康。"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
PLACEHOLDER_TOKENS = ("__project_name__", "__pkg_name__", "__module_path__")
# 变体 CLAUDE.md 的标题行（若 build_claude_md 剥离失败会漏进项目）与模板专属指南名
TEMPLATE_ONLY_MARKERS = ("实例化时合并进项目根", "add-language", "maintain-template")


class InitSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="tmpl-init-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _init(self, lang: str, name: str = "demo-app", arch: str = "cls", *extra: str) -> Path:
        proj = self.tmp / name
        subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "init.py"),
                "--name",
                name,
                "--lang",
                lang,
                "--arch",
                arch,
                "--target",
                str(proj),
                *extra,
            ],
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        return proj

    def _read(self, proj: Path, rel: str) -> str:
        return (proj / rel).read_text(encoding="utf-8")

    def _assert_common(self, proj: Path, lang: str, arch: str = "cls") -> None:
        # 占位符零残留（路径与内容）
        for p in proj.rglob("*"):
            for tok in PLACEHOLDER_TOKENS:
                self.assertNotIn(tok, p.name, f"路径残留 {tok}: {p}")
                if p.is_file():
                    try:
                        text = p.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        continue
                    self.assertNotIn(tok, text, f"内容残留 {tok}: {p}")

        # 未选变体不进项目
        self.assertFalse((proj / "variants").exists())

        # CLAUDE.md 为项目版：标题正确、含变体标注的语言规则段与项目原则、无模板专属内容
        claude = self._read(proj, "CLAUDE.md")
        self.assertIn(f"# CLAUDE.md — {proj.name}", claude)
        self.assertIn(f"（{arch} 分层变体）", claude)
        self.assertIn("项目原则", claude)
        for marker in TEMPLATE_ONLY_MARKERS:
            self.assertNotIn(marker, claude, f"项目 CLAUDE.md 混入模板专属内容：{marker}")

        # 文档机制在项目内自洽
        check = subprocess.run(
            [sys.executable, str(proj / "scripts" / "check_docs.py")],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(
            check.returncode, 0, f"项目 check_docs 失败:\n{check.stdout}\n{check.stderr}"
        )

        # 模板专属内容不进项目
        self.assertFalse((proj / "scripts" / "init.py").exists())
        self.assertFalse((proj / "scaffold").exists())
        self.assertFalse((proj / ".claude" / "skills" / "new-project").exists())
        # .claude 只带共享配置；本机私有文件（权限批准产生的 local）不进项目
        self.assertTrue((proj / ".claude" / "settings.json").is_file())
        self.assertFalse((proj / ".claude" / "settings.local.json").exists())

    def test_python_cls(self) -> None:
        proj = self._init("python", "demo-app", "cls")
        self.assertTrue((proj / "src" / "demo_app" / "entry" / "cli.py").is_file())
        self.assertTrue((proj / "src" / "demo_app" / "logic" / "greeter.py").is_file())
        self.assertTrue((proj / "src" / "demo_app" / "model" / "clock.py").is_file())
        self.assertFalse((proj / "src" / "demo_app" / "service").exists())
        self.assertIn('name = "demo-app"', self._read(proj, "pyproject.toml"))
        self.assertIn("demo_app", self._read(proj, "src/demo_app/logic/greeter.py"))
        self._assert_common(proj, "python", "cls")

    def test_python_hex(self) -> None:
        proj = self._init("python", "demo-app", "hex")
        self.assertTrue((proj / "src" / "demo_app" / "service" / "greeter.py").is_file())
        self.assertTrue((proj / "src" / "demo_app" / "domain" / "greeting.py").is_file())
        self.assertTrue((proj / "src" / "demo_app" / "domain" / "ports.py").is_file())
        self.assertTrue((proj / "src" / "demo_app" / "infra" / "greeting_log.py").is_file())
        self.assertFalse((proj / "src" / "demo_app" / "logic").exists())
        self.assertFalse((proj / "src" / "demo_app" / "model").exists())
        self.assertIn("demo_app", self._read(proj, "src/demo_app/service/greeter.py"))
        self.assertIn("GreetingLog", self._read(proj, "src/demo_app/domain/ports.py"))
        self._assert_common(proj, "python", "hex")

    def test_go_cls(self) -> None:
        proj = self._init("go", "demo-app", "cls")
        self.assertTrue((proj / "cmd" / "demo-app" / "main.go").is_file())
        self.assertIn("module demo-app", self._read(proj, "go.mod"))
        self.assertIn("demo-app/internal/logic", self._read(proj, "cmd/demo-app/main.go"))
        self.assertTrue((proj / "internal" / "model" / "clock.go").is_file())
        self.assertFalse((proj / "internal" / "service").exists())
        self._assert_common(proj, "go", "cls")

    def test_go_hex(self) -> None:
        proj = self._init("go", "demo-app", "hex")
        self.assertIn("demo-app/internal/service", self._read(proj, "cmd/demo-app/main.go"))
        self.assertTrue((proj / "internal" / "domain" / "clock.go").is_file())
        self.assertTrue((proj / "internal" / "domain" / "greeting_log.go").is_file())
        self.assertTrue((proj / "internal" / "infra" / "greeting_log.go").is_file())
        self.assertFalse((proj / "internal" / "logic").exists())
        self._assert_common(proj, "go", "hex")

    def test_node_both_archs(self) -> None:
        cls = self._init("node", "demo-app", "cls")
        self.assertTrue((cls / "src" / "entry" / "cli.ts").is_file())
        self.assertTrue((cls / "src" / "logic" / "greeter.ts").is_file())
        self.assertIn('"name": "demo-app"', self._read(cls, "package.json"))
        self._assert_common(cls, "node", "cls")

        hex_ = self._init("node", "demo-app-hex", "hex")
        self.assertTrue((hex_ / "src" / "service" / "greeter.ts").is_file())
        self.assertTrue((hex_ / "src" / "domain" / "greetingLog.ts").is_file())
        self.assertTrue((hex_ / "src" / "infra" / "inMemoryGreetingLog.ts").is_file())
        self.assertFalse((hex_ / "src" / "logic").exists())
        self._assert_common(hex_, "node", "hex")

    def test_rust_both_archs(self) -> None:
        cls = self._init("rust", "demo-app", "cls")
        self.assertTrue((cls / "src" / "main.rs").is_file())
        self.assertTrue((cls / "src" / "logic" / "greeter.rs").is_file())
        self.assertIn('name = "demo_app"', self._read(cls, "Cargo.toml"))
        self.assertIn("use demo_app::", self._read(cls, "src/main.rs"))
        self._assert_common(cls, "rust", "cls")

        hex_ = self._init("rust", "demo-app-hex", "hex")
        self.assertTrue((hex_ / "src" / "service" / "greeter.rs").is_file())
        self.assertTrue((hex_ / "src" / "domain" / "greeting_log.rs").is_file())
        self.assertTrue((hex_ / "src" / "infra" / "greeting_log.rs").is_file())
        self.assertFalse((hex_ / "src" / "logic").exists())
        self._assert_common(hex_, "rust", "hex")

    def test_rust_layer_reexports(self) -> None:
        # main/tests 用层边界短路径（logic::Greeter、infra::SystemClock），
        # 依赖 mod.rs 的 pub use 再导出；缺失即编译失败（曾为存量 bug）
        for arch, mod_pair in (
            ("cls", ("src/logic/mod.rs", "pub use greeter::Greeter")),
            ("cls", ("src/infra/mod.rs", "pub use clock::SystemClock")),
            ("hex", ("src/service/mod.rs", "pub use greeter::Greeter")),
        ):
            layer = mod_pair[0].split("/")[1]
            with self.subTest(arch=arch, layer=layer):
                proj = self._init("rust", f"demo-reexport-{layer}", arch)
                self.assertIn(mod_pair[1], self._read(proj, mod_pair[0]))

    def test_arch_alias(self) -> None:
        # 全称别名（classic / hexagonal）与短名等价
        for alias, arch, marker, pkg in (
            ("classic", "cls", "src/demo_app/logic/greeter.py", "demo-app"),
            ("hexagonal", "hex", "src/demo_app_hex/service/greeter.py", "demo-app-hex"),
        ):
            with self.subTest(arch=alias):
                proj = self._init("python", pkg, alias)
                self.assertTrue((proj / marker).is_file())
                self.assertIn(f"（{arch} 分层变体）", self._read(proj, "CLAUDE.md"))

    def test_rejects_invalid_arch(self) -> None:
        r = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "init.py"), "--name", "ok-name", "--lang", "python",
             "--arch", "layered", "--target", str(self.tmp / "x")],
            capture_output=True, encoding="utf-8", errors="replace",
        )
        self.assertEqual(r.returncode, 2)

    def test_go_module_path(self) -> None:
        proj = self._init(
            "go", "svc", "cls", "--module-path", "github.com/znluar/svc"
        )
        self.assertIn("module github.com/znluar/svc", self._read(proj, "go.mod"))

    def test_transform_tolerates_binary_files(self) -> None:
        """transform 遇非 UTF-8 文件跳过内容替换，路径改名仍生效（二进制资源场景）。"""
        spec = importlib.util.spec_from_file_location("tmpl_init", SCRIPTS_DIR / "init.py")
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        d = self.tmp / "binproj"
        d.mkdir()
        (d / "logo.__project_name__.bin").write_bytes(b"\xff\xfe\x00__project_name__")
        mod.transform(d, {"__project_name__": "demo"})
        self.assertTrue((d / "logo.demo.bin").is_file())
        self.assertFalse((d / "logo.__project_name__.bin").exists())

    def test_rejects_invalid_name(self) -> None:
        r = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "init.py"), "--name", "1bad", "--lang", "python",
             "--target", str(self.tmp / "x")],
            capture_output=True, encoding="utf-8", errors="replace",
        )
        self.assertEqual(r.returncode, 2)

    def test_rejects_nonempty_target(self) -> None:
        occupied = self.tmp / "occupied"
        occupied.mkdir()
        (occupied / "x.txt").write_text("x", encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "init.py"), "--name", "ok-name", "--lang", "python",
             "--target", str(occupied)],
            capture_output=True, encoding="utf-8", errors="replace",
        )
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
