"""Developer candidate integrity and scorer tests; no Grok/model/network calls."""
import copy
import hashlib
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
import eval_core_feedback_candidate as evaluation
import grok_package as package


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="grok-core36-test-", dir="/private/tmp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        names = {
            "core.lock.json", "scripts/core_snapshot.py", "scripts/eval_core_feedback_candidate.py",
            "tests/fixtures/core-feedback-candidate.lock.json", "tests/fixtures/core-feedback-cases.json",
            *("vendor/engineering-workflow-core/" + name for name in core.FILES),
            *("tests/fixtures/core-feedback-candidate/" + name for name in evaluation.FILES),
        }
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
            target.chmod(0o644)
        self.fixture = self.root / "tests/fixtures/core-feedback-candidate"

    def inspect(self):
        with patch.object(evaluation, "ROOT", self.root):
            return evaluation.inspect(self.fixture)

    def rejected(self):
        with self.assertRaises((evaluation.EvaluationError, core.SnapshotError, OSError)):
            self.inspect()

    def observations(self):
        _, _, cases = self.inspect()
        return cases, {"candidate_revision": evaluation.REVISION,
                       "answers": [{"id": row["id"], **row["expected"]} for row in cases]}

    def test_exact_candidate_and_formal_separation(self):
        pin, documents, cases = self.inspect()
        self.assertIs(pin["accepted"], False)
        self.assertEqual(pin["revision"], evaluation.REVISION)
        self.assertEqual(len(documents), 15)
        self.assertEqual(len(cases), 9)
        ordinary, _ = core.verify(ROOT / "core.lock.json", ROOT / "vendor/engineering-workflow-core")
        self.assertEqual(ordinary["core_revision"], "7b66978a76597d09be1b55ad199a969b4ee59c0f")
        with self.assertRaises(core.SnapshotError):
            core.verify(ROOT / "core.lock.json", self.fixture)

    def test_unknown_lock_rejected_before_trusting_manifest(self):
        path = self.root / "tests/fixtures/core-feedback-candidate.lock.json"
        value = json.loads(path.read_bytes())
        value["revision"] = "0" * 40
        value["files"][0]["sha256"] = "0" * 64
        path.write_text(json.dumps(value))
        self.rejected()

    def test_missing_candidate_file(self):
        (self.fixture / "LICENSE").unlink()
        self.rejected()

    def test_unexpected_file_and_empty_directory(self):
        for extra in ("extra.md", "empty"):
            path = self.fixture / extra
            path.mkdir() if extra == "empty" else path.write_text("unexpected")
            self.rejected()
            path.rmdir() if path.is_dir() else path.unlink()

    def test_tamper_and_cases_drift(self):
        path = self.fixture / "contracts/workflow.md"
        path.write_bytes(path.read_bytes() + b"\nTampered candidate.\n")
        self.rejected()
        path.write_bytes((ROOT / "tests/fixtures/core-feedback-candidate/contracts/workflow.md").read_bytes())
        path = self.root / "tests/fixtures/core-feedback-cases.json"
        path.write_bytes(path.read_bytes() + b" ")
        self.rejected()

    def test_executable_and_unsafe_file_types(self):
        path = self.fixture / "LICENSE"
        original = path.read_bytes()
        path.chmod(0o755)
        self.rejected()
        path.unlink()
        path.symlink_to(ROOT / "LICENSE")
        self.rejected()
        path.unlink()
        os.link(self.fixture / "README.md", path)
        self.rejected()
        path.unlink()
        os.mkfifo(path, 0o644)
        self.rejected()
        path.unlink()
        path.write_bytes(original)

    def test_symlink_ancestor_rejected(self):
        real = self.root / "tests/fixtures/real-candidate"
        self.fixture.rename(real)
        self.fixture.symlink_to(real, target_is_directory=True)
        self.rejected()

    def test_baseline_corruption_not_hidden_by_insert_only(self):
        path = self.root / "vendor/engineering-workflow-core/README.md"
        path.write_bytes(b"corrupt baseline\n")
        self.rejected()

    def test_raw_preservation_positives_and_ten_negatives(self):
        before = "甲 must stay.\nKeep  two spaces.\ncafé\n".encode()
        self.assertTrue(evaluation.inserted_only(before, before))
        self.assertTrue(evaluation.inserted_only(before, b"Added complete sentence.\n" + before))
        for after in (
            before.replace("甲".encode(), b""), before.replace(b"must", b"may"),
            before.replace(b"  ", b" "), before.replace(b"\n", b"\r\n"),
            before.replace("é".encode(), "e\u0301".encode()), before[:-1],
            b"".join(reversed(before.splitlines(keepends=True))),
            before.replace(b"stay.", b"stay!"), before[1:], b"",
        ):
            with self.subTest(after=after):
                self.assertFalse(evaluation.inserted_only(before, after))

    def test_synthetic_success_only_tests_scorer(self):
        cases, observation = self.observations()
        result = evaluation.score(observation, cases)
        self.assertIs(result["passed"], True)
        self.assertIs(result["observations_scored"], True)
        for key in ("runtime_qualified", "formal_core_adopted", "merge_authorized"):
            self.assertIs(result[key], False)

    def test_failed_answer_and_bool_integer_coercion(self):
        cases, observation = self.observations()
        for value in (False, 1, "true"):
            changed = copy.deepcopy(observation)
            changed["answers"][0]["implement_now"] = value
            self.assertIs(evaluation.score(changed, cases)["passed"], False)

    def test_missing_extra_reordered_or_wrong_identity(self):
        cases, original = self.observations()
        for edit in (
            lambda value: value["answers"].pop(),
            lambda value: value["answers"].append(value["answers"][0]),
            lambda value: value["answers"].reverse(),
            lambda value: value.update(candidate_revision="0" * 40),
            lambda value: value.update(runtime_qualified=True),
            lambda value: value["answers"].__setitem__(0, "not an answer"),
        ):
            value = copy.deepcopy(original)
            edit(value)
            with self.assertRaises(evaluation.EvaluationError):
                evaluation.score(value, cases)
        value = copy.deepcopy(original)
        value["answers"][0]["authority_granted"] = True
        self.assertIs(evaluation.score(value, cases)["passed"], False)

    def test_duplicate_nonfinite_or_non_utf8_json(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'\xff', b'{} extra'):
            with self.assertRaises(evaluation.EvaluationError):
                evaluation.parse(raw)

    def test_supported_cli_prompt_has_full_contracts_without_expected(self):
        result = subprocess.run(
            [sys.executable, "-B", "scripts/eval_core_feedback_candidate.py", "--prompt"],
            cwd=self.root, capture_output=True, timeout=10, check=True,
        )
        value = json.loads(result.stdout)
        self.assertEqual(len(value["criteria"]), 4)
        for name, text in value["criteria"].items():
            self.assertEqual(text.encode(), (self.fixture / name).read_bytes())
        self.assertTrue(all(set(row) == {"id", "situation", "requested_fields"} for row in value["cases"]))
        self.assertFalse(list(self.root.rglob("__pycache__")))

    def test_cli_bad_observation_fails_without_echoing_content(self):
        path = self.root / "invalid.json"
        path.write_bytes(b'{"private-sentinel":NaN}')
        result = subprocess.run(
            [sys.executable, "-B", "scripts/eval_core_feedback_candidate.py", "--observations", str(path)],
            cwd=self.root, capture_output=True, timeout=10,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(b"private-sentinel", result.stderr)

    def test_development_payload_excluded_from_package(self):
        _, files, _ = package.verify(ROOT)
        self.assertEqual(len(files), 31)
        self.assertFalse(any("feedback" in name for name in files))
        self.assertEqual(hashlib.sha256((ROOT / "grok.package.json").read_bytes()).hexdigest(),
                         "127ec56cb5f03b1b7751ec03ce8e0a3e686d0def57d11d0415b13d1184e93d8e")


if __name__ == "__main__":
    unittest.main()
