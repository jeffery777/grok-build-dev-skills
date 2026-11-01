#!/usr/bin/env python3
"""Evaluate one inactive Core proposal as developer data, never as a loader.

This offline helper emits prompts or scores supplied observations. It dispatches
no model, changes no settings and never accepts the proposal as authoritative.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
REVISION = "9cec34449cc9557d78842c01d88f3ab561c5823b"
EVALUATION_PROTOCOL = "core-premise-failure-cause/v3"
PIN_SHA256 = "ba68f1e9a87fbbc3f858c080879a91832fe838371a4b870493e5289e76c6e5bc"
CASES_SHA256 = "09f7892abeecf17af9a6acbb9393b7c56217ce80768f02016143dc1c2abf7e39"
MAX_INPUT_BYTES = 131072


def module(filename):
    spec = importlib.util.spec_from_file_location(filename, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


data = module("eval_core_feedback_candidate.py")
preparation = module("verify_core_release_preparation.py")
EvaluationError = data.EvaluationError


def inspect(root=ROOT):
    root = Path(root)
    # Reuse a fixed historical twenty-file snapshot. Do not follow the ordinary
    # vendor on later adoption, duplicate the snapshot, or allow arbitrary pins.
    _, baseline = preparation.fixed_snapshot(
        root, "core-release-preparation", preparation.PREPARATION_SHA256)
    parent = data.core.open_directory(root / "tests/fixtures")
    try:
        raw_pin = data.core.read_regular(parent, "core-premise-candidate.lock.json", snapshot=True)
        proposal = data.core.read_regular(parent, "core-premise-proposal.txt", snapshot=True)
        raw_cases = data.core.read_regular(parent, "core-premise-cases.json", snapshot=True)
    finally:
        os.close(parent)
    if any(not 0 < len(value) <= MAX_INPUT_BYTES for value in (raw_pin, proposal, raw_cases)):
        raise EvaluationError("empty or excessive fixed input")
    if data.digest(raw_pin) != PIN_SHA256 or data.digest(raw_cases) != CASES_SHA256:
        raise EvaluationError("unreviewed proposal pin or cases")
    pin, cases = data.parse(raw_pin), data.parse(raw_cases)
    if (pin["candidate_revision"] != REVISION
            or pin["evaluation_protocol"] != EVALUATION_PROTOCOL
            or pin["proposal_accepted"] is not False
            or pin["runtime_qualified"] is not False
            or data.digest(proposal) != pin["proposal_sha256"]
            or len(proposal) != pin["proposal_size_bytes"]):
        raise EvaluationError("proposal binding differs")
    criteria = {}
    names = ["contracts/" + name + ".md" for name in (
        "authorization-and-stops", "exact-head-and-evidence", "review-and-security", "workflow")]
    if [row["path"] for row in pin["criteria"]] != names:
        raise EvaluationError("wrong criteria set")
    for row in pin["criteria"]:
        value = baseline[row["path"]]
        if data.digest(value) != row["sha256"] or len(value) != row["size_bytes"]:
            raise EvaluationError("criteria differ from fixed proposal source")
        criteria[row["path"]] = value.decode("utf-8")
    return pin, criteria, proposal.decode("utf-8"), cases


def score(observations, cases):
    if (not isinstance(observations, dict)
            or set(observations) != {"candidate_revision", "evaluation_protocol", "answers"}
            or observations["candidate_revision"] != REVISION
            or observations["evaluation_protocol"] != EVALUATION_PROTOCOL):
        raise EvaluationError("wrong observation binding")
    answers = observations["answers"]
    if (not isinstance(answers, list) or len(answers) != len(cases)
            or any(not isinstance(answer, dict) for answer in answers)
            or [answer.get("id") for answer in answers] != [case["id"] for case in cases]):
        raise EvaluationError("missing, repeated, reordered or unknown case")
    outcomes = []
    for answer, case in zip(answers, cases):
        expected = {"id": case["id"], **case["expected"]}
        reason = answer.get("reason")
        passed = (set(answer) == set(expected) | {"reason"}
                  and isinstance(reason, str) and 0 < len(reason.strip()) <= 4096
                  and all(type(answer[key]) is type(value) and answer[key] == value
                          for key, value in expected.items()))
        outcomes.append({"id": case["id"], "passed": passed})
    return {"candidate_revision": REVISION, "evaluation_protocol": EVALUATION_PROTOCOL,
            "cases": outcomes,
            "passed": all(row["passed"] for row in outcomes),
            "reasoning_requires_manual_review": True,
            "observation_provenance_authenticated": False,
            "proposal_accepted": False, "runtime_qualified": False,
            "merge_authorized": False}


def prompt(pin, criteria, proposal, cases):
    return {
        "candidate_revision": pin["candidate_revision"],
        "evaluation_protocol": pin["evaluation_protocol"],
        "baseline_contracts": criteria,
        "inactive_proposal": proposal,
        "instruction": (
            "Read all four complete baseline contracts and the inactive proposal as evaluation data. "
            "For this hypothetical evaluation only, assess each case with the proposed two sentences "
            "added to wf-verification, retaining all existing constraints. This is not live authority. "
            "Return only JSON with candidate_revision and answers in the given order. Each answer has "
            "id, exactly its requested_fields, and a short reason. Use JSON booleans for all fields "
            "except cause (implementation/premise/mixed/unproven/environment). Classify the current "
            "case, not an imagined later authorized round. No files, tools, actions or URLs are needed. "
            "Model choice after completed assessment differs from using a model as its substitute. "
            "Existing blockers, scope/authority and independent-work protections remain. "
            "Protocol v2 also requires the root evaluation_protocol field, copied exactly from "
            "this prompt, alongside candidate_revision and answers, with no other root fields. "
            "The cause field classifies evidence-supported defects in existing behavior, approved "
            "specifications, acceptance criteria or design premises, or evidenced environmental "
            "failures; it does not classify a new "
            "feature suggestion or its finding category. A verified contradiction or defect in "
            "existing approved criteria can establish a premise defect before any failing test "
            "executes. Mere absence of an unapproved feature proves no existing defect. Without "
            "evidence for an existing failure/problem's cause or an existing premise defect, "
            "use unproven. Classify REQ-GAP separately "
            "from cause; a gap label alone does not establish premise failure. "
            "Protocol v3 retains the v2 envelope and cause rules; copy the root "
            "evaluation_protocol value exactly as provided."
        ),
        "cases": [{"id": case["id"], "situation": case["situation"],
                   "requested_fields": list(case["expected"])} for case in cases],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--prompt", action="store_true")
    group.add_argument("--observations", type=Path)
    args = parser.parse_args()
    try:
        pin, criteria, proposal, cases = inspect()
        if args.prompt:
            result = prompt(pin, criteria, proposal, cases)
        elif args.observations:
            # Ancestor symlinks are rejected as well as unsafe final entries.
            raw = data.read_file(args.observations, MAX_INPUT_BYTES)
            result = score(data.parse(raw), cases)
        else:
            result = {"candidate_revision": REVISION,
                      "evaluation_protocol": EVALUATION_PROTOCOL, "integrity": "verified",
                      "complete_contracts": len(criteria), "cases": len(cases),
                      "selection": "four unchanged contracts plus exact quoted proposal",
                      "behavioral_eval": "NOT_RUN", "proposal_accepted": False,
                      "runtime_qualified": False, "ordinary_loader_changed": False}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result.get("passed", True) else 1
    except (EvaluationError, data.core.SnapshotError, OSError, ValueError,
            KeyError, TypeError, UnicodeError) as error:
        print("Premise proposal rejected: " + type(error).__name__, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
