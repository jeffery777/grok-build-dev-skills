"""Fixed initialize-shaped fixture policy; no CLI, session or model operations."""
from __future__ import annotations

import json

REQUEST = (b'{"jsonrpc":"2.0","id":1,"method":"initialize",'
           b'"params":{"protocolVersion":1,"clientCapabilities":{}}}\n')
PROJECTION = b'{"id":1,"jsonrpc":"2.0","result":{"protocolVersion":1}}\n'
MAX_BYTES = 8192
MAX_DEPTH = 32


class _DuplicateKey(ValueError):
    pass


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey()
        result[key] = value
    return result


def _nonfinite(_):
    raise ValueError()


def _check_depth(item):
    pending = [(item, 1)]
    while pending:
        value, depth = pending.pop()
        if isinstance(value, (dict, list)):
            if depth > MAX_DEPTH:
                raise ValueError()
            children = value.values() if isinstance(value, dict) else value
            pending.extend((child, depth + 1) for child in children)


class InitializeExchange:
    """Consume bounded private bytes; return only a fixed constant projection."""

    def __init__(self):
        self._pending = bytearray()
        self._received = {"stdout": 0, "stderr": 0}
        self._observed = False
        self.reason = "pending"

    @property
    def done(self):
        return self.reason != "pending"

    @property
    def accepted(self):
        return self.reason == "response"

    def _reject(self, reason):
        if self.reason in {"pending", "response"}:
            self.reason = reason
        self._pending.clear()

    def feed(self, stream: str, raw: bytes) -> bytes:
        if stream not in self._received or not isinstance(raw, bytes):
            raise ValueError("invalid fixture stream")
        self._received[stream] += len(raw)
        if self._received[stream] > MAX_BYTES:
            self._reject("oversized")
            return b""
        if stream == "stderr":
            if raw:
                self._reject("stderr")
            return b""
        if self.reason == "response":
            if raw.strip(b" \t\r\n"):
                self._reject("extra_message")
            return b""
        if self.done:
            return b""
        self._pending.extend(raw)
        if b"\n" not in self._pending:
            return b""
        line, _, tail = self._pending.partition(b"\n")
        self._pending.clear()
        if tail.strip(b" \t\r\n"):
            self._reject("extra_message")
            return b""
        try:
            item = json.loads(line.decode("utf-8"), object_pairs_hook=_object,
                              parse_constant=_nonfinite)
            _check_depth(item)
        except _DuplicateKey:
            self._reject("duplicate_key")
            return b""
        except (ValueError, UnicodeError, RecursionError):
            self._reject("malformed")
            return b""
        if not isinstance(item, dict) or item.get("jsonrpc") != "2.0":
            self._reject("envelope")
        elif "method" in item:
            self._reject("server_request")
        elif "error" in item:
            self._reject("error_response")
        elif type(item.get("id")) is not int or item["id"] != 1:
            self._reject("response_id")
        elif not isinstance(item.get("result"), dict):
            self._reject("result_shape")
        elif (type(item["result"].get("protocolVersion")) is not int
              or item["result"]["protocolVersion"] != 1):
            self._reject("protocol_version")
        else:
            self.reason = "response"
            self._observed = True
            return PROJECTION
        return b""

    def eof(self, stream: str):
        if stream == "stdout" and not self.done:
            self._reject("premature_eof")

    def observation(self) -> dict:
        # No peer key, string, error message, auth method or capability is copied.
        return {"reason": self.reason, "response_observed": self._observed,
                "response_id": 1 if self._observed else None,
                "protocol_version": 1 if self._observed else None,
                "stdout_bytes_received": self._received["stdout"],
                "stderr_bytes_received": self._received["stderr"]}
