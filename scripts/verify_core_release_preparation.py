#!/usr/bin/env python3
"""Read-only developer preparation; never select a formal Core or publish it."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import core_snapshot as core

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA256 = "ea3f0bc43d3b93a0d07bc67551de0662a6cf684187038ec21f0569f9e4a35505"
PREPARATION_SHA256 = "b585375f7a898c910fc707f727381aea98514df30448bdf9b6dbfa11f8dca379"
BASELINE_REVISION = "7b66978a76597d09be1b55ad199a969b4ee59c0f"
REVIEWED_HEAD = "cbe3efa1ecc1d2ec04d2edc7078eb22c9dbec038"


class PreparationError(core.SnapshotError):
    pass


def digest(value):
    return hashlib.sha256(value).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PreparationError("duplicate field")
        result[key] = value
    return result


def parse(raw):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(PreparationError("nonfinite JSON")))


def fixed_snapshot(root, name, expected_digest):
    parent = core.open_directory(root / "tests/fixtures")
    try:
        raw = core.read_regular(parent, name + ".lock.json", snapshot=True)
    finally:
        os.close(parent)
    if len(raw) > 32768 or digest(raw) != expected_digest:
        raise PreparationError("unreviewed preparation data")
    pin = parse(raw)
    rows = pin["files"]
    names = [row["path"] for row in rows]
    if names != sorted(set(names)):
        raise PreparationError("invalid fixed paths")
    captured = core.capture_inventory(root / "tests/fixtures" / name, frozenset(names))
    for row in rows:
        value = captured[row["path"]]
        if row["mode"] != "100644" or len(value) != row["size_bytes"] or digest(value) != row["sha256"]:
            raise PreparationError("fixed bytes or mode mismatch")
    collection = digest(b"".join(p.encode() + b"\t" + digest(v).encode() + b"\n"
                                  for p, v in sorted(captured.items())))
    if collection != pin["collection_sha256"]:
        raise PreparationError("collection mismatch")
    return pin, captured


def baseline(root=None):
    root = ROOT if root is None else Path(root)
    pin, files = fixed_snapshot(root, "core-feedback-baseline", BASELINE_SHA256)
    if pin["revision"] != BASELINE_REVISION or len(files) != 14:
        raise PreparationError("historical baseline identity")
    return files


def load_candidate(root):
    spec = importlib.util.spec_from_file_location(
        "fixed_core_development_candidate", root / "scripts/eval_core_feedback_candidate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = root
    return module


def inspect(root=None):
    root = ROOT if root is None else Path(root)
    pin, files = fixed_snapshot(root, "core-release-preparation", PREPARATION_SHA256)
    if (pin["reviewed_head"] != REVIEWED_HEAD or len(files) != 20
            or any(pin[k] is not None for k in ("publication_revision", "tag_object", "release_id"))
            or any(pin[k] is not False for k in ("formal_core_adopted", "runtime_qualified", "merge_authorized"))):
        raise PreparationError("preparation is not publication")
    old = baseline(root)
    candidate = load_candidate(root)
    _, criteria, _ = candidate.inspect(root / "tests/fixtures/core-feedback-candidate")
    for name, before in old.items():
        if not candidate.inserted_only(before, files[name]):
            raise PreparationError("baseline text removed")
    for name in (p for p in files if p.startswith("contracts/")):
        if files[name] != criteria[name].encode("utf-8"):
            raise PreparationError("evaluated contract changed")
    if files["LICENSE"] != old["LICENSE"]:
        raise PreparationError("license changed")
    markdown = b"".join(p.encode() + b"\t" + digest(v).encode() + b"\n"
                        for p, v in sorted(files.items()) if p.endswith(".md"))
    if (digest(markdown) != pin["markdown_collection_sha256"]
            or sum(map(len, files.values())) != pin["total_bytes"]):
        raise PreparationError("migration values differ from fixed bytes")
    core.validate_references(files)
    return {"status": "prepared-publication-pending", "reviewed_head": REVIEWED_HEAD,
            "files": len(files), "total_bytes": sum(map(len, files.values())),
            "publication_revision": None, "tag_object": None,
            "formal_core_adopted": False, "runtime_qualified": False, "merge_authorized": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-publication", action="store_true")
    args = parser.parse_args()
    try:
        result = inspect()
        print(json.dumps(result, sort_keys=True))
        return 1 if args.require_publication else 0
    except (core.SnapshotError, OSError, ValueError, KeyError, TypeError, RecursionError) as error:
        print("Core preparation rejected: " + type(error).__name__, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
