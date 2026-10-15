"""Fixed harmless peers only. No Grok, network, credentials, shell or RPC client."""
import json
import os
from pathlib import Path
import select
import signal
import sys
import time

case = sys.argv[1]
evidence = Path(sys.argv[2])
request = sys.stdin.buffer.readline(4097)
assert request == (b'{"jsonrpc":"2.0","id":1,"method":"initialize",'
                   b'"params":{"protocolVersion":1,"clientCapabilities":{}}}\n')
rows = [json.loads(line) for line in (evidence / "journal.jsonl").read_bytes().splitlines()]
assert rows[1]["event"] == "spawned"
assert rows[1]["pid"] == os.getpid() == rows[1]["observed_pgid"]
assert not select.select([sys.stdin], [], [], 0.03)[0], "stdin closed or extra request"
secret = "FICTIONAL_SECRET_MARKER_GC2"
response = json.dumps({"jsonrpc": "2.0", "id": 1,
                      "result": {"protocolVersion": 1, "authMethods": [secret],
                                 "agentInfo": {"name": secret}}, "unknown": secret}).encode() + b"\n"
if case == "ignore_term":
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
elif case == "nonzero":
    signal.signal(signal.SIGTERM, lambda _sig, _frame: os._exit(7))
elif case in {"late_stderr", "late_frame"}:
    def late(_sig, _frame):
        if case == "late_stderr":
            os.write(2, secret.encode())
        else:
            os.write(1, b'{"method":"unexpected","params":{"text":"' + secret.encode() + b'"}}\n')
        raise SystemExit(0)
    signal.signal(signal.SIGTERM, late)

if case == "fragmented":
    for part in (response[:7], response[7:-1], response[-1:]):
        os.write(1, part)
        time.sleep(0.01)
elif case in {"normal", "ignore_term", "late_stderr", "late_frame"}:
    os.write(1, response)
elif case == "extra":
    os.write(1, response + response)
elif case == "stderr":
    os.write(2, secret.encode())
elif case == "partial":
    os.write(1, response[:-1])
    raise SystemExit(0)
elif case == "oversized":
    os.write(1, b"x" * 8193)
elif case == "wrong_id":
    os.write(1, b'{"jsonrpc":"2.0","id":2,"result":{"protocolVersion":1}}\n')
elif case == "timeout":
    pass
elif case == "exit_zero":
    os.write(1, response)
    raise SystemExit(0)
elif case == "nonzero":
    os.write(1, response)
    os._exit(7)
else:
    raise SystemExit("unknown harmless fixture")
time.sleep(4)  # Self-expire even if the controller fails; tests reap exact own children.
