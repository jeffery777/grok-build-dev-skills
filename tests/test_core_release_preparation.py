"""Fixed adoption preparation and historical-baseline regressions; no models."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import core_snapshot as core
import eval_core_feedback_candidate as candidate
import grok_package as package
import verify_core_release_preparation as prep


class ReleasePreparationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve(), prefix="grok-preparation-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("vendor/engineering-workflow-core", "tests/fixtures/core-feedback-baseline",
                     "tests/fixtures/core-feedback-candidate", "tests/fixtures/core-release-preparation"):
            shutil.copytree(ROOT / name, self.root / name)
        for name in ("core.lock.json", "tests/fixtures/core-feedback-baseline.lock.json",
                     "tests/fixtures/core-feedback-candidate.lock.json", "tests/fixtures/core-feedback-cases.json",
                     "tests/fixtures/core-release-preparation.lock.json", "scripts/verify_core_release_preparation.py",
                     "scripts/eval_core_feedback_candidate.py", "scripts/core_snapshot.py"):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
            target.chmod(0o644)

    def rejected(self):
        with self.assertRaises((core.SnapshotError, OSError, ValueError)):
            prep.inspect(self.root)

    def test_exact_preparation_keeps_publication_gate_and_formal_default(self):
        value = prep.inspect(self.root)
        self.assertEqual(value["files"], 20)
        self.assertEqual(value["status"], "prepared-publication-pending")
        self.assertIsNone(value["publication_revision"])
        self.assertIsNone(value["tag_object"])
        for key in ("formal_core_adopted", "runtime_qualified", "merge_authorized"):
            self.assertIs(value[key], False)
        result, _ = core.verify(self.root / "core.lock.json", self.root / "vendor/engineering-workflow-core")
        self.assertEqual(result["core_revision"], prep.BASELINE_REVISION)

    def test_historical_baseline_tamper_is_not_hidden_by_insert_only(self):
        (self.root / "tests/fixtures/core-feedback-baseline/README.md").write_bytes(b"short corrupt baseline\n")
        self.rejected()

    def test_unknown_or_claimed_published_manifest_is_rejected(self):
        path = self.root / "tests/fixtures/core-release-preparation.lock.json"
        original = path.read_bytes()
        for field, value in (("reviewed_head", "0" * 40), ("formal_core_adopted", True),
                             ("publication_revision", "0" * 40), ("tag_object", "0" * 40)):
            changed = json.loads(original)
            changed[field] = value
            path.write_text(json.dumps(changed))
            self.rejected()
        path.write_bytes(original)

    def test_original_baseline_pin_cannot_be_replaced(self):
        path = self.root / "tests/fixtures/core-feedback-baseline.lock.json"
        path.write_bytes(path.read_bytes() + b" ")
        self.rejected()

    def test_tamper_missing_extra_and_empty_directory(self):
        fixture = self.root / "tests/fixtures/core-release-preparation"
        path = fixture / "LICENSE"
        original = path.read_bytes()
        path.write_bytes(original + b"changed")
        self.rejected()
        path.unlink()
        self.rejected()
        path.write_bytes(original)
        for name in ("extra.md", "empty"):
            extra = fixture / name
            extra.mkdir() if name == "empty" else extra.write_text("unexpected\n")
            self.rejected()
            extra.rmdir() if extra.is_dir() else extra.unlink()

    def test_unsafe_modes_symlink_hardlink_fifo_are_rejected(self):
        path = self.root / "tests/fixtures/core-feedback-baseline/LICENSE"
        original = path.read_bytes()
        path.chmod(0o755)
        self.rejected()
        path.unlink()
        path.symlink_to(ROOT / "LICENSE")
        self.rejected()
        path.unlink()
        os.link(self.root / "tests/fixtures/core-feedback-baseline/README.md", path)
        self.rejected()
        path.unlink()
        os.mkfifo(path, 0o644)
        self.rejected()
        path.unlink()
        path.write_bytes(original)

    def test_symlink_ancestor_is_rejected(self):
        path = self.root / "tests/fixtures/core-feedback-baseline"
        real = path.with_name("real-baseline")
        path.rename(real)
        path.symlink_to(real, target_is_directory=True)
        self.rejected()

    def test_historical_eval_survives_a_future_formal_vendor_advance(self):
        vendor = self.root / "vendor/engineering-workflow-core"
        shutil.rmtree(vendor)
        shutil.copytree(self.root / "tests/fixtures/core-release-preparation", vendor)
        with self.assertRaises(core.SnapshotError):
            core.verify(self.root / "core.lock.json", vendor)
        # Stub only this unit boundary's future formal acceptance, not provenance.
        files = core.capture_inventory(vendor, frozenset(row["path"] for row in json.loads(
            (self.root / "tests/fixtures/core-release-preparation.lock.json").read_bytes())["files"]))
        with patch.object(candidate, "ROOT", self.root), patch.object(
                candidate.core, "verify", return_value=({"status": "future-test-only"}, files)) as checked:
            _, _, cases = candidate.inspect(self.root / "tests/fixtures/core-feedback-candidate")
        checked.assert_called_once_with(self.root / "core.lock.json", vendor)
        self.assertEqual(len(cases), 9)
        self.assertNotEqual((vendor / "README.md").read_bytes(), prep.baseline(self.root)["README.md"])

    def test_preparation_is_rejected_as_an_ordinary_lock_or_vendor(self):
        value = json.loads((ROOT / "core.lock.json").read_bytes())
        value["core_revision"] = prep.REVIEWED_HEAD
        path = self.root / "core.lock.json"
        path.write_text(json.dumps(value))
        with self.assertRaises(core.SnapshotError):
            core.load_lock(path)
        with self.assertRaises(core.SnapshotError):
            core.verify(ROOT / "core.lock.json", self.root / "tests/fixtures/core-release-preparation")

    def test_cli_publication_requirement_fails_closed(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/verify_core_release_preparation.py"),
                                 "--require-publication"], capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertIsNone(json.loads(result.stdout)["tag_object"])

    def test_bad_json_is_rejected_without_coercion(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'\xff'):
            with self.assertRaises(ValueError):
                prep.parse(raw)

    def test_plain_python_entries_do_not_create_bytecode(self):
        env = dict(os.environ)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        for name, options in (("verify_core_release_preparation.py", []),
                              ("eval_core_feedback_candidate.py", ["--prompt"])):
            result = subprocess.run([sys.executable, str(self.root / "scripts" / name), *options],
                                    cwd=self.root, env=env, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(list(self.root.rglob("__pycache__")))

    def test_baseline_error_cli_does_not_echo_content_or_traceback(self):
        path = self.root / "tests/fixtures/core-feedback-baseline.lock.json"
        path.write_bytes(b'{"private-sentinel":NaN}')
        for name in ("verify_core_release_preparation.py", "eval_core_feedback_candidate.py"):
            result = subprocess.run([sys.executable, "-B", str(self.root / "scripts" / name)],
                                    cwd=self.root, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn(b"private-sentinel", result.stdout + result.stderr)
            self.assertNotIn(b"Traceback", result.stderr)

    def test_developer_files_are_not_distributed(self):
        _, files, _ = package.verify(ROOT)
        self.assertEqual(len(files), 31)
        self.assertFalse(any("preparation" in name or "baseline" in name for name in files))
        self.assertEqual(prep.digest((ROOT / "grok.package.json").read_bytes()),
                         "127ec56cb5f03b1b7751ec03ce8e0a3e686d0def57d11d0415b13d1184e93d8e")


if __name__ == "__main__":
    unittest.main()
