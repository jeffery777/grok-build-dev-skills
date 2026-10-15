"""Developer-only bounded POSIX probe mechanics. No CLI or runtime integration."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import time
import uuid

import core_snapshot as core
from initialize_exchange import InitializeExchange, PROJECTION, REQUEST


def _write(fd: int, raw: bytes) -> None:
    while raw:
        count = os.write(fd, raw)
        if count == 0:
            raise OSError("zero-length evidence write")
        raw = raw[count:]
    os.fsync(fd)


class _Evidence:
    """New private directory and sequential journal; never adopts old evidence."""

    def __init__(self, path: Path):
        self.fds = {}
        self.directory = None
        parent = core.open_directory(path.parent)
        try:
            os.mkdir(path.name, 0o700, dir_fd=parent)
            self.directory = os.open(path.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                     dir_fd=parent)
            for name in ("journal.jsonl", "stdout.bin", "stderr.bin"):
                self.fds[name] = self.create(name)
            os.fsync(self.directory)
            os.fsync(parent)
        except BaseException:
            self.close()
            raise
        finally:
            os.close(parent)

    def create(self, name: str) -> int:
        return os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                       0o600, dir_fd=self.directory)

    def event(self, event: str, **fields) -> None:
        raw = json.dumps({"event": event, **fields}, sort_keys=True).encode() + b"\n"
        _write(self.fds["journal.jsonl"], raw)

    def receipt(self, value: dict) -> None:
        fd = self.create("receipt.json")
        try:
            _write(fd, json.dumps(value, sort_keys=True).encode() + b"\n")
            os.fsync(self.directory)
        finally:
            os.close(fd)

    def close(self) -> None:
        for fd in self.fds.values():
            os.close(fd)
        self.fds.clear()
        if self.directory is not None:
            os.close(self.directory)
            self.directory = None


def run_probe(*, argv: list[str], cwd: Path, evidence: Path, identity: dict,
              env: dict[str, str], input_data: bytes = b"", budget: float = 2.0,
              output_limit: int = 65536, initialize_only: bool = False) -> dict:
    """Run one caller-authorized harmless probe; no retry, recovery or approval.

    Only the direct child and its still-owned process group may be controlled.
    Callers must inspect status, errors, input/output completeness and child exit.
    No result establishes sandboxing or termination of escaped descendants.
    """
    start = time.monotonic()
    started_at = datetime.now(timezone.utc).isoformat()
    if os.name != "posix":
        raise ValueError("POSIX is required")
    if (not isinstance(argv, list) or not 1 <= len(argv) <= 32
            or any(not isinstance(a, str) or not a or len(a) > 1024 or "\0" in a for a in argv)
            or not Path(argv[0]).is_absolute()):
        raise ValueError("bounded argv with an absolute executable is required")
    if (not isinstance(identity, dict) or set(identity) != {"request_id", "revision", "action"}
            or any(not isinstance(v, str) or not re.fullmatch(r"[A-Za-z0-9._/-]{1,128}", v)
                   for v in identity.values())
            or not re.fullmatch(r"[0-9a-f]{40}", identity["revision"])):
        raise ValueError("bound request/revision/action identity is required")
    if (not isinstance(env, dict) or len(env) > 64
            or any(not isinstance(k, str) or not isinstance(v, str) or not k or "=" in k
                   or "\0" in k + v or len(k) + len(v) > 4096 for k, v in env.items())):
        raise ValueError("an explicit bounded environment is required")
    if (type(budget) not in (int, float) or not math.isfinite(budget) or not 0.5 <= budget <= 30
            or type(output_limit) is not int or not 1 <= output_limit <= 262144
            or not isinstance(input_data, bytes) or len(input_data) > 4096):
        raise ValueError("invalid time/input/output limit")
    if type(initialize_only) is not bool or (initialize_only and input_data):
        raise ValueError("initialize mode requires no caller-supplied input")
    exchange = InitializeExchange() if initialize_only else None
    if exchange is not None:
        input_data = REQUEST
    cwd, evidence = core.absolute_path(Path(cwd)), core.absolute_path(Path(evidence))
    roots = (Path(os.path.realpath("/tmp")), Path(os.path.realpath("/var/tmp")))
    if not any(evidence.is_relative_to(root) and evidence != root for root in roots):
        raise ValueError("evidence must be a new directory below a system temporary root")
    cwd_fd = core.open_directory(cwd)
    os.close(cwd_fd)
    store = _Evidence(evidence)
    deadline = start + budget
    reserve = min(0.4, budget / 2)
    action_deadline = deadline - reserve
    result = {
        "format": "bounded-probe-observation/v1", "attempt_id": str(uuid.uuid4()),
        "identity": dict(identity), "cwd": str(cwd), "controller_uid": os.getuid(),
        "started_at": started_at, "budget_seconds": budget,
        "pid": None, "expected_pgid": None, "observed_pgid": None, "returncode": None,
        "status": "BLOCKED", "reason": "not_started", "errors": [], "signals": [],
        "stdin_bytes_sent": 0, "stdout_bytes_stored": 0, "stderr_bytes_stored": 0,
        "stdout_bytes_reserved": 0, "stderr_bytes_reserved": 0,
        "output_persistence_uncertain": False,
        "output_truncated": False, "streams_eof": False, "identity_persisted": False,
        "direct_child_reaped": False, "descendant_stop": "NOT_VERIFIED",
        "runtime_qualified": False, "skill_loading_qualified": False,
        "delegation_qualified": False, "delivery_ready": False,
    }
    if exchange is not None:
        result["initialize_exchange"] = exchange.observation()
    proc = None
    selector = selectors.DefaultSelector()
    signal_failed = False

    def error(stage, exception):
        result["errors"].append({"stage": stage, "type": type(exception).__name__,
                                 "errno": getattr(exception, "errno", None)})

    def event(name, **fields):
        try:
            store.event(name, **{"elapsed": time.monotonic() - start, **fields})
            return True
        except OSError as exception:
            error("journal_" + name, exception)
            return False

    def unregister(pipe, close=True):
        try:
            selector.unregister(pipe)
        except KeyError:
            pass
        if close:
            pipe.close()

    def persist_output(name, raw):
        field = name + "_bytes_stored"
        quota = name + "_bytes_reserved"
        retained = raw[:max(0, output_limit - result[quota])]
        if len(retained) != len(raw):
            result["output_truncated"] = True
        if retained:
            # A partial write or later fsync error must never release quota.
            result[quota] += len(retained)
            try:
                _write(store.fds[name + ".bin"], retained)
            except (Exception, KeyboardInterrupt):
                result[field] = None
                result["output_persistence_uncertain"] = True
                raise
            if result[field] is not None:
                result[field] += len(retained)

    def pump(timeout):
        # One small read per ready stream prevents a noisy stream starving its peer.
        for key, _ in selector.select(max(0, timeout)):
            pipe, name = key.fileobj, key.data
            if name == "stdin":
                count = os.write(pipe.fileno(), input_data[result["stdin_bytes_sent"]:])
                result["stdin_bytes_sent"] += count
                if result["stdin_bytes_sent"] == len(input_data):
                    unregister(pipe, close=exchange is None)
                continue
            raw = os.read(pipe.fileno(), 8192)
            if not raw:
                if exchange is not None:
                    exchange.eof(name)
                    result["initialize_exchange"] = exchange.observation()
                unregister(pipe)
                continue
            if exchange is not None:
                # The parser survives through cleanup. Never persist these raw bytes.
                exchange.feed(name, raw)
                result["initialize_exchange"] = exchange.observation()
            else:
                persist_output(name, raw)

    def send(sig):
        nonlocal signal_failed
        # poll may reap the child. Never signal its numerical PID/PGID afterwards.
        if proc.poll() is not None:
            return
        item = {"signal": signal.Signals(sig).name, "target_pgid": proc.pid,
                "elapsed": time.monotonic() - start}
        result["signals"].append(item)
        event("signal_intent", **item)
        try:
            if os.getpgid(proc.pid) != proc.pid:
                raise OSError("owned process group changed")
            os.killpg(proc.pid, sig)
            item["outcome"] = "sent"
        except OSError as exception:
            item.update(outcome="unconfirmed", errno=exception.errno,
                        error_type=type(exception).__name__)
            error("signal", exception)
            signal_failed = True  # Denied/uncertain signal is never retried or escalated.
        event("signal_result", **item)

    drain_failed = False

    def drain(timeout):
        nonlocal drain_failed
        if drain_failed:
            time.sleep(max(0, timeout))
            return
        try:
            pump(timeout)
        except (Exception, KeyboardInterrupt) as exception:
            error("drain", exception)
            drain_failed = True

    try:
        # This durable intent survives failure between spawn and the PID event.
        store.event("launch_intent", **result, argv=argv, environment_keys=sorted(env),
                    input_sha256=hashlib.sha256(input_data).hexdigest())
        if time.monotonic() >= action_deadline:
            result["reason"] = "budget_before_spawn"
        else:
            result["reason"] = "spawn_attempted"
            proc = subprocess.Popen(argv, cwd=cwd, env=env, shell=False, close_fds=True,
                                    start_new_session=True, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result.update(pid=proc.pid, expected_pgid=proc.pid)
            try:
                result["observed_pgid"] = os.getpgid(proc.pid)
            except OSError as exception:
                error("group_observation", exception)
            result["identity_persisted"] = event("spawned", pid=proc.pid,
                expected_pgid=proc.pid, observed_pgid=result["observed_pgid"],
                controller_uid=result["controller_uid"], cwd=str(cwd), identity=identity)
            for name in ("stdout", "stderr"):
                pipe = getattr(proc, name)
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ, name)
            if not result["identity_persisted"] or result["observed_pgid"] != proc.pid:
                result["reason"] = "identity_unconfirmed"
            else:
                if input_data:
                    os.set_blocking(proc.stdin.fileno(), False)
                    selector.register(proc.stdin, selectors.EVENT_WRITE, "stdin")
                else:
                    proc.stdin.close()
                result["reason"] = "running"
                while time.monotonic() < action_deadline:
                    pump(min(0.02, action_deadline - time.monotonic()))
                    if exchange is not None and exchange.done:
                        result["reason"] = ("initialize_response" if exchange.accepted
                                            else "initialize_rejected")
                        break
                    if result["output_truncated"]:
                        result["reason"] = "output_limit"
                        break
                    if proc.poll() is not None:
                        result["reason"] = "exited"
                        break
                if result["reason"] == "running":
                    result["reason"] = "timeout"
    except (Exception, KeyboardInterrupt) as exception:
        error("run", exception)
        result["reason"] = "controller_error"
    finally:
        if exchange is not None:
            event("initialize_observation", observation=exchange.observation())
        if proc is not None:
            try:
                if not proc.stdin.closed:
                    unregister(proc.stdin)
                if proc.poll() is None:
                    send(signal.SIGTERM)
                    term_deadline = min(deadline - reserve / 4, time.monotonic() + reserve / 2)
                    while proc.poll() is None and time.monotonic() < term_deadline:
                        drain(min(0.01, term_deadline - time.monotonic()))
                    if proc.poll() is None and not signal_failed and time.monotonic() < deadline - reserve / 4:
                        send(signal.SIGKILL)
                while time.monotonic() < deadline - reserve / 4:
                    drain(min(0.01, deadline - reserve / 4 - time.monotonic()))
                    if proc.poll() is not None and not selector.get_map():
                        break
                result["returncode"] = proc.poll()
                result["direct_child_reaped"] = proc.returncode is not None
                result["streams_eof"] = not selector.get_map()
            except (Exception, KeyboardInterrupt) as exception:
                error("cleanup", exception)
            finally:
                # Close only our descriptors, even when signaling or draining failed.
                for pipe in (proc.stdin, proc.stdout, proc.stderr):
                    try:
                        if not pipe.closed:
                            pipe.close()
                    except OSError as exception:
                        error("close_pipe", exception)
        try:
            selector.close()
        except OSError as exception:
            error("close_selector", exception)
        initialize_complete = False
        if exchange is not None:
            result["initialize_exchange"] = exchange.observation()
            if exchange.done and not exchange.accepted:
                result["reason"] = "initialize_rejected"
            elif exchange.accepted and result["reason"] == "exited":
                result["reason"] = "initialize_response"
            initialize_complete = (exchange.accepted and result["reason"] == "initialize_response"
                    and result["identity_persisted"]
                    and result["direct_child_reaped"] and result["streams_eof"]
                    and not result["errors"]
                    and result["stdin_bytes_sent"] == len(input_data)
                    and (result["returncode"] == 0 or (result["returncode"] == -signal.SIGTERM
                         and any(s.get("signal") == "SIGTERM" and s.get("outcome") == "sent"
                                 for s in result["signals"]))))
            if initialize_complete:
                try:
                    persist_output("stdout", PROJECTION)
                except (Exception, KeyboardInterrupt) as exception:
                    error("projection", exception)
        result["cleanup_elapsed_seconds"] = time.monotonic() - start
        result["ended_at"] = datetime.now(timezone.utc).isoformat()
        result["cleanup_deadline_met"] = result["cleanup_elapsed_seconds"] <= budget
        if (exchange is None and result["reason"] == "exited" and result["returncode"] == 0
                and result["identity_persisted"] and result["direct_child_reaped"]
                and result["streams_eof"] and not result["errors"]
                and not result["output_truncated"] and result["cleanup_deadline_met"]
                and result["stdin_bytes_sent"] == len(input_data)):
            result["status"] = "COMPLETE_DIRECT_CHILD_ONLY"
        if (initialize_complete and not result["errors"]
                and not result["output_truncated"] and result["cleanup_deadline_met"]
                and result["stdin_bytes_sent"] == len(input_data)):
            result["status"] = "COMPLETE_INITIALIZE_DIRECT_CHILD_ONLY"
        event("finished", result=result)
        if result["errors"]:
            result["status"] = "BLOCKED"
        try:
            store.receipt(result)
        except OSError as exception:
            error("receipt", exception)
            result["status"] = "BLOCKED"
            event("receipt_failed", errors=result["errors"])
        finally:
            try:
                store.close()
            except OSError as exception:
                error("close_evidence", exception)
                result["status"] = "BLOCKED"
    # Persistence itself can block in the kernel. This final measurement belongs
    # to the returned observation; the on-disk receipt measures through cleanup.
    result["elapsed_seconds"] = time.monotonic() - start
    result["deadline_met"] = result["elapsed_seconds"] <= budget
    if not result["deadline_met"]:
        result["status"] = "BLOCKED"
    return result
