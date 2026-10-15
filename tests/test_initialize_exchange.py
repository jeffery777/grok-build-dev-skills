"""Initialize-shaped parser and owned harmless stub integration; never starts Grok."""
import errno
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from initialize_exchange import InitializeExchange, MAX_BYTES, MAX_DEPTH, PROJECTION, REQUEST
import probe_controller as probe

VALID = b'{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":1}}\n'
SECRET = b"FICTIONAL_SECRET_MARKER_GC2"


class ParserTests(unittest.TestCase):
    def test_fragmented_lf_and_fixed_projection(self):
        x = InitializeExchange()
        for part in (VALID[:3], VALID[3:-1]):
            self.assertEqual(x.feed("stdout", part), b"")
            self.assertFalse(x.done)
        self.assertEqual(x.feed("stdout", b"\n"), PROJECTION)
        self.assertTrue(x.accepted)
        self.assertEqual(x.observation()["stdout_bytes_received"], len(VALID))

    def test_unknown_fields_cannot_enter_projection_or_observation(self):
        x = InitializeExchange()
        raw = VALID[:-2] + b',"authMethods":["' + SECRET + b'"],"unknown":"' + SECRET + b'"}\n'
        self.assertEqual(x.feed("stdout", raw), PROJECTION)
        self.assertNotIn(SECRET, json.dumps(x.observation()).encode())

    def test_response_schema_types_and_presence(self):
        cases = [([], "envelope"),
                 ({"jsonrpc": "1.0"}, "envelope"),
                 ({"jsonrpc": "2.0", "id": True, "result": {}}, "response_id"),
                 ({"jsonrpc": "2.0", "id": 1.0, "result": {}}, "response_id"),
                 ({"jsonrpc": "2.0", "id": "1", "result": {}}, "response_id"),
                 ({"jsonrpc": "2.0", "id": 2, "result": {}}, "response_id"),
                 ({"jsonrpc": "2.0", "id": 1, "result": []}, "result_shape"),
                 ({"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": True}}, "protocol_version"),
                 ({"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": 1.0}}, "protocol_version"),
                 ({"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": 2}}, "protocol_version"),
                 ({"jsonrpc": "2.0", "id": 1, "result": {}}, "protocol_version"),
                 ({"jsonrpc": "2.0", "id": 1, "error": None, "result": {}}, "error_response"),
                 ({"jsonrpc": "2.0", "id": 1, "method": None, "result": {}}, "server_request")]
        for value, reason in cases:
            with self.subTest(reason=reason, value=value):
                x = InitializeExchange()
                self.assertEqual(x.feed("stdout", json.dumps(value).encode() + b"\n"), b"")
                self.assertEqual(x.reason, reason)
                self.assertFalse(x.accepted)

    def test_duplicate_nonfinite_utf8_and_malformed_values(self):
        for raw, reason in [(b'{"jsonrpc":"2.0","id":1,"id":1}\n', "duplicate_key"),
                            (b'{"x":{"k":1,"k":2}}\n', "duplicate_key"),
                            (b'{"x":NaN}\n', "malformed"),
                            (b'{"x":Infinity}\n', "malformed"),
                            (b'\xff\n', "malformed"), (b'{bad}\n', "malformed"),
                            (b'[' * 1100 + b']' * 1100 + b'\n', "malformed")]:
            with self.subTest(reason=reason):
                x = InitializeExchange()
                self.assertEqual(x.feed("stdout", raw), b"")
                self.assertEqual(x.reason, reason)

    def test_extra_frame_and_partial_tail_same_or_later_read(self):
        for tail in (VALID, b'{"method":', b'\v'):
            for together in (True, False):
                with self.subTest(together=together, tail=tail):
                    x = InitializeExchange()
                    if together:
                        self.assertEqual(x.feed("stdout", VALID + tail), b"")
                    else:
                        x.feed("stdout", VALID)
                        self.assertEqual(x.feed("stdout", tail), b"")
                    self.assertEqual(x.reason, "extra_message")

    def test_cumulative_cap_before_buffering_and_premature_eof(self):
        x = InitializeExchange()
        x.feed("stdout", b"x" * MAX_BYTES)
        self.assertFalse(x.done)
        x.feed("stdout", b"x")
        self.assertEqual(x.reason, "oversized")
        self.assertEqual(len(x._pending), 0)
        for partial in (b"", VALID[:-1]):
            x = InitializeExchange()
            x.feed("stdout", partial)
            x.eof("stdout")
            self.assertEqual(x.reason, "premature_eof")

    def test_stderr_after_response_rejects_without_returning_text(self):
        x = InitializeExchange()
        x.feed("stdout", VALID)
        self.assertEqual(x.feed("stderr", SECRET), b"")
        self.assertFalse(x.accepted)
        self.assertTrue(x.observation()["response_observed"])
        self.assertNotIn(SECRET, json.dumps(x.observation()).encode())

    def test_explicit_depth_limit_independent_of_interpreter(self):
        for depth, accepted in ((MAX_DEPTH - 1, True), (MAX_DEPTH, False)):
            raw = VALID[:-2] + b',"unknown":' + b'[' * depth + b'0' + b']' * depth + b'}\n'
            x = InitializeExchange()
            x.feed("stdout", raw)
            self.assertEqual(x.accepted, accepted)


@unittest.skipUnless(os.name == "posix", "POSIX process semantics")
class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gc2-stub-", dir=os.path.realpath("/tmp"))
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.target = self.work / "evidence"
        self.children = []
        self.popen = subprocess.Popen
        self.addCleanup(self.reap)

    def reap(self):
        for p in self.children:
            if p.poll() is None:
                p.kill()
            p.wait(timeout=5)

    def spawn(self, *args, **kwargs):
        self.assertIs(kwargs["shell"], False)
        self.assertIs(kwargs["start_new_session"], True)
        self.assertIs(kwargs["close_fds"], True)
        self.assertEqual(kwargs["env"], {"HOME": str(self.work), "LANG": "C"})
        p = self.popen(*args, **kwargs)
        self.children.append(p)
        return p

    def run_case(self, case="normal", **changes):
        args = dict(argv=[os.path.realpath(sys.executable), "-I", "-B",
                          str(ROOT / "tests/fixtures/initialize_stub.py"), case, str(self.target)],
                    cwd=self.work, evidence=self.target,
                    identity={"request_id": "gc2-stub", "revision": "a" * 40,
                              "action": "offline-initialize-test"},
                    env={"HOME": str(self.work), "LANG": "C"}, budget=0.8,
                    initialize_only=True)
        args.update(changes)
        with mock.patch.object(probe.subprocess, "Popen", side_effect=self.spawn):
            r = probe.run_probe(**args)
        for key in ("runtime_qualified", "skill_loading_qualified", "delegation_qualified", "delivery_ready"):
            self.assertIs(r[key], False)
        self.assertEqual(r["descendant_stop"], "NOT_VERIFIED")
        self.assertNotIn(SECRET, json.dumps(r).encode())
        for p in self.target.iterdir():
            self.assertNotIn(SECRET, p.read_bytes(), p.name)
        return r

    def test_normal_and_fragmented_exchange_hold_stdin_and_keep_identity(self):
        for case in ("normal", "fragmented", "exit_zero"):
            with self.subTest(case=case):
                self.target = self.work / case
                r = self.run_case(case)
                self.assertEqual(r["status"], "COMPLETE_INITIALIZE_DIRECT_CHILD_ONLY")
                self.assertEqual(r["stdin_bytes_sent"], len(REQUEST))
                self.assertTrue(r["identity_persisted"])
                self.assertTrue(r["direct_child_reaped"])
                self.assertTrue(r["streams_eof"])
                self.assertIn(r["returncode"], (0, -signal.SIGTERM))
                self.assertEqual((self.target / "stdout.bin").read_bytes(), PROJECTION)
                self.assertEqual((self.target / "stderr.bin").read_bytes(), b"")
                rows = [json.loads(x) for x in (self.target / "journal.jsonl").read_bytes().splitlines()]
                self.assertEqual(rows[1]["event"], "spawned")
                self.assertEqual(r["initialize_exchange"]["reason"], "response")

    def test_malformed_oversized_extra_and_eof_stop_without_raw_evidence(self):
        for case, reason in (("wrong_id", "response_id"), ("extra", "extra_message"),
                             ("partial", "premature_eof"), ("oversized", "oversized"),
                             ("stderr", "stderr")):
            with self.subTest(case=case):
                self.target = self.work / case
                r = self.run_case(case)
                self.assertEqual(r["status"], "BLOCKED")
                self.assertEqual(r["initialize_exchange"]["reason"], reason)
                self.assertTrue(r["direct_child_reaped"])
                self.assertEqual((self.target / "stdout.bin").read_bytes(), b"")
                self.assertEqual((self.target / "stderr.bin").read_bytes(), b"")

    def test_late_cleanup_stderr_or_message_invalidates_projection(self):
        for case in ("late_stderr", "late_frame"):
            with self.subTest(case=case):
                self.target = self.work / case
                r = self.run_case(case)
                self.assertTrue(r["initialize_exchange"]["response_observed"])
                self.assertEqual(r["status"], "BLOCKED")
                self.assertEqual((self.target / "stdout.bin").read_bytes(), b"")

    def test_timeout_nonzero_and_forced_kill_do_not_complete(self):
        for case in ("timeout", "nonzero", "ignore_term"):
            with self.subTest(case=case):
                self.target = self.work / case
                r = self.run_case(case)
                self.assertEqual(r["status"], "BLOCKED")
                self.assertTrue(r["direct_child_reaped"])
                self.assertEqual((self.target / "stdout.bin").read_bytes(), b"")
                if case == "ignore_term":
                    self.assertEqual(r["returncode"], -signal.SIGKILL)
                elif case == "nonzero":
                    self.assertEqual(r["returncode"], 7)

    def test_projection_partial_and_postwrite_failures_preserve_uncertainty(self):
        for partial in (True, False):
            self.target = self.work / ("partial" if partial else "postwrite")
            original = probe._write

            def failing(fd, raw):
                if raw == PROJECTION:
                    if partial:
                        os.write(fd, raw[:3])
                    else:
                        original(fd, raw)
                    raise OSError(errno.EIO, "fixture")
                return original(fd, raw)

            with mock.patch.object(probe, "_write", side_effect=failing):
                r = self.run_case()
            self.assertEqual(r["status"], "BLOCKED")
            self.assertIsNone(r["stdout_bytes_stored"])
            self.assertTrue(r["output_persistence_uncertain"])
            self.assertEqual(r["stdout_bytes_reserved"], len(PROJECTION))
            self.assertEqual((self.target / "stdout.bin").stat().st_size, 3 if partial else len(PROJECTION))

    def test_projection_cap_and_signal_denial_remain_blocked(self):
        r = self.run_case(output_limit=8)
        self.assertTrue(r["output_truncated"])
        self.assertEqual(r["status"], "BLOCKED")
        self.target = self.work / "denied"
        with mock.patch.object(probe.os, "killpg", side_effect=PermissionError(errno.EPERM, "fixture")) as send:
            r = self.run_case()
        self.assertEqual(send.call_count, 1)
        self.assertEqual(r["status"], "BLOCKED")
        self.assertFalse(r["direct_child_reaped"])
        self.assertEqual((self.target / "stdout.bin").read_bytes(), b"")

    def test_custom_input_or_nonboolean_mode_never_spawns(self):
        for changes in (dict(input_data=b"forbidden"), dict(initialize_only=1)):
            with self.assertRaises(ValueError):
                self.run_case(**changes)
        self.assertEqual(self.children, [])

    def test_identity_journal_failure_never_sends_initialize(self):
        original = probe._Evidence.event

        def fail_spawn(store, name, **fields):
            if name == "spawned":
                raise OSError(errno.EIO, "fixture")
            return original(store, name, **fields)

        with mock.patch.object(probe._Evidence, "event", fail_spawn):
            r = self.run_case()
        self.assertEqual(r["status"], "BLOCKED")
        self.assertFalse(r["identity_persisted"])
        self.assertEqual(r["stdin_bytes_sent"], 0)
        self.assertEqual((self.target / "stdout.bin").read_bytes(), b"")

    def test_final_receipt_failure_downgrades_valid_response(self):
        with mock.patch.object(probe._Evidence, "receipt", side_effect=OSError(errno.EIO, "fixture")):
            r = self.run_case()
        self.assertEqual(r["status"], "BLOCKED")
        self.assertTrue(r["initialize_exchange"]["response_observed"])
        self.assertTrue(any(e["stage"] == "receipt" for e in r["errors"]))


if __name__ == "__main__":
    unittest.main()
