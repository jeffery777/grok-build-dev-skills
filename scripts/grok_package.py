#!/usr/bin/env python3
"""Verify and stage the offline Grok consumer package; never starts Grok."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

# Avoid adding import caches to a staged package during its own verification.
sys.dont_write_bytecode = True
import core_snapshot as core

ROOT = Path(__file__).resolve().parents[1]
FORMAT = "grok-offline-package/v1"
PACKET_FORMAT = "grok-consumer-evidence/v1"
VERSION = "1.0.52 (0920c8169e27)"
CATALOG = "capabilities/grok-build-1.0.52.json"
MANIFEST = "grok.package.json"
SKILLS = ("grok-engineering-workflow", "grok-review-change")
PATHS = frozenset({
    "LICENSE", "core.lock.json", CATALOG, "references/grok-capabilities.md",
    "scripts/core_snapshot.py", "scripts/grok_package.py",
    *(f"skills/{name}/SKILL.md" for name in SKILLS),
    *(f"vendor/engineering-workflow-core/{name}" for name in core.FILES),
})
TOOL_NAMES = {
    "native_spawn": {"task", "spawn_subagent"},
    "native_output": {"get_task_output", "get_command_or_subagent_output"},
    "native_wait": {"wait_tasks", "wait_commands_or_subagents"},
    "native_cancel": {"kill_task", "kill_command_or_subagent"},
    "native_message": {"send_subagent_message"},
}
CAPABILITIES = frozenset(TOOL_NAMES) | {"peer_sessions", "acp_stdio"}
BLOCKED = [
    {"id": "G2-R01", "reason": "No qualified effective sandbox/permission and deny readback."},
    {"id": "G2-R02", "reason": "Actual loaded tool schemas and model/effort remain unverified."},
    {"id": "G2-R03", "reason": "Native child lifecycle and independent review are not runtime-qualified."},
    {"id": "G2-R04", "reason": "Approval forwarding, waiting, reject/cancel and identity binding remain unqualified."},
    {"id": "G2-R05", "reason": "Explicit-session resume/recovery and uncertain-effect reconciliation remain unqualified."},
    {"id": "G2-R06", "reason": "Skill loading, API/subscription entitlement and installation are not verified or granted."},
]


def read_file(root: Path, name: str, *, snapshot: bool = True) -> bytes:
    name = core.relative_path(name)
    parent = core.open_directory(root / Path(name).parent)
    try:
        return core.read_regular(parent, Path(name).name, snapshot=snapshot)
    finally:
        core.os.close(parent)


def json_data(raw: bytes) -> object:
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=core.no_duplicate_keys)
    except core.SnapshotError:
        raise
    except (ValueError, RecursionError) as error:
        raise core.SnapshotError("invalid bounded UTF-8 JSON") from error


def digest(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise core.SnapshotError("invalid lowercase digest")
    return value


def catalog_data(raw: bytes) -> dict:
    data = core.exact_keys(json_data(raw), {
        "format", "runtime", "documented_version", "sources", "capabilities", "known_limits",
    })
    if (data["format"] != "grok-documented-capabilities/v1"
            or data["runtime"] != "grok-build" or data["documented_version"] != VERSION):
        raise core.SnapshotError("unsupported documented capability identity")
    if (not isinstance(data["capabilities"], list)
            or len(data["capabilities"]) != len(CAPABILITIES)):
        raise core.SnapshotError("invalid documented capability inventory")
    ids = set()
    for item in data["capabilities"]:
        core.exact_keys(item, {"id", "documented", "names", "limits", "source_ids"})
        if (not isinstance(item["id"], str) or item["id"] not in CAPABILITIES
                or item["id"] in ids or item["documented"] is not True):
            raise core.SnapshotError("invalid or duplicate documented capability")
        for field in ("names", "limits", "source_ids"):
            if (not isinstance(item[field], list) or not item[field]
                    or any(not isinstance(value, str) or not value for value in item[field])):
                raise core.SnapshotError("invalid documented capability detail")
        ids.add(item["id"])
    if not isinstance(data["sources"], list) or not data["sources"]:
        raise core.SnapshotError("missing capability sources")
    source_ids = set()
    for source in data["sources"]:
        core.exact_keys(source, {"id", "kind", "location", "sha256", "accessed_on"})
        if (not isinstance(source["id"], str)
                or not re.fullmatch(r"[a-z0-9-]{1,64}", source["id"])
                or source["id"] in source_ids or source["accessed_on"] != "2026-10-15"):
            raise core.SnapshotError("invalid capability source identity")
        if source["kind"] == "bundled-guide":
            core.relative_path(source["location"])
            digest(source["sha256"])
        elif source["kind"] == "official-website":
            if (not isinstance(source["location"], str)
                    or not re.fullmatch(r"https://docs\.x\.ai/build/[a-z0-9/-]+", source["location"])
                    or source["sha256"] is not None):
                raise core.SnapshotError("invalid official capability source")
        else:
            raise core.SnapshotError("unknown capability source kind")
        source_ids.add(source["id"])
    if any(set(item["source_ids"]) - source_ids for item in data["capabilities"]):
        raise core.SnapshotError("missing capability source reference")
    if (not isinstance(data["known_limits"], list) or not data["known_limits"]
            or any(not isinstance(value, str) or not value for value in data["known_limits"])):
        raise core.SnapshotError("missing capability limitations")
    return data


def validate_skills(files: dict[str, bytes]) -> None:
    seen = set()
    for name in SKILLS:
        try:
            text = files[f"skills/{name}/SKILL.md"].decode("utf-8")
        except UnicodeError as error:
            raise core.SnapshotError("skill is not UTF-8") from error
        match = re.match(r"\A---\nname: ([a-z0-9-]{1,63})\ndescription: ([^\n]+)\n---\n(.+)\Z", text, re.S)
        # This consumer accepts its two canonical plain-scalar headers, not all YAML.
        if (not match or match.group(1) != name or match.group(1) in seen
                or not 10 <= len(match.group(2)) <= 300
                or match.group(2) != match.group(2).strip()
                or not re.fullmatch(r"[A-Za-z][A-Za-z0-9 ,./()_-]*", match.group(2))):
            raise core.SnapshotError("invalid or duplicate canonical skill identity")
        seen.add(match.group(1))


def verify(root: Path, layout: str = "source") -> tuple[dict, dict[str, bytes], dict]:
    root = core.absolute_path(root)
    raw_manifest = read_file(root, MANIFEST)
    manifest = core.exact_keys(json_data(raw_manifest), {"format", "core_revision", "files"})
    if manifest["format"] != FORMAT or manifest["core_revision"] != core.CORE_REVISION:
        raise core.SnapshotError("unsupported package identity")
    if not isinstance(manifest["files"], list) or len(manifest["files"]) != len(PATHS):
        raise core.SnapshotError("invalid package inventory")
    expected = {}
    for item in manifest["files"]:
        core.exact_keys(item, {"path", "sha256"})
        name = core.relative_path(item["path"])
        if name not in PATHS or name in expected:
            raise core.SnapshotError("unknown or duplicate package path")
        expected[name] = digest(item["sha256"])
    if layout == "staging":
        files = core.capture_inventory(root, PATHS | {MANIFEST})
        if files[MANIFEST] != raw_manifest:
            raise core.SnapshotError("package manifest changed during capture")
    elif layout == "source":
        # Development docs/tests are outside the package. Owned skill/reference/catalog
        # roots must be exact, so extra assets or duplicate skill directories fail.
        files = {name: read_file(root, name) for name in PATHS}
        for folder in ("skills", "references", "capabilities"):
            names = {name[len(folder) + 1:] for name in PATHS if name.startswith(folder + "/")}
            captured = core.capture_inventory(root / folder, names)
            if any(captured[name] != files[folder + "/" + name] for name in names):
                raise core.SnapshotError("package directory changed during capture")
        files[MANIFEST] = raw_manifest
    else:
        raise core.SnapshotError("unknown package layout")
    for name, expected_digest in expected.items():
        if core.sha256(files[name]) != expected_digest:
            raise core.SnapshotError("package digest mismatch")
    core_result, core_files = core.verify(root / "core.lock.json", root / "vendor/engineering-workflow-core")
    if any(files["vendor/engineering-workflow-core/" + name] != raw for name, raw in core_files.items()):
        raise core.SnapshotError("Core changed during package capture")
    if core.sha256(files["core.lock.json"]) != core_result["lock_sha256"]:
        raise core.SnapshotError("Core lock changed during package capture")
    validate_skills(files)
    catalog = catalog_data(files[CATALOG])
    references = core.validate_references(files)
    result = {
        "status": "package_verified", "format": FORMAT, "layout": layout,
        "core_revision": core.CORE_REVISION, "core_collection_sha256": core.COLLECTION_SHA256,
        "manifest_sha256": core.sha256(raw_manifest), "verified_files": len(files),
        "local_references": references, "skills": list(SKILLS),
        "runtime_qualified": False, "skill_loading_qualified": False,
        "delegation_qualified": False, "delivery_ready": False,
        "blocked_checks": BLOCKED,
    }
    return result, files, catalog


def capability_report(catalog: dict, packet: bytes | None = None) -> dict:
    names: set[str] = set()
    source_kind = None
    if packet is not None:
        data = core.exact_keys(json_data(packet), {
            "format", "runtime", "documented_version", "source", "observed_tool_names",
        })
        if (data["format"] != PACKET_FORMAT or data["runtime"] != "grok-build"
                or data["documented_version"] != VERSION):
            raise core.SnapshotError("unsupported consumer evidence identity")
        source = core.exact_keys(data["source"], {"kind", "sha256"})
        if source["kind"] not in ("fixture", "operator_report"):
            raise core.SnapshotError("unsupported consumer evidence source")
        digest(source["sha256"])
        source_kind = source["kind"]
        supplied = data["observed_tool_names"]
        allowed = set().union(*TOOL_NAMES.values())
        if (not isinstance(supplied, list) or len(supplied) > len(allowed)
                or any(not isinstance(name, str) or name not in allowed for name in supplied)
                or len(set(supplied)) != len(supplied)):
            raise core.SnapshotError("invalid relevant native tool-name observation")
        names = set(supplied)
    observations = []
    for item in catalog["capabilities"]:
        matches = bool(names & TOOL_NAMES.get(item["id"], set()))
        observations.append({
            "capability": item["id"], "documented": True,
            "schema_observation": ("fixture_only" if source_kind == "fixture" else "operator_report_unverified")
                if matches else "not_supplied",
            "runtime_verified": False,
        })
    return {
        "status": "packet_validated" if packet is not None else "documented_catalog",
        "packet_format": PACKET_FORMAT, "documented_version": VERSION,
        "source_digest_authenticated": False, "full_grok_schema_validated": False,
        "capabilities": observations, "runtime_qualified": False,
        "skill_loading_qualified": False, "delegation_qualified": False,
        "delivery_ready": False, "blocked_checks": BLOCKED,
    }


def stage(root: Path, destination: Path, layout: str = "source") -> dict:
    result, files, _ = verify(root, layout)
    core.stage_verified_files(files, destination, source_roots=(root, ROOT))
    readback, _, _ = verify(destination, "staging")
    if readback["manifest_sha256"] != result["manifest_sha256"]:
        raise core.SnapshotError("staged package identity mismatch")
    readback["status"] = "package_staged"
    return readback


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("verify", "stage", "capabilities", "packet"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--layout", choices=("source", "staging"), default="source")
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--packet", type=Path)
    args = parser.parse_args()
    if (args.action == "stage") != (args.destination is not None):
        parser.error("--destination is required only for stage")
    if (args.action == "packet") != (args.packet is not None):
        parser.error("--packet is required only for packet")
    try:
        if args.action == "stage":
            result = stage(args.root, args.destination, args.layout)
        else:
            result, _, catalog = verify(args.root, args.layout)
            if args.action in {"capabilities", "packet"}:
                raw = None
                if args.packet is not None:
                    path = core.absolute_path(args.packet)
                    raw = read_file(path.parent, path.name, snapshot=False)
                result = capability_report(catalog, raw)
    except core.SnapshotError as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        return 1
    except OSError as error:
        print(json.dumps({"status": "error", "error": "filesystem operation failed", "errno": error.errno}), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
