"""Our entry selection/receipt tests use a stub SDK, never GitNexus or a model."""
from contextlib import contextmanager
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import gitnexus_index as entry


class EntryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ggn1-entry-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.profile = self.root / "accepted.json"
        self.data = {name: "fixture-only" for name in entry.PROFILE_KEYS}
        self.data["expected_coverage_paths"] = ["README.md"]
        self.profile.write_text(json.dumps(self.data))
        self.profile.chmod(0o600)
        self.digest = hashlib.sha256(self.profile.read_bytes()).hexdigest()
        self.head = "a" * 40
        self.calls = []
        self.metadata = SimpleNamespace(state="stale", reason="fixture-stale",
            indexed_revision="b" * 40, metadata_digest="c" * 64)
        self.repo = SimpleNamespace(root=self.root, head=self.head, branch="topic",
            identity={"repository_identity_digest": "d" * 64})
        self.receipt = {"fixture_only": True, "status": "refreshed",
            "authority_invariants": {"mutation_authorized": False}}
        self.outcome = SimpleNamespace(status="refreshed", reason="fixture-only", receipt=self.receipt)
        case = self
        class Controller:
            def __init__(self, qualification, **kwargs):
                case.calls.append(("controller", qualification, kwargs))
            def refresh(self, repository, **kwargs):
                case.calls.append(("refresh", repository, kwargs))
                if isinstance(case.outcome, BaseException):
                    raise case.outcome
                return case.outcome
        def collect(root, **kwargs):
            self.calls.append(("repository", root, kwargs))
            return self.repo
        def qualify(**kwargs):
            self.calls.append(("qualification", kwargs))
            return "accepted-profile-fixture"
        self.sdk = SimpleNamespace(collect_repository_state=collect,
            qualify_local_1612=qualify,
            collect_tracked_snapshot=lambda *a, **k: "snapshot-fixture",
            assess_metadata=lambda *a, **k: self.metadata,
            RefreshController=Controller)

    def args(self, action="inspect", extra=()):
        return entry.parser().parse_args([action, "--root", str(self.root),
            "--repository-id", "fixture.repo", "--expected-remote", "https://example.invalid/fixture.git",
            "--expected-head", self.head, "--expected-branch", "topic",
            "--profile", str(self.profile), "--expected-profile-sha256", self.digest,
            "--request-id", "fixture-request", *extra])

    def refresh_args(self):
        return self.args("refresh", ["--role", "execution", "--assigned-writer", "grok",
            "--confirm-refresh", "--isolated-home", str(self.root / "private-home")])

    def test_observation_and_plan_do_not_construct_controller(self):
        for action in ("inspect", "plan"):
            result = entry.operate(self.args(action), self.sdk)
            self.assertEqual(result["status"], "observed" if action == "inspect" else "plan_only")
            self.assertFalse(result["authority_granted"])
            self.assertEqual(result["metadata"]["state"], "stale")
        self.assertFalse(any(c[0] == "controller" for c in self.calls))

    def test_missing_assignment_reviewer_and_codex_assignment_stop(self):
        for edit in ({"assigned_writer": None}, {"assigned_writer": "codex"},
                     {"role": "review"}, {"confirm_refresh": False}, {"isolated_home": None}):
            args = self.refresh_args()
            for k, v in edit.items(): setattr(args, k, v)
            with self.assertRaises(entry.UseError): entry.operate(args, self.sdk)
        self.assertEqual(self.calls, [])

    def test_wrong_target_stops_before_profile_qualification(self):
        for field, wrong in [("head", "b" * 40), ("branch", "other"), ("root", self.root / "other")]:
            with patch.object(self.repo, field, wrong):
                with self.assertRaises(entry.UseError): entry.operate(self.args(), self.sdk)
        self.assertFalse(any(c[0] in {"qualification", "controller"} for c in self.calls))

    def test_profile_is_externally_pinned_and_unknown_override_rejected(self):
        self.profile.write_text(json.dumps({**self.data, "runner": "forbidden"}))
        with self.assertRaises(entry.UseError): entry.operate(self.args(), self.sdk)
        args = self.args()
        args.expected_profile_sha256 = hashlib.sha256(self.profile.read_bytes()).hexdigest()
        with self.assertRaises(entry.package.core.SnapshotError): entry.operate(args, self.sdk)
        self.assertFalse(any(c[0] == "qualification" for c in self.calls))

    def test_profile_coverage_and_receipts_forwarded_without_probe(self):
        entry.operate(self.args(), self.sdk)
        forwarded = next(c[1] for c in self.calls if c[0] == "qualification")
        self.assertEqual(forwarded["expected_coverage_paths"], ["README.md"])
        self.assertEqual(forwarded["version_output"], "fixture-only")
        self.assertNotIn("runner", forwarded)

    def test_only_shared_controller_default_lock_and_direct_refresh_used(self):
        result = entry.operate(self.refresh_args(), self.sdk)
        self.assertIs(result["controller_receipt"], self.receipt)
        controller = next(c for c in self.calls if c[0] == "controller")
        self.assertEqual(set(controller[2]), {"enabled", "timeout_seconds", "gitnexus_home"})
        call = next(c for c in self.calls if c[0] == "refresh")
        self.assertTrue(call[2]["explicit_opt_in"])
        self.assertEqual(call[2]["expected_head"], self.head)
        self.assertEqual(len([c for c in self.calls if c[0] == "refresh"]), 1)

    def test_fresh_noop_and_invalid_metadata_never_refresh(self):
        for state, status in [("fresh", "not_run"), ("partial", "blocked"),
                              ("unknown", "blocked"), ("incompatible", "blocked")]:
            self.metadata.state = state
            result = entry.operate(self.refresh_args(), self.sdk)
            self.assertEqual(result["status"], status)
        self.assertFalse(any(c[0] == "controller" for c in self.calls))

    def test_failed_receipt_preserved_and_never_retried(self):
        self.outcome = SimpleNamespace(status="failed", reason="fixture-timeout", receipt=self.receipt)
        result = entry.operate(self.refresh_args(), self.sdk)
        self.assertEqual(result["status"], "failed")
        self.assertIs(result["controller_receipt"], self.receipt)
        self.assertTrue(result["manual_reconciliation_required"])
        self.assertEqual(len([c for c in self.calls if c[0] == "refresh"]), 1)

    def test_unknown_and_cancelled_controller_effects_require_reconciliation(self):
        for error in (RuntimeError("private-path-must-not-escape"), KeyboardInterrupt()):
            self.outcome = error
            with self.assertRaises(entry.UncertainRefresh): entry.operate(self.refresh_args(), self.sdk)
        self.assertEqual(len([c for c in self.calls if c[0] == "refresh"]), 2)

    def test_cli_unknown_exit_and_error_redaction(self):
        @contextmanager
        def sdk_context(): yield self.sdk
        self.outcome = RuntimeError("private-path-must-not-escape")
        args = self.refresh_args()
        with patch.object(entry, "verified_controller", sdk_context):
            argv = ["refresh", "--root", str(args.root), "--repository-id", args.repository_id,
                "--expected-remote", args.expected_remote, "--expected-head", args.expected_head,
                "--expected-branch", args.expected_branch, "--profile", str(args.profile),
                "--expected-profile-sha256", args.expected_profile_sha256,
                "--request-id", args.request_id, "--role", "execution", "--assigned-writer", "grok",
                "--confirm-refresh", "--isolated-home", str(args.isolated_home)]
            output = io.StringIO()
            with patch("sys.stdout", output): code = entry.main(argv)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["status"], "unknown")
        self.assertEqual(json.loads(output.getvalue())["root"], str(self.root))
        self.assertEqual(json.loads(output.getvalue())["head"], self.head)
        self.assertNotIn("private-path", output.getvalue())

    def test_actual_verified_modules_load_without_process_or_namespace_leak(self):
        names = ("git_source", "memory_contract", "gitnexus_adapter")
        for name in names: self.assertNotIn(name, sys.modules)
        with patch("subprocess.Popen", side_effect=AssertionError("no process allowed")):
            with entry.verified_controller() as sdk:
                self.assertTrue(callable(sdk.qualify_local_1612))
                self.assertTrue(callable(sdk.RefreshController.refresh))
        for name in names: self.assertNotIn(name, sys.modules)

    def test_existing_dependency_is_not_silently_adopted(self):
        with patch.dict(sys.modules, {"git_source": SimpleNamespace(untrusted=True)}):
            with self.assertRaises(entry.UseError):
                with entry.verified_controller(): pass


if __name__ == "__main__":
    unittest.main()
