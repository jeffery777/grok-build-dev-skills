"""Offline package/evidence tests; no Grok, model, network or installation."""
import copy
import hashlib
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
sys.path.insert(0, str(ROOT / "scripts"))
import grok_package as package


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="p3g2-tests-", dir=os.path.realpath("/tmp"))
        self.addCleanup(self.temp.cleanup)
        self.case = Path(self.temp.name).resolve()
        self.root = self.case / "source"
        for name in package.PATHS | {package.MANIFEST}:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
            target.chmod(0o644)
        self.destination = self.case / "staged"
        self.packet_path = self.case / "packet.json"
        self.packet = {
            "format": package.PACKET_FORMAT, "runtime": "grok-build",
            "documented_version": package.VERSION,
            "source": {"kind": "fixture", "sha256": "0" * 64},
            "observed_tool_names": ["spawn_subagent", "get_task_output", "wait_tasks", "kill_task"],
        }

    def write_packet(self):
        self.packet_path.write_text(json.dumps(self.packet))
        return self.packet_path.read_bytes()

    def edit_manifest(self, edit):
        path = self.root / package.MANIFEST
        data = json.loads(path.read_bytes())
        edit(data)
        path.write_text(json.dumps(data))

    def rehash(self, name):
        value = hashlib.sha256((self.root / name).read_bytes()).hexdigest()
        self.edit_manifest(lambda data: next(item for item in data["files"] if item["path"] == name).__setitem__("sha256", value))

    def cli(self, *args, script_root=ROOT, no_bytecode_env=True):
        environment = dict(os.environ)
        environment.pop("PYTHONDONTWRITEBYTECODE", None)
        if no_bytecode_env:
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(script_root / "scripts/grok_package.py"), *args,
             "--root", str(self.root)],
            capture_output=True, text=True, timeout=10, env=environment,
        )

    def assert_unqualified(self, result):
        for key in ("runtime_qualified", "skill_loading_qualified", "delegation_qualified", "delivery_ready"):
            self.assertIs(result[key], False)
        self.assertEqual({row["id"] for row in result["blocked_checks"]},
                         {"G2-R01", "G2-R02", "G2-R03", "G2-R04", "G2-R05", "G2-R06"})

    def test_source_and_staging_layouts(self):
        result, files, _ = package.verify(self.root)
        self.assertEqual(result["verified_files"], 20)
        self.assertEqual(result["local_references"], 225)
        self.assert_unqualified(result)
        self.assertEqual(set(files), package.PATHS | {package.MANIFEST})
        extra = self.root / "development-only.txt"
        extra.write_text("not packaged")
        self.assertEqual(package.verify(self.root)[0]["verified_files"], 20)
        with self.assertRaises(package.core.SnapshotError):
            package.verify(self.root, "staging")

    def test_staging_readback_and_relocation(self):
        result = package.stage(self.root, self.destination)
        self.assertEqual(result["status"], "package_staged")
        self.assert_unqualified(result)
        verified, files, _ = package.verify(self.destination, "staging")
        self.assertEqual(result["manifest_sha256"], verified["manifest_sha256"])
        for name, raw in files.items():
            self.assertEqual(raw, (self.root / name).read_bytes())
            self.assertEqual(stat.S_IMODE((self.destination / name).stat().st_mode), 0o644)
        self.assertEqual(stat.S_IMODE(self.destination.stat().st_mode), 0o700)
        # Run the relocated consumer itself, without relying on -B or its env alias.
        relocated = subprocess.run(
            [sys.executable, str(self.destination / "scripts/grok_package.py"), "verify", "--layout", "staging"],
            capture_output=True, text=True, timeout=10,
            env={key: value for key, value in os.environ.items() if key != "PYTHONDONTWRITEBYTECODE"},
        )
        self.assertEqual(relocated.returncode, 0, relocated.stderr)
        self.assert_unqualified(json.loads(relocated.stdout))
        self.assertFalse((self.destination / "scripts/__pycache__").exists())

    def test_existing_destination_is_preserved(self):
        self.destination.mkdir()
        sentinel = self.destination / "keep"
        sentinel.write_text("unchanged")
        with self.assertRaises(FileExistsError):
            package.stage(self.root, self.destination)
        self.assertEqual(sentinel.read_text(), "unchanged")
        self.assertEqual(list(self.destination.iterdir()), [sentinel])

    def test_tamper_before_any_write(self):
        (self.root / "references/grok-capabilities.md").write_text("changed")
        result = self.cli("stage", "--destination", str(self.destination))
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.destination.exists())

    def test_protected_source_destinations(self):
        for destination in (self.root / "output", ROOT / "p3g2-must-not-create"):
            with self.subTest(destination=destination), self.assertRaises(package.core.SnapshotError):
                package.stage(self.root, destination)
            self.assertFalse(destination.exists())

    def test_manifest_path_and_identity_rejections(self):
        original = (self.root / package.MANIFEST).read_bytes()
        edits = [
            lambda data: data.__setitem__("format", "unknown"),
            lambda data: data.__setitem__("core_revision", "main"),
            lambda data: data.__setitem__("runtime_qualified", True),
            lambda data: data["files"].pop(),
            lambda data: data["files"].__setitem__(1, copy.deepcopy(data["files"][0])),
        ]
        edits += [lambda data, value=value: data["files"][0].__setitem__("path", value)
                  for value in ("../secret", "/tmp/file", "a//b", "./LICENSE", "a\tb", "a\nb", "a\\b", "unknown.md")]
        for index, edit in enumerate(edits):
            with self.subTest(index=index):
                (self.root / package.MANIFEST).write_bytes(original)
                self.edit_manifest(edit)
                with self.assertRaises(package.core.SnapshotError):
                    package.verify(self.root)

    def test_mode_symlink_hardlink_and_special_sources(self):
        name = "references/grok-capabilities.md"
        path = self.root / name
        original = path.read_bytes()
        for kind in ("mode", "symlink", "hardlink", "fifo"):
            with self.subTest(kind=kind):
                if path.exists() or path.is_symlink():
                    path.unlink()
                if kind == "mode":
                    path.write_bytes(original); path.chmod(0o755)
                elif kind == "symlink":
                    path.symlink_to(ROOT / name)
                elif kind == "hardlink":
                    os.link(ROOT / name, path)
                else:
                    os.mkfifo(path, 0o644)
                result = self.cli("verify")
                self.assertEqual(result.returncode, 1)
                self.assertEqual(json.loads(result.stderr)["status"], "error")

    def test_extra_skill_and_empty_directory_are_rejected(self):
        extra = self.root / "skills/unlisted"
        extra.mkdir()
        with self.assertRaises(package.core.SnapshotError):
            package.verify(self.root)
        (extra / "SKILL.md").write_bytes((self.root / "skills/grok-review-change/SKILL.md").read_bytes())
        with self.assertRaises(package.core.SnapshotError):
            package.verify(self.root)

    def test_duplicate_skill_identity_even_with_updated_manifest(self):
        name = "skills/grok-review-change/SKILL.md"
        path = self.root / name
        path.write_bytes(path.read_bytes().replace(b"name: grok-review-change", b"name: grok-engineering-workflow"))
        self.rehash(name)
        with self.assertRaisesRegex(package.core.SnapshotError, "skill identity"):
            package.verify(self.root)

    def test_unsupported_yaml_values_are_not_treated_as_plain_descriptions(self):
        name = "skills/grok-review-change/SKILL.md"
        path = self.root / name
        original = path.read_text()
        for value in ("[not, a, scalar]", "*unknown-alias", "description # hidden comment",
                      "True      ", "False     ", "Null      ", "No        "):
            with self.subTest(value=value):
                path.write_text(original.replace(original.splitlines()[2], "description: " + value))
                self.rehash(name)
                with self.assertRaises(package.core.SnapshotError):
                    package.verify(self.root)

    def test_reference_escape_even_with_updated_manifest(self):
        name = "references/grok-capabilities.md"
        with (self.root / name).open("a") as output:
            output.write("\n[escape](../../outside.md)\n")
        self.rehash(name)
        with self.assertRaisesRegex(package.core.SnapshotError, "reference"):
            package.verify(self.root)

    def test_core_identity_cannot_be_rewritten_by_package_manifest(self):
        name = "vendor/engineering-workflow-core/contracts/workflow.md"
        (self.root / name).write_text("rewritten obligation")
        self.rehash(name)
        with self.assertRaisesRegex(package.core.SnapshotError, "digest"):
            package.verify(self.root)

    def test_catalog_rejects_readiness_and_unknown_source_claims(self):
        original = (self.root / package.CATALOG).read_bytes()
        for edit in [lambda data: data.__setitem__("runtime_verified", True),
                     lambda data: data["sources"][0].__setitem__("kind", "authenticated-runtime"),
                     lambda data: data["capabilities"][0].__setitem__("id", "codex-spawn"),
                     lambda data: data["capabilities"][0].__setitem__("source_ids", ["missing"])]:
            (self.root / package.CATALOG).write_bytes(original)
            data = json.loads(original)
            edit(data)
            (self.root / package.CATALOG).write_text(json.dumps(data))
            self.rehash(package.CATALOG)
            with self.assertRaises(package.core.SnapshotError):
                package.verify(self.root)

    def test_fixture_never_promotes_readiness(self):
        _, _, catalog = package.verify(self.root)
        report = package.capability_report(catalog, self.write_packet())
        self.assert_unqualified(report)
        self.assertFalse(report["source_digest_authenticated"])
        self.assertFalse(report["full_grok_schema_validated"])
        self.assertEqual(report["capabilities"][0]["schema_observation"], "fixture_only")

    def test_operator_report_is_not_authenticated_runtime_evidence(self):
        self.packet["source"]["kind"] = "operator_report"
        self.write_packet()
        self.packet_path.chmod(0o600)
        result = self.cli("packet", "--packet", str(self.packet_path))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assert_unqualified(report)
        self.assertEqual(report["capabilities"][0]["schema_observation"], "operator_report_unverified")

    def test_absent_native_tools_stay_unobserved(self):
        self.packet["observed_tool_names"] = []
        report = package.capability_report(package.verify(self.root)[2], self.write_packet())
        self.assertTrue(all(row["schema_observation"] == "not_supplied" for row in report["capabilities"]))
        self.assert_unqualified(report)

    def test_invalid_evidence_packets(self):
        original = copy.deepcopy(self.packet)
        edits = [
            lambda data: data.__setitem__("format", "grok-api/v1"),
            lambda data: data.__setitem__("runtime", "codex"),
            lambda data: data.__setitem__("documented_version", "latest"),
            lambda data: data.__setitem__("runtime_verified", True),
            lambda data: data.__setitem__("approval", "yes"),
            lambda data: data.__setitem__("session_id", "private"),
            lambda data: data["source"].__setitem__("kind", "runtime_verified"),
            lambda data: data["source"].__setitem__("sha256", "A" * 64),
            lambda data: data.__setitem__("observed_tool_names", ["collaboration.spawn_agent"]),
            lambda data: data.__setitem__("observed_tool_names", ["task", "task"]),
            lambda data: data.__setitem__("observed_tool_names", [{}]),
        ]
        catalog = package.verify(self.root)[2]
        for index, edit in enumerate(edits):
            with self.subTest(index=index):
                self.packet = copy.deepcopy(original)
                edit(self.packet)
                with self.assertRaises(package.core.SnapshotError):
                    package.capability_report(catalog, self.write_packet())

    def test_json_errors_are_bounded_without_tracebacks(self):
        for raw in (b"\xff", b"{", b"9" * 5000, b"[" * 50000 + b"0" + b"]" * 50000,
                    b'{"format":1,"format":2}'):
            with self.subTest(length=len(raw)):
                self.packet_path.write_bytes(raw)
                result = self.cli("packet", "--packet", str(self.packet_path))
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertEqual(json.loads(result.stderr)["status"], "error")
                self.assertNotIn(str(self.case), result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_packet_symlink_fifo_and_size_are_rejected(self):
        for kind in ("symlink", "fifo", "oversize"):
            with self.subTest(kind=kind):
                if self.packet_path.exists() or self.packet_path.is_symlink():
                    self.packet_path.unlink()
                if kind == "symlink": self.packet_path.symlink_to(self.root / package.CATALOG)
                elif kind == "fifo": os.mkfifo(self.packet_path, 0o600)
                else: self.packet_path.write_bytes(b"x" * (package.core.MAX_FILE_BYTES + 1))
                result = self.cli("packet", "--packet", str(self.packet_path))
                self.assertEqual(result.returncode, 1)
                self.assertEqual(json.loads(result.stderr)["status"], "error")

    def test_cli_actions_and_usage(self):
        for action in ("verify", "capabilities"):
            result = self.cli(action)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_unqualified(json.loads(result.stdout))
        self.assertEqual(self.cli("packet").returncode, 2)
        self.assertEqual(self.cli("stage").returncode, 2)
        self.assertEqual(self.cli("verify", "--destination", str(self.destination)).returncode, 2)
        self.assertEqual(self.cli("stage", "--destination", str(self.destination)).returncode, 0)


class SharedStagingTests(unittest.TestCase):
    def test_unsafe_generic_inventory_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory(dir=os.path.realpath("/tmp")) as folder:
            destination = Path(folder).resolve() / "output"
            for files in ({}, {"../escape": b"x"}, {"a": b"x", "a/b": b"y"}, {"a": "not bytes"}):
                with self.subTest(files=list(files)), self.assertRaises(package.core.SnapshotError):
                    package.core.stage_verified_files(files, destination, source_roots=())
                self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
