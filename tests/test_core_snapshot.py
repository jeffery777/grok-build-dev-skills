"""Offline acceptance and adversarial fixtures; never starts Grok or a model."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("core_snapshot", ROOT / "scripts/core_snapshot.py")
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="p3g1-tests-", dir=os.path.realpath("/tmp"))
        self.addCleanup(self.temp.cleanup)
        self.case = Path(self.temp.name).resolve()
        self.snapshot = self.case / "snapshot"
        shutil.copytree(ROOT / "vendor/engineering-workflow-core", self.snapshot)
        self.lock = self.case / "lock.json"
        self.lock.write_bytes((ROOT / "core.lock.json").read_bytes())
        self.destination = self.case / "staged"

    def edit_lock(self, change):
        value = json.loads(self.lock.read_text())
        change(value)
        self.lock.write_text(json.dumps(value))

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/core_snapshot.py"), *args,
             "--lock", str(self.lock), "--snapshot", str(self.snapshot)],
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True, text=True, timeout=10,
        )

    def rejected_lock(self, change):
        self.edit_lock(change)
        with self.assertRaises(core.SnapshotError):
            core.verify(self.lock, self.snapshot)

    def test_pinned_bytes_and_false_authority(self):
        result, files = core.verify(self.lock, self.snapshot)
        self.assertEqual(result["core_revision"], "784ed24f4a09ec35ac7209e0fd2287b214aea260")
        self.assertEqual(result["collection_sha256"], "f308093e1dbb6ba2796a3b286406a5f02adde692d05a200b2894e88527bed3c4")
        self.assertEqual(result["verified_files"], 11)
        self.assertEqual(result["local_references"], 298)
        self.assertFalse(result["runtime_qualified"])
        self.assertFalse(result["delivery_ready"])
        self.assertEqual(set(files), core.FILES)

    def test_stage_readback_and_modes(self):
        result = core.stage(self.lock, self.snapshot, self.destination)
        self.assertEqual(result["status"], "staged")
        readback, staged = core.verify(self.lock, self.destination)
        self.assertEqual(readback["collection_sha256"], result["collection_sha256"])
        for name, data in staged.items():
            self.assertEqual(data, (ROOT / "vendor/engineering-workflow-core" / name).read_bytes())
            self.assertEqual(stat.S_IMODE((self.destination / name).stat().st_mode), 0o644)
        self.assertEqual(stat.S_IMODE(self.destination.stat().st_mode), 0o700)

    def test_existing_target_is_not_adopted_or_overwritten(self):
        self.destination.mkdir()
        sentinel = self.destination / "keep"
        sentinel.write_text("unchanged")
        with self.assertRaises(FileExistsError):
            core.stage(self.lock, self.snapshot, self.destination)
        self.assertEqual(sentinel.read_text(), "unchanged")
        self.assertEqual(list(self.destination.iterdir()), [sentinel])

    def test_tamper_does_not_create_destination(self):
        (self.snapshot / "README.md").write_text("changed")
        result = self.cli("stage", "--destination", str(self.destination))
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.destination.exists())

    def test_outside_temp_target_is_rejected(self):
        with self.assertRaises(core.SnapshotError):
            core.stage(self.lock, self.snapshot, Path("/p3g1-must-not-create"))

    def test_stage_cannot_modify_source(self):
        with self.assertRaises(core.SnapshotError):
            core.stage(self.lock, self.snapshot, self.snapshot / "new")
        self.assertFalse((self.snapshot / "new").exists())

    def test_destination_symlink_is_rejected(self):
        actual = self.case / "keep"
        actual.mkdir()
        self.destination.symlink_to(actual, target_is_directory=True)
        with self.assertRaises(FileExistsError):
            core.stage(self.lock, self.snapshot, self.destination)
        self.assertEqual(list(actual.iterdir()), [])

    def test_destination_parent_symlink_is_rejected(self):
        alias = self.case / "alias"
        alias.symlink_to(self.case, target_is_directory=True)
        with self.assertRaises(OSError):
            core.stage(self.lock, self.snapshot, alias / "output")
        self.assertFalse((self.case / "output").exists())

    def test_wrong_identity_and_schema(self):
        original = self.lock.read_bytes()
        for key, value in [
            ("core_revision", "main"), ("core_revision", "0" * 40),
            ("core_repository", "https://example.invalid/other"),
            ("contract_language", "en"), ("schema_version", True),
            ("schema_version", 2),
        ]:
            with self.subTest(key=key, value=value):
                self.lock.write_bytes(original)
                self.rejected_lock(lambda data: data.__setitem__(key, value))

    def test_unknown_field_is_rejected(self):
        self.rejected_lock(lambda data: data.__setitem__("authorize", True))

    def test_wrong_algorithm_and_collection(self):
        original = self.lock.read_bytes()
        for key, value in [("algorithm", "sha256-path-nul-sha256-lf-v1"), ("sha256", "0" * 64)]:
            with self.subTest(key=key):
                self.lock.write_bytes(original)
                self.rejected_lock(lambda data: data["collection"].__setitem__(key, value))

    def test_wrong_license_identity(self):
        self.rejected_lock(lambda data: data["license"].__setitem__("sha256", "0" * 64))

    def test_wrong_license_path(self):
        self.rejected_lock(lambda data: data["license"].__setitem__("path", "../LICENSE"))

    def test_duplicate_json_key(self):
        text = self.lock.read_text().replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1')
        self.lock.write_text(text)
        with self.assertRaisesRegex(core.SnapshotError, "duplicate"):
            core.verify(self.lock, self.snapshot)

    def test_duplicate_manifest_path(self):
        self.rejected_lock(lambda data: data["files"].__setitem__(1, copy.deepcopy(data["files"][0])))

    def test_invalid_manifest_paths(self):
        original = self.lock.read_bytes()
        for name in ["../LICENSE", "/LICENSE", "x//y.md", "./README.md",
                     "a/../README.md", "a\tb.md", "a\nb.md", "a\rb.md",
                     "a\x00b.md", "a\\b.md", "unexpected.md"]:
            with self.subTest(path=name):
                self.lock.write_bytes(original)
                self.rejected_lock(lambda data: data["files"][0].__setitem__("path", name))

    def test_unknown_or_malformed_digest(self):
        original = self.lock.read_bytes()
        for value in ["0" * 64, "A" * 64, 12, "abcd"]:
            with self.subTest(value=value):
                self.lock.write_bytes(original)
                self.rejected_lock(lambda data: data["files"][0].__setitem__("sha256", value))

    def test_missing_or_extra_manifest_file(self):
        original = self.lock.read_bytes()
        self.rejected_lock(lambda data: data["files"].pop())
        self.lock.write_bytes(original)
        self.rejected_lock(lambda data: data["files"].append(copy.deepcopy(data["files"][0])))

    def test_sorted_collection_is_order_independent(self):
        self.edit_lock(lambda data: data["files"].reverse())
        self.assertEqual(core.verify(self.lock, self.snapshot)[0]["verified_files"], 11)

    def test_json_and_utf8_errors(self):
        for bad in [b"{", b"\xff", b"[]"]:
            with self.subTest(bad=bad):
                self.lock.write_bytes(bad)
                with self.assertRaises(core.SnapshotError):
                    core.verify(self.lock, self.snapshot)

    def test_json_conversion_and_nesting_errors_are_bounded(self):
        for bad in [b"9" * 5000, b"[" * 50000 + b"0" + b"]" * 50000]:
            with self.subTest(length=len(bad)):
                self.assertLess(len(bad), core.MAX_FILE_BYTES)
                self.lock.write_bytes(bad)
                result = self.cli("stage", "--destination", str(self.destination))
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                error = json.loads(result.stderr)
                self.assertEqual(error["status"], "error")
                self.assertLess(len(error["error"]), 100)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn(str(ROOT), result.stderr)
                self.assertNotIn(str(self.case), result.stderr)
                self.assertFalse(self.destination.exists())

    def test_missing_snapshot_file(self):
        (self.snapshot / "README.md").unlink()
        with self.assertRaises(core.SnapshotError):
            core.verify(self.lock, self.snapshot)

    def test_extra_file_and_empty_directory(self):
        extra = self.snapshot / "unexpected"
        for directory in [False, True]:
            with self.subTest(directory=directory):
                if directory:
                    extra.mkdir()
                else:
                    extra.write_text("extra")
                with self.assertRaises(core.SnapshotError):
                    core.verify(self.lock, self.snapshot)
                if directory:
                    extra.rmdir()
                else:
                    extra.unlink()

    def test_bytes_are_not_newline_normalized(self):
        p = self.snapshot / "contracts/workflow.md"
        p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
        with self.assertRaisesRegex(core.SnapshotError, "digest"):
            core.verify(self.lock, self.snapshot)

    def test_license_tamper(self):
        (self.snapshot / "LICENSE").write_text("removed notice")
        with self.assertRaisesRegex(core.SnapshotError, "digest"):
            core.verify(self.lock, self.snapshot)

    def test_snapshot_mode_drift(self):
        (self.snapshot / "README.md").chmod(0o755)
        with self.assertRaisesRegex(core.SnapshotError, "mode"):
            core.verify(self.lock, self.snapshot)

    def test_symlink_file_and_snapshot_root(self):
        path = self.snapshot / "README.md"
        path.unlink()
        path.symlink_to(ROOT / "README.md")
        with self.assertRaises(OSError):
            core.verify(self.lock, self.snapshot)
        alias = self.case / "snapshot-alias"
        alias.symlink_to(self.snapshot, target_is_directory=True)
        with self.assertRaises(OSError):
            core.verify(self.lock, alias)

    def test_symlink_directory(self):
        directory = self.snapshot / "contracts"
        directory.rename(self.case / "contracts")
        directory.symlink_to(self.case / "contracts", target_is_directory=True)
        with self.assertRaises(core.SnapshotError):
            core.verify(self.lock, self.snapshot)

    def test_hardlink_is_rejected(self):
        path = self.snapshot / "README.md"
        path.rename(self.case / "linked")
        os.link(self.case / "linked", path)
        with self.assertRaisesRegex(core.SnapshotError, "non-hardlinked"):
            core.verify(self.lock, self.snapshot)

    def test_special_snapshot_file_never_hangs(self):
        path = self.snapshot / "README.md"
        path.unlink()
        os.mkfifo(path, 0o644)
        result = self.cli("verify")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stderr)["status"], "error")

    def test_lock_symlink_and_fifo(self):
        self.lock.unlink()
        self.lock.symlink_to(ROOT / "core.lock.json")
        self.assertEqual(self.cli("verify").returncode, 1)
        self.lock.unlink()
        os.mkfifo(self.lock, 0o600)
        self.assertEqual(self.cli("verify").returncode, 1)

    def test_oversized_file(self):
        (self.snapshot / "README.md").write_bytes(b"x" * (1024 * 1024 + 1))
        with self.assertRaisesRegex(core.SnapshotError, "size limit"):
            core.verify(self.lock, self.snapshot)

    def test_parent_traversal_in_root(self):
        with self.assertRaises(core.SnapshotError):
            core.verify(self.lock, self.snapshot / ".." / "snapshot")

    def test_cli_output_and_usage(self):
        result = self.cli("verify")
        self.assertEqual(result.returncode, 0)
        receipt = json.loads(result.stdout)
        self.assertFalse(receipt["runtime_qualified"])
        self.assertFalse(receipt["delivery_ready"])
        self.assertEqual(self.cli("stage").returncode, 2)
        self.assertEqual(self.cli("verify", "--destination", str(self.destination)).returncode, 2)

    def test_cli_stage(self):
        result = self.cli("stage", "--destination", str(self.destination))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "staged")
        self.assertEqual(core.verify(self.lock, self.destination)[0]["verified_files"], 11)


class ReferenceTests(unittest.TestCase):
    def check_links(self, files):
        return core.validate_references({name: text.encode() for name, text in files.items()})

    def test_relative_html_reference_and_heading_fragments(self):
        self.assertEqual(self.check_links({
            "README.md": '[one](docs/a.md#標題-1)\n<a href="LICENSE">license</a>\n[x]: docs/a.md#anchor\n',
            "docs/a.md": '# 標題\n# 標題\n<a id="anchor"></a>\n[back](../README.md)\n',
            "LICENSE": "MIT",
        }), 4)

    def test_missing_and_escaping_references(self):
        for link in ["missing.md", "../secret", "%2e%2e/secret", "/etc/file",
                     "x%0ay", "README.md#missing", "README.md?query", "javascript:alert"]:
            with self.subTest(link=link), self.assertRaises(core.SnapshotError):
                self.check_links({"README.md": f"[bad]({link})"})

    def test_fenced_examples_are_not_references(self):
        self.assertEqual(self.check_links({
            "README.md": '# Title\n```text\n[example](missing.md)\n```\n[ok](#title)\n',
        }), 1)

    def test_external_links_are_not_fetched(self):
        self.assertEqual(self.check_links({
            "README.md": "[external](https://example.invalid/no-network)\n",
        }), 0)


if __name__ == "__main__":
    unittest.main()
