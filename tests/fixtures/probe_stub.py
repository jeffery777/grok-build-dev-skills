"""Harmless fixed process cases. No network, credentials, shell or runtime CLI."""
import json
import os
from pathlib import Path
import signal
import sys
import time

case = sys.argv[1]
if case == "identity":
    data = sys.stdin.buffer.read()
    rows = [json.loads(line) for line in Path("evidence/journal.jsonl").read_bytes().splitlines()]
    spawned = next(row for row in rows if row["event"] == "spawned")
    assert spawned["pid"] == os.getpid() == spawned["observed_pgid"]
    assert rows[0]["identity"] == spawned["identity"]
    os.write(1, b"identity-before-input:" + data)
elif case == "normal":
    os.write(1, b"normal\x00\xff\n")
    os.write(2, b"stderr\n")
elif case == "nonzero":
    os.write(2, b"fixture-failure\n")
    raise SystemExit(7)
elif case == "flood":
    for _ in range(256):
        os.write(1, b"x" * 1024)
        os.write(2, b"y" * 1024)
elif case in {"sleep", "ignore", "closed-input", "no-read"}:
    if case == "ignore":
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    if case == "closed-input":
        os.close(0)
    os.write(1, b"started\n")
    os.write(2, b"partial-before-stop\n")
    time.sleep(4)  # A test failure still cannot leave this fixture alive indefinitely.
else:
    raise SystemExit("unknown harmless fixture")
