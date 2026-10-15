"""Bounded local stubs only; never invokes Grok or investigates other processes."""
import errno
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import probe_controller as probe


@unittest.skipUnless(os.name == "posix", "POSIX process semantics")
class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gc1-stub-", dir=os.path.realpath("/tmp"))
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.target = self.work / "evidence"
        self.children = []
        self.popen = subprocess.Popen
        self.addCleanup(self.reap_test_children)

    def reap_test_children(self):
        # Handles only exact Popen objects created by this test, never a PID lookup.
        for child in self.children:
            if child.poll() is None:
                child.kill()
            child.wait(timeout=5)

    def spawn(self, *args, **kwargs):
        child = self.popen(*args, **kwargs)
        self.children.append(child)
        self.assertIs(kwargs["shell"], False)
        self.assertIs(kwargs["start_new_session"], True)
        self.assertIs(kwargs["close_fds"], True)
        self.assertEqual(kwargs["env"], {"HOME": str(self.work), "LANG": "C"})
        return child

    def run_case(self, case="normal", **changes):
        args = dict(argv=[os.path.realpath(sys.executable), "-I", "-B",
                          str(ROOT / "tests/fixtures/probe_stub.py"), case],
                    cwd=self.work, evidence=self.target,
                    identity={"request_id": "stub-request", "revision": "a" * 40,
                              "action": "offline-controller-test"},
                    env={"HOME": str(self.work), "LANG": "C"}, budget=0.8)
        args.update(changes)
        with mock.patch.object(probe.subprocess, "Popen", side_effect=self.spawn):
            result = probe.run_probe(**args)
        for field in ("runtime_qualified", "skill_loading_qualified",
                      "delegation_qualified", "delivery_ready"):
            self.assertIs(result[field], False)
        self.assertEqual(result["descendant_stop"], "NOT_VERIFIED")
        return result

    def rows(self):
        return [json.loads(line) for line in (self.target / "journal.jsonl").read_bytes().splitlines()]

    def receipt(self):
        return json.loads((self.target / "receipt.json").read_bytes())

    def test_normal_binary_output_private_evidence_and_identity(self):
        result = self.run_case()
        self.assertEqual(result["status"], "COMPLETE_DIRECT_CHILD_ONLY")
        self.assertEqual(result["returncode"], 0)
        self.assertTrue(result["direct_child_reaped"])
        self.assertTrue(result["streams_eof"])
        self.assertEqual((self.target / "stdout.bin").read_bytes(), b"normal\x00\xff\n")
        self.assertEqual((self.target / "stderr.bin").read_bytes(), b"stderr\n")
        self.assertEqual(self.rows()[0]["event"], "launch_intent")
        self.assertEqual(self.rows()[1]["event"], "spawned")
        self.assertEqual(self.receipt()["pid"], result["pid"])
        self.assertEqual(stat.S_IMODE(self.target.stat().st_mode), 0o700)
        for path in self.target.iterdir():
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertLessEqual(result["elapsed_seconds"], 1.3)

    def test_identity_is_durable_before_any_input(self):
        result = self.run_case("identity", input_data=b"fixture-input")
        self.assertEqual(result["status"], "COMPLETE_DIRECT_CHILD_ONLY")
        self.assertEqual(result["stdin_bytes_sent"], 13)
        self.assertEqual((self.target / "stdout.bin").read_bytes(),
                         b"identity-before-input:fixture-input")

    def test_nonzero_child_is_separate_from_controller_result(self):
        result = self.run_case("nonzero")
        self.assertEqual(result["reason"], "exited")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["returncode"], 7)
        self.assertTrue(result["direct_child_reaped"])

    def test_timeout_retains_output_before_signaling(self):
        original = os.killpg

        def signal_with_readback(pgid, sig):
            self.assertEqual((self.target / "stdout.bin").read_bytes(), b"started\n")
            self.assertIn(b"partial-before-stop", (self.target / "stderr.bin").read_bytes())
            self.assertEqual(self.rows()[1]["pid"], pgid)
            original(pgid, sig)

        with mock.patch.object(probe.os, "killpg", side_effect=signal_with_readback):
            result = self.run_case("sleep")
        self.assertEqual(result["reason"], "timeout")
        self.assertEqual([s["signal"] for s in result["signals"]], ["SIGTERM"])
        self.assertEqual(result["returncode"], -signal.SIGTERM)
        self.assertTrue(result["direct_child_reaped"])
        self.assertTrue(result["deadline_met"])

    def test_term_ignored_uses_one_kill_within_original_budget(self):
        result = self.run_case("ignore")
        self.assertEqual([s["signal"] for s in result["signals"]], ["SIGTERM", "SIGKILL"])
        self.assertEqual(result["returncode"], -signal.SIGKILL)
        self.assertTrue(result["direct_child_reaped"])
        self.assertTrue(result["deadline_met"])

    def test_both_streams_are_bounded_without_line_or_utf8_assumptions(self):
        result = self.run_case("flood", output_limit=1024)
        self.assertTrue(result["output_truncated"])
        self.assertEqual(result["reason"], "output_limit")
        for name in ("stdout", "stderr"):
            self.assertLessEqual((self.target / (name + ".bin")).stat().st_size, 1024)
            self.assertGreater(result[name + "_bytes_stored"], 0)

    def test_no_read_input_remains_bounded_and_is_never_replayed(self):
        result = self.run_case("no-read", input_data=b"x" * 4096)
        self.assertEqual(result["reason"], "timeout")
        self.assertLessEqual(result["stdin_bytes_sent"], 4096)
        self.assertEqual(len(self.children), 1)
        self.assertTrue(result["direct_child_reaped"])

    def test_closed_input_does_not_erase_receipt(self):
        result = self.run_case("closed-input", input_data=b"x" * 4096)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(self.receipt()["attempt_id"], result["attempt_id"])
        self.assertEqual(len(self.children), 1)

    def test_no_signals_after_reaping_direct_child(self):
        with mock.patch.object(probe.os, "killpg") as send:
            result = self.run_case("normal")
        send.assert_not_called()
        self.assertEqual(result["signals"], [])

    def test_signal_errors_keep_evidence_and_never_escalate(self):
        for fault in (PermissionError(errno.EPERM, "fixture"),
                      ProcessLookupError(errno.ESRCH, "fixture"),
                      OSError(errno.EIO, "fixture")):
            with self.subTest(fault=type(fault).__name__):
                self.target = self.work / type(fault).__name__
                with mock.patch.object(probe.os, "killpg", side_effect=fault) as send:
                    result = self.run_case("sleep", budget=0.5)
                self.assertEqual(send.call_count, 1)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertFalse(result["direct_child_reaped"])
                self.assertEqual(self.receipt()["signals"][0]["outcome"], "unconfirmed")
                self.assertIn(b"started", (self.target / "stdout.bin").read_bytes())
                self.assertTrue(any(e["stage"] == "signal" for e in result["errors"]))

    def test_prelaunch_journal_failure_never_spawns(self):
        original = probe._Evidence.event

        def failing(store, name, **fields):
            if name == "launch_intent":
                raise OSError(errno.EIO, "fixture")
            return original(store, name, **fields)

        with mock.patch.object(probe._Evidence, "event", failing):
            result = self.run_case()
        self.assertEqual(self.children, [])
        self.assertIsNone(result["pid"])
        self.assertEqual(result["status"], "BLOCKED")

    def test_pid_event_failure_sends_no_input(self):
        original = probe._Evidence.event

        def failing(store, name, **fields):
            if name == "spawned":
                raise OSError(errno.EIO, "fixture")
            return original(store, name, **fields)

        with mock.patch.object(probe._Evidence, "event", failing):
            result = self.run_case("identity", input_data=b"must-not-send")
        self.assertFalse(result["identity_persisted"])
        self.assertEqual(result["stdin_bytes_sent"], 0)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["direct_child_reaped"])

    def test_output_failure_does_not_prevent_kill_or_final_receipt(self):
        original = probe._write

        def failing(fd, raw):
            if raw.startswith((b"started", b"partial-before-stop")):
                raise OSError(errno.EIO, "fixture")
            return original(fd, raw)

        with mock.patch.object(probe, "_write", side_effect=failing):
            result = self.run_case("ignore")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["direct_child_reaped"])
        self.assertEqual(result["signals"][-1]["signal"], "SIGKILL")
        self.assertEqual(self.receipt()["attempt_id"], result["attempt_id"])

    def test_partial_and_postwrite_failures_never_reuse_output_quota(self):
        for partial in (True, False):
            with self.subTest(partial=partial):
                self.target = self.work / ("partial" if partial else "postwrite")
                original = probe._write
                failed = False

                def failing(fd, raw):
                    nonlocal failed
                    if raw.startswith(b"x") and not failed:
                        failed = True
                        if partial:
                            os.write(fd, raw[:3])
                        else:
                            original(fd, raw)  # Error after write/fsync, before acknowledgement.
                        raise OSError(errno.EIO, "fixture")
                    return original(fd, raw)

                with mock.patch.object(probe, "_write", side_effect=failing):
                    result = self.run_case("flood", output_limit=16)
                self.assertTrue(failed)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertTrue(result["output_persistence_uncertain"])
                self.assertIsNone(result["stdout_bytes_stored"])
                self.assertEqual(result["stdout_bytes_reserved"], 16)
                self.assertEqual((self.target / "stdout.bin").stat().st_size, 3 if partial else 16)
                for name in ("stdout", "stderr"):
                    self.assertLessEqual((self.target / (name + ".bin")).stat().st_size, 16)
                    self.assertLessEqual(result[name + "_bytes_reserved"], 16)

    def test_known_truncation_survives_postwrite_failure(self):
        original = probe._write
        failed = False

        def failing(fd, raw):
            nonlocal failed
            if raw.startswith(b"normal") and not failed:
                failed = True
                original(fd, raw)
                raise OSError(errno.EIO, "fixture")
            return original(fd, raw)

        with mock.patch.object(probe, "_write", side_effect=failing):
            result = self.run_case(output_limit=8)
        self.assertTrue(failed)
        self.assertTrue(result["output_truncated"])
        self.assertTrue(self.receipt()["output_truncated"])
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["output_persistence_uncertain"])
        self.assertIsNone(result["stdout_bytes_stored"])
        self.assertEqual(result["stdout_bytes_reserved"], 8)
        self.assertEqual((self.target / "stdout.bin").stat().st_size, 8)
        self.assertTrue(result["direct_child_reaped"])

    def test_slow_evidence_setup_consumes_budget_without_spawning(self):
        original = probe._Evidence.__init__

        def slow_setup(store, path):
            time.sleep(0.65)
            original(store, path)

        with mock.patch.object(probe._Evidence, "__init__", slow_setup):
            result = self.run_case(budget=0.5)
        self.assertEqual(self.children, [])
        self.assertEqual(result["reason"], "budget_before_spawn")
        self.assertGreaterEqual(result["elapsed_seconds"], 0.65)
        self.assertFalse(result["deadline_met"])
        self.assertFalse(result["cleanup_deadline_met"])
        self.assertEqual(result["status"], "BLOCKED")

    def test_evidence_setup_fsync_failure_never_spawns(self):
        with mock.patch.object(probe.os, "fsync", side_effect=OSError(errno.EIO, "fixture")):
            with self.assertRaises(OSError):
                self.run_case()
        self.assertEqual(self.children, [])

    def test_receipt_failure_preserves_journal_and_output(self):
        with mock.patch.object(probe._Evidence, "receipt", side_effect=OSError(errno.EIO, "fixture")):
            result = self.run_case()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(self.rows()[-1]["event"], "receipt_failed")
        self.assertTrue((self.target / "stdout.bin").read_bytes().startswith(b"normal"))

    def test_spawn_failure_is_recorded_without_second_attempt(self):
        result = self.run_case(argv=["/nonexistent-gc1-fixture-executable"])
        self.assertEqual(result["reason"], "controller_error")
        self.assertIsNone(result["pid"])
        self.assertEqual(self.rows()[0]["reason"], "not_started")
        self.assertEqual(result["status"], "BLOCKED")

    def test_keyboard_interrupt_attempts_cleanup_and_receipt(self):
        original = probe.selectors.DefaultSelector.select
        calls = 0

        def interrupt_once(selector, timeout=None):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise KeyboardInterrupt()
            return original(selector, timeout)

        with mock.patch.object(probe.selectors.DefaultSelector, "select", interrupt_once):
            result = self.run_case("sleep")
        self.assertTrue(result["direct_child_reaped"])
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(self.receipt()["errors"][0]["type"], "KeyboardInterrupt")

    def test_existing_evidence_is_not_adopted_or_overwritten(self):
        self.target.mkdir()
        sentinel = self.target / "keep"
        sentinel.write_bytes(b"unchanged")
        with self.assertRaises(FileExistsError):
            self.run_case()
        self.assertEqual(sentinel.read_bytes(), b"unchanged")
        self.assertEqual(self.children, [])

    def test_symlink_ancestor_is_rejected_before_spawn(self):
        alias = self.work / "alias"
        alias.symlink_to(self.work, target_is_directory=True)
        with self.assertRaises(OSError):
            self.run_case(evidence=alias / "evidence")
        self.assertEqual(self.children, [])

    def test_invalid_id_paths_and_limits_never_spawn(self):
        cases = [dict(identity={"request_id": "x", "revision": "main", "action": "x"}),
                 dict(identity={"request_id": "x", "revision": "a" * 40}),
                 dict(argv="echo fixture"), dict(argv=["relative-program"]),
                 dict(budget=float("nan")), dict(budget=0.1), dict(budget=31),
                 dict(output_limit=True), dict(output_limit=262145),
                 dict(input_data=b"x" * 4097), dict(env=None),
                 dict(evidence=Path("/not-approved/gc1-evidence")),
                 dict(evidence=self.work / ".." / "escape")]
        for changes in cases:
            with self.subTest(changes=list(changes)):
                with self.assertRaises((ValueError, probe.core.SnapshotError)):
                    self.run_case(**changes)
        self.assertEqual(self.children, [])


if __name__ == "__main__":
    unittest.main()
