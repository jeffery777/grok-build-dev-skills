"""Explicit Grok GitNexus entry; no model, auto-refresh or qualification probes."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import types

sys.dont_write_bytecode = True
import grok_package as package

ACTOR = "grok"
PROFILE_KEYS = frozenset({
    "configured_path", "runtime_path", "package_root",
    "accepted_executable_sha256", "accepted_runtime_sha256", "accepted_package_sha256",
    "accepted_runner_identity", "accepted_dependency_sha256", "expected_coverage_paths",
    "version_output", "analyze_help_output", "accepted_probe_sha256",
})


class UseError(ValueError):
    """Our entry cannot safely select the requested operation."""


class UncertainRefresh(RuntimeError):
    """The controller did not return a completed result; never replay blindly."""


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("action", choices=("inspect", "plan", "refresh"))
    result.add_argument("--root", type=Path, required=True)
    result.add_argument("--repository-id", required=True)
    result.add_argument("--expected-remote", required=True)
    result.add_argument("--expected-head", required=True)
    result.add_argument("--expected-branch", required=True)
    result.add_argument("--profile", type=Path, required=True)
    result.add_argument("--expected-profile-sha256", required=True)
    result.add_argument("--request-id", required=True)
    result.add_argument("--role", choices=("execution", "review"), default="review")
    result.add_argument("--assigned-writer", choices=("codex", "grok"))
    result.add_argument("--confirm-refresh", action="store_true")
    result.add_argument("--isolated-home", type=Path)
    result.add_argument("--timeout", type=int, default=120)
    return result


def validate_selection(args: argparse.Namespace) -> None:
    if (not args.root.is_absolute() or args.root.resolve(strict=True) != args.root
            or not args.profile.is_absolute()
            or not re.fullmatch(r"[0-9a-f]{40}", args.expected_head)
            or not re.fullmatch(r"[0-9a-f]{64}", args.expected_profile_sha256)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", args.request_id)
            or not args.expected_branch or not 1 <= args.timeout <= 180):
        raise UseError("invalid bounded selection")
    if args.action == "refresh":
        if (args.role != "execution" or args.assigned_writer != ACTOR
                or not args.confirm_refresh or args.isolated_home is None
                or not args.isolated_home.is_absolute()):
            raise UseError("refresh requires the assigned execution writer")
    elif args.confirm_refresh or args.isolated_home is not None:
        raise UseError("write options do not belong to an observation")


@contextmanager
def verified_controller():
    """Execute only captured, code-anchored bytes; preserve bare sibling imports."""
    _, captured, _ = package.verify(package.ROOT)
    names = ("git_source", "memory_contract", "gitnexus_adapter")
    if any(name in sys.modules for name in names):
        raise UseError("controller dependency namespace is already occupied")
    loaded = {}
    try:
        for name in names:
            relative = package.GN_DIRECTORY + "/" + name + ".py"
            raw = captured[relative]
            if hashlib.sha256(raw).hexdigest() != package.GN_FILE_HASHES[relative]:
                raise UseError("controller source changed")
            module = types.ModuleType(name)
            module.__file__ = str(package.ROOT / relative)
            sys.modules[name] = module
            loaded[name] = module
            exec(compile(raw, module.__file__, "exec"), module.__dict__)
        yield loaded["gitnexus_adapter"]
    finally:
        for name, module in loaded.items():
            if sys.modules.get(name) is module:
                del sys.modules[name]


def accepted_profile(args: argparse.Namespace) -> dict:
    raw = package.read_file(args.profile.parent, args.profile.name, snapshot=False)
    if hashlib.sha256(raw).hexdigest() != args.expected_profile_sha256:
        raise UseError("profile differs from independently accepted bytes")
    profile = package.core.exact_keys(package.json_data(raw), PROFILE_KEYS)
    # No runner/environment/lock override is accepted. Coverage stays caller-owned.
    return profile


def operate(args: argparse.Namespace, sdk) -> dict:
    validate_selection(args)
    deadline = time.monotonic() + args.timeout
    repository = sdk.collect_repository_state(
        args.root, canonical_repository_id=args.repository_id,
        expected_remote=args.expected_remote, deadline=deadline,
    )
    if (repository.root != args.root or repository.head != args.expected_head
            or repository.branch != args.expected_branch):
        raise UseError("selected repository identity differs from the brief")
    profile = accepted_profile(args)
    qualification = sdk.qualify_local_1612(**profile, timeout_seconds=args.timeout)
    snapshot = sdk.collect_tracked_snapshot(repository.root, deadline=deadline)
    metadata = sdk.assess_metadata(repository, snapshot, qualification, deadline=deadline)
    result = {
        "format": "grok-gitnexus-operation/v1", "actor": ACTOR,
        "action": args.action, "request_id": args.request_id,
        "role": args.role, "assigned_writer": args.assigned_writer,
        "source_S": package.GN_SOURCE_S, "source_T": package.GN_SOURCE_T,
        "gitnexus_version": "1.6.12", "profile_sha256": args.expected_profile_sha256,
        "repository_identity_digest": repository.identity["repository_identity_digest"],
        "head": repository.head, "branch": repository.branch,
        "metadata": {"state": metadata.state, "reason": metadata.reason,
                     "indexed_revision": metadata.indexed_revision,
                     "metadata_digest": metadata.metadata_digest},
        "authority_granted": False, "gate_satisfied": False,
        "automatic_refresh_enabled": False, "manual_reconciliation_required": False,
    }
    if args.action != "refresh":
        result["status"] = "observed" if args.action == "inspect" else "plan_only"
        # A plan neither grants authority nor duplicates controller eligibility checks.
        return result
    if metadata.state == "fresh":
        return {**result, "status": "not_run", "reason": "already-fresh"}
    if metadata.state not in {"missing", "stale"}:
        return {**result, "status": "blocked", "reason": "index-evidence-not-eligible"}
    controller = sdk.RefreshController(
        qualification, enabled=True, timeout_seconds=args.timeout,
        gitnexus_home=args.isolated_home,
    )
    try:
        refreshed = controller.refresh(
            repository, expected_head=args.expected_head,
            explicit_opt_in=True, deadline=deadline,
        )
    except (Exception, KeyboardInterrupt) as error:
        raise UncertainRefresh("refresh outcome requires reconciliation") from error
    return {**result, "status": refreshed.status, "reason": refreshed.reason,
            "controller_receipt": refreshed.receipt,
            "manual_reconciliation_required": refreshed.status != "refreshed"}


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    binding = {}
    try:
        validate_selection(args)
        binding = {"actor": ACTOR, "action": args.action, "request_id": args.request_id,
                   "root": str(args.root), "head": args.expected_head,
                   "branch": args.expected_branch,
                   "profile_sha256": args.expected_profile_sha256,
                   "source_S": package.GN_SOURCE_S, "source_T": package.GN_SOURCE_T}
        with verified_controller() as sdk:
            result = operate(args, sdk)
    except UncertainRefresh:
        result = {**binding, "status": "unknown", "reason": "refresh-outcome-unconfirmed",
                  "manual_reconciliation_required": True, "automatic_retry": False}
    except KeyboardInterrupt:
        result = {**binding, "status": "cancelled", "reason": "observation-interrupted",
                  "manual_reconciliation_required": False}
    except Exception:
        # Never echo private profile paths, payloads or raw exception text.
        result = {**binding, "status": "blocked", "reason": "preconditions-not-established",
                  "manual_reconciliation_required": False}
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["status"] in {"observed", "plan_only", "not_run", "refreshed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
