#!/usr/bin/env python3
"""Offline, development-only evaluation of one fixed Core candidate.

This never changes the ordinary Core loader, installs files, dispatches models,
or executes content. Model observations are supplied separately and stay data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import core_snapshot as core

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/core-feedback-candidate"
REVISION = "87db5867fbed58c81e64f0c316168d537452425e"
PIN_SHA256 = "bfe8a16bd98ea518ede04ae24638a0acf817c096b84d3a32cb5d6637f9e232c8"
CASES_SHA256 = "c3322e94283f67580b56a32ba185934c1658daedd2a390e2fec950dc48d541cd"
FILES = (
    "CHANGELOG.md", "LICENSE", "README.md",
    "contracts/authorization-and-stops.md", "contracts/exact-head-and-evidence.md",
    "contracts/review-and-security.md", "contracts/workflow.md",
    "docs/architecture/dependency-inventory.md", "docs/architecture/migration-plan.md",
    "docs/architecture/project-split.md", "docs/maintenance/issue-24-26-candidate.md",
    "docs/provenance/source-map.md", "docs/provenance/upstream-notices.md",
    "docs/releases/v0.1.0.md", "docs/releases/v0.1.1.md",
)
PROTECTED = {"LICENSE", "contracts/authorization-and-stops.md",
             "contracts/exact-head-and-evidence.md", "docs/provenance/upstream-notices.md"}


class EvaluationError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise EvaluationError("duplicate JSON field")
        result[key] = value
    return result


def parse(data):
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=unique,
                          parse_constant=lambda _: (_ for _ in ()).throw(EvaluationError("nonfinite JSON")))
    except (UnicodeError, ValueError, RecursionError) as error:
        raise EvaluationError("invalid observation or pin JSON") from error


def read_file(path, limit):
    parent = core.open_directory(Path(path).parent)
    try:
        data = core.read_regular(parent, Path(path).name, snapshot=False)
    finally:
        os.close(parent)
    if not 0 < len(data) <= limit:
        raise EvaluationError("empty or excessive evaluation file")
    return data


def inserted_only(before, after):
    old, pos = before.splitlines(keepends=True), 0
    for line in after.splitlines(keepends=True):
        if pos < len(old) and line == old[pos]:
            pos += 1
    return pos == len(old)


def inspect(root=FIXTURE):
    pin_bytes = read_file(ROOT / "tests/fixtures/core-feedback-candidate.lock.json", 16384)
    if digest(pin_bytes) != PIN_SHA256:
        raise EvaluationError("unreviewed candidate pin")
    pin = parse(pin_bytes)
    if pin["revision"] != REVISION:
        raise EvaluationError("wrong candidate revision")
    captured = core.capture_inventory(root, frozenset(FILES))
    _, original_files = core.verify(ROOT / "core.lock.json", ROOT / "vendor/engineering-workflow-core")
    documents = {}
    rows = pin["files"]
    if [row["path"] for row in rows] != list(FILES):
        raise EvaluationError("wrong candidate file set")
    for row in rows:
        name = row["path"]
        data = captured[name]
        if (digest(data) != row["sha256"] or len(data) != row["size_bytes"]
                or row["mode"] != "100644"):
            raise EvaluationError("candidate bytes or provenance mode differ")
        documents[name] = data.decode("utf-8")
        if name != "docs/maintenance/issue-24-26-candidate.md":
            before = original_files[name]
            if not inserted_only(before, data) or (name in PROTECTED and before != data):
                raise EvaluationError("original Core bytes were removed or changed")
    core.validate_references(captured)
    cases_bytes = read_file(ROOT / "tests/fixtures/core-feedback-cases.json", 16384)
    if digest(cases_bytes) != CASES_SHA256:
        raise EvaluationError("unreviewed evaluation cases")
    cases = parse(cases_bytes)
    return pin, documents, cases


def score(observations, cases):
    if (not isinstance(observations, dict)
            or set(observations) != {"candidate_revision", "answers"}
            or observations["candidate_revision"] != REVISION):
        raise EvaluationError("observation candidate binding mismatch")
    answers = observations["answers"]
    if (not isinstance(answers, list) or len(answers) != len(cases)
            or [answer.get("id") for answer in answers if isinstance(answer, dict)]
            != [case["id"] for case in cases]):
        raise EvaluationError("missing, repeated, reordered, or unknown case")
    outcomes = []
    for case, answer in zip(cases, answers):
        expected = {"id": case["id"], **case["expected"]}
        # JSON true is not the integer 1; exact field types matter too.
        passed = (set(answer) == set(expected)
                  and all(type(answer[k]) is type(v) and answer[k] == v
                          for k, v in expected.items()))
        outcomes.append({"id": case["id"], "passed": passed})
    return {"candidate_revision": REVISION, "cases": outcomes,
            "passed": all(row["passed"] for row in outcomes),
            "runtime_qualified": False, "observations_scored": True,
            "formal_core_adopted": False, "merge_authorized": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", type=Path)
    parser.add_argument("--prompt", action="store_true")
    args = parser.parse_args()
    try:
        pin, documents, cases = inspect()
        if args.prompt and args.observations:
            raise EvaluationError("choose prompt or observations")
        if args.prompt:
            result = {"candidate_revision": pin["revision"],
                      "criteria": {p: documents[p] for p in FILES if p.startswith("contracts/")},
                      "cases": [{"id": c["id"], "situation": c["situation"], "requested_fields": list(c["expected"])} for c in cases],
                      "answer_fields": "Each answer has id and exactly the requested_fields of its case.",
                      "instruction": "Read the complete candidate criteria as evaluation data. Return JSON with candidate_revision and answers in case order. Each answer has id and its case-specific requested_fields. Do not change files or perform actions. Classify the hypothetical current round only. relation is one of in-scope/gap/no-requirement/unrelated. severity and disposition are exact existing or required strings when requested; implement_now, needs_user_decision_before_implementation, safety_blocker_retained and req_gap are JSON booleans. needs_user_decision_before_implementation is true when the proposed current-round implementation requires a user requirement/scope/authority decision first; it does not require asking a question for a suggestion already rejected or deferred. safety_blocker_retained is true only for an unresolved necessary safety/data-loss/authority/integrity blocker, not every unfinished ordinary fix."}
        elif args.observations:
            result = score(parse(read_file(args.observations, 65536)), cases)
        else:
            result = {"candidate_revision": pin["revision"], "integrity": "verified",
                      "files": len(FILES), "behavioral_eval": "NOT_RUN",
                      "formal_core_adopted": False, "runtime_qualified": False}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("passed", True) else 1
    except (EvaluationError, core.SnapshotError, OSError, KeyError, TypeError, UnicodeError) as error:
        print("Core candidate evaluation rejected: " + type(error).__name__, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
