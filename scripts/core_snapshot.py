#!/usr/bin/env python3
"""Verify the pinned Core snapshot and copy verified bytes to fresh temp staging.

No network, model, installer, credential discovery, or subprocess execution.
The code and its pinned constants are trusted; a lock is not an authority grant.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CORE_REPOSITORY = "https://github.com/jeffery777/engineering-workflow-core"
CORE_REVISION = "7b66978a76597d09be1b55ad199a969b4ee59c0f"
ALGORITHM = "sha256-path-tab-sha256-lf-v1"
COLLECTION_SHA256 = "ef0ed075dfbddd7504f65126deabe135632e4737f3148efaf19551224a577ea5"
LICENSE_SHA256 = "49d64e81e9fd3b12470c1da48367b120b28d404ca08edfdd950278e28e4da34f"
MARKDOWN_PATHS = frozenset({
    "CHANGELOG.md",
    "README.md",
    "contracts/authorization-and-stops.md",
    "contracts/exact-head-and-evidence.md",
    "contracts/review-and-security.md",
    "contracts/workflow.md",
    "docs/architecture/dependency-inventory.md",
    "docs/architecture/migration-plan.md",
    "docs/architecture/project-split.md",
    "docs/provenance/source-map.md",
    "docs/provenance/upstream-notices.md",
    "docs/releases/v0.1.0.md",
    "docs/releases/v0.1.1.md",
})
FILES = MARKDOWN_PATHS | {"LICENSE"}
DIRECTORIES = frozenset(
    str(parent) for name in FILES for parent in PurePosixPath(name).parents
    if str(parent) != "."
)
MAX_FILE_BYTES = 1024 * 1024
ASSEMBLER_VERSION = "1"


class SnapshotError(ValueError):
    """An invalid lock, snapshot, reference, or staging target."""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relative_path(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_./-]+", value):
        raise SnapshotError("invalid manifest path")
    parts = value.split("/")
    if value.startswith("/") or any(part in {"", ".", ".."} for part in parts):
        raise SnapshotError("noncanonical manifest path")
    return value


def exact_keys(value: object, expected: set[str]) -> dict:
    if not isinstance(value, dict) or set(value) != expected:
        raise SnapshotError("invalid lock fields")
    return value


def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise SnapshotError("duplicate JSON key")
        result[key] = value
    return result


def absolute_path(path: Path) -> Path:
    if ".." in path.parts:
        raise SnapshotError("parent traversal in filesystem path")
    return path.absolute()


def open_directory(path: Path) -> int:
    """Open every component without following symlinks, including ancestors."""
    path = absolute_path(path)
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            new_fd = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
            )
            os.close(fd)
            fd = new_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def signature(info: os.stat_result) -> tuple:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def read_regular(parent_fd: int, name: str, *, snapshot: bool = False) -> bytes:
    # NONBLOCK prevents a FIFO from hanging before fstat can reject it.
    fd = os.open(
        name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd
    )
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise SnapshotError("expected a regular, non-hardlinked file")
        if snapshot and stat.S_IMODE(before.st_mode) != 0o644:
            raise SnapshotError("snapshot file mode must be 0644")
        if before.st_size > MAX_FILE_BYTES:
            raise SnapshotError("file exceeds size limit")
        chunks, length = [], 0
        while True:
            data = os.read(fd, min(65536, MAX_FILE_BYTES + 1 - length))
            if not data:
                break
            chunks.append(data)
            length += len(data)
            if length > MAX_FILE_BYTES:
                raise SnapshotError("file exceeds size limit")
        if signature(before) != signature(os.fstat(fd)) or length != before.st_size:
            raise SnapshotError("file changed during read")
        return b"".join(chunks)
    finally:
        os.close(fd)


def load_lock(path: Path) -> tuple[dict, bytes]:
    path = absolute_path(path)
    parent = open_directory(path.parent)
    try:
        raw = read_regular(parent, path.name)
    finally:
        os.close(parent)
    try:
        lock = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicate_keys)
    except SnapshotError:
        raise
    except (ValueError, RecursionError) as error:
        # Includes UTF-8/JSON syntax, integer conversion, and nesting limits.
        raise SnapshotError("lock is not valid UTF-8 JSON") from error
    exact_keys(lock, {
        "schema_version", "core_repository", "core_revision", "contract_language",
        "collection", "files", "license",
    })
    if (type(lock["schema_version"]) is not int or lock["schema_version"] != 1
            or lock["core_repository"] != CORE_REPOSITORY
            or lock["core_revision"] != CORE_REVISION
            or lock["contract_language"] != "zh-TW"):
        raise SnapshotError("unsupported lock identity or schema")
    collection = exact_keys(lock["collection"], {"algorithm", "sha256"})
    if collection != {"algorithm": ALGORITHM, "sha256": COLLECTION_SHA256}:
        raise SnapshotError("unsupported collection algorithm or digest")
    if not isinstance(lock["files"], list) or len(lock["files"]) != len(MARKDOWN_PATHS):
        raise SnapshotError("invalid Markdown inventory")
    found = {}
    for entry in lock["files"]:
        exact_keys(entry, {"path", "sha256"})
        name = relative_path(entry["path"])
        digest = entry["sha256"]
        if name not in MARKDOWN_PATHS or name in found:
            raise SnapshotError("unexpected or duplicate Markdown path")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise SnapshotError("invalid file digest")
        found[name] = digest
    payload = b"".join(
        name.encode("utf-8") + b"\t" + found[name].encode("ascii") + b"\n"
        for name in sorted(found, key=lambda value: value.encode("utf-8"))
    )
    if set(found) != MARKDOWN_PATHS or sha256(payload) != COLLECTION_SHA256:
        raise SnapshotError("file set is not the pinned Markdown collection")
    license_entry = exact_keys(lock["license"], {"path", "sha256"})
    if license_entry != {"path": "LICENSE", "sha256": LICENSE_SHA256}:
        raise SnapshotError("invalid pinned license")
    return lock, raw


def inventory_paths(names: set[str] | frozenset[str]) -> tuple[frozenset[str], frozenset[str]]:
    """Validate a caller-owned inventory before using it as filesystem paths."""
    files = frozenset(relative_path(name) for name in names)
    if not files:
        raise SnapshotError("empty file inventory")
    directories = frozenset(
        str(parent) for name in files for parent in PurePosixPath(name).parents
        if str(parent) != "."
    )
    if files & directories:
        raise SnapshotError("file and directory inventory collision")
    return files, directories


def capture_inventory(root: Path, names: set[str] | frozenset[str]) -> dict[str, bytes]:
    expected_files, expected_directories = inventory_paths(names)
    files: dict[str, bytes] = {}

    def visit(fd: int, prefix: str) -> None:
        before = os.fstat(fd)
        seen = set()
        with os.scandir(fd) as entries:
            for entry in entries:
                name = prefix + entry.name
                if name not in expected_files and name not in expected_directories:
                    raise SnapshotError("unexpected snapshot entry")
                seen.add(name)
                info = os.stat(entry.name, dir_fd=fd, follow_symlinks=False)
                if name in expected_directories:
                    if not stat.S_ISDIR(info.st_mode):
                        raise SnapshotError("expected snapshot directory")
                    child = os.open(
                        entry.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                        dir_fd=fd,
                    )
                    try:
                        visit(child, name + "/")
                    finally:
                        os.close(child)
                else:
                    files[name] = read_regular(fd, entry.name, snapshot=True)
        expected = {
            name for name in expected_files | expected_directories
            if name.startswith(prefix) and "/" not in name[len(prefix):]
        }
        if seen != expected:
            raise SnapshotError("missing snapshot entry")
        if signature(before) != signature(os.fstat(fd)):
            raise SnapshotError("directory changed during read")

    root_fd = open_directory(root)
    try:
        visit(root_fd, "")
    finally:
        os.close(root_fd)
    return files


def capture_snapshot(root: Path) -> dict[str, bytes]:
    return capture_inventory(root, FILES)


def markdown_body(text: str) -> str:
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def anchors(text: str) -> set[str]:
    result = set(re.findall(r"<a\s+[^>]*id=[\"']([^\"']+)[\"']", text))
    counts: dict[str, int] = {}
    for line in text.splitlines():
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)(?:\s+#+\s*)?$", line)
        if match:
            title = match.group(1).replace("`", "").lower()
            slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
            number = counts.get(slug, 0)
            counts[slug] = number + 1
            result.add(slug if not number else f"{slug}-{number}")
    return result


def validate_references(files: dict[str, bytes]) -> int:
    """Check local files/fragments; never dereference external URLs.

    Supported syntax covers this pinned collection: inline/reference links,
    HTML href/src, explicit anchors, and ATX heading fragments.
    """
    documents = {}
    for name, raw in files.items():
        if name.endswith(".md"):
            try:
                documents[name] = markdown_body(raw.decode("utf-8"))
            except UnicodeError as error:
                raise SnapshotError("Markdown is not UTF-8") from error
    targets = {name: anchors(text) for name, text in documents.items()}
    checked = 0
    for name, text in documents.items():
        links = re.findall(r"\[[^\]\n]*\]\(([^\s)]+)\)", text)
        links += re.findall(r"(?m)^ {0,3}\[[^\]]+\]:\s*<?([^>\s]+)>?", text)
        links += re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", text)
        for link in links:
            try:
                parsed = urlsplit(link)
            except ValueError as error:
                raise SnapshotError("invalid reference URL") from error
            if parsed.scheme or parsed.netloc:
                if parsed.scheme not in {"https", "http", "mailto"}:
                    raise SnapshotError("unsupported external reference scheme")
                continue
            path = unquote(parsed.path)
            if (parsed.query or path.startswith("/") or "\\" in path
                    or any(char in path for char in "\x00\t\r\n")):
                raise SnapshotError("unsafe local reference")
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), path)) if path else name
            if target not in files:
                raise SnapshotError("local reference leaves snapshot or is missing")
            fragment = unquote(parsed.fragment)
            if fragment and fragment not in targets.get(target, set()):
                raise SnapshotError("missing local reference anchor")
            checked += 1
    return checked


def verify(lock_path: Path, snapshot: Path) -> tuple[dict, dict[str, bytes]]:
    lock, raw_lock = load_lock(lock_path)
    files = capture_snapshot(snapshot)
    for entry in lock["files"] + [lock["license"]]:
        if sha256(files[entry["path"]]) != entry["sha256"]:
            raise SnapshotError("snapshot digest mismatch")
    references = validate_references(files)
    result = {
        "status": "verified", "core_repository": CORE_REPOSITORY,
        "core_revision": CORE_REVISION, "collection_algorithm": ALGORITHM,
        "collection_sha256": COLLECTION_SHA256, "license_sha256": LICENSE_SHA256,
        "verified_files": len(files), "local_references": references,
        "contract_language": "zh-TW", "lock_sha256": sha256(raw_lock),
        "assembler_version": ASSEMBLER_VERSION,
        "assembler_sha256": sha256(Path(__file__).read_bytes()),
        "adapter_repository": "jeffery777/grok-build-dev-skills",
        "layout": "core-snapshot-v1", "python_version": sys.version.split()[0],
        "runtime_qualified": False, "delivery_ready": False,
    }
    return result, files


def stage_verified_files(
    files: dict[str, bytes], destination: Path, *, source_roots: tuple[Path, ...]
) -> None:
    """Copy already-verified data to a fresh system-temp target; never install."""
    inventory_paths(set(files))
    if any(not isinstance(data, bytes) or len(data) > MAX_FILE_BYTES for data in files.values()):
        raise SnapshotError("invalid captured file bytes")
    destination = absolute_path(destination)
    # Only system temp roots, never an environment-supplied TMPDIR allow grant.
    temp_roots = {Path(os.path.realpath(path)) for path in ("/tmp", "/var/tmp")}
    if not any(destination.is_relative_to(root) and destination != root for root in temp_roots):
        raise SnapshotError("staging destination must be below a system temp root")
    if any(destination.is_relative_to(absolute_path(root)) for root in source_roots):
        raise SnapshotError("staging must not alter the source snapshot")
    parent = open_directory(destination.parent)
    target = None
    try:
        # Exclusive creation; no existing target is adopted or overwritten.
        os.mkdir(destination.name, mode=0o700, dir_fd=parent)
        target = os.open(
            destination.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=parent,
        )
        for name in sorted(files):
            directory = os.dup(target)
            try:
                for component in PurePosixPath(name).parts[:-1]:
                    try:
                        os.mkdir(component, mode=0o700, dir_fd=directory)
                    except FileExistsError:
                        pass
                    child = os.open(
                        component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                        dir_fd=directory,
                    )
                    os.close(directory)
                    directory = child
                fd = os.open(
                    PurePosixPath(name).name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                    0o600, dir_fd=directory,
                )
                try:
                    with os.fdopen(fd, "wb", closefd=False) as output:
                        output.write(files[name])
                    os.fchmod(fd, 0o644)
                finally:
                    os.close(fd)
            finally:
                os.close(directory)
        if capture_inventory(destination, set(files)) != files:
            raise SnapshotError("staging readback differs from verified bytes")
        current = os.stat(destination.name, dir_fd=parent, follow_symlinks=False)
        opened = os.fstat(target)
        if (current.st_dev, current.st_ino) != (opened.st_dev, opened.st_ino):
            raise SnapshotError("staging directory identity changed")
    finally:
        if target is not None:
            os.close(target)
        os.close(parent)
    # Failure retains the fresh partial target for inspection; never removes data.


def stage(lock_path: Path, snapshot: Path, destination: Path) -> dict:
    result, files = verify(lock_path, snapshot)
    stage_verified_files(files, destination, source_roots=(snapshot,))
    result["status"] = "staged"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("verify", "stage"))
    parser.add_argument("--lock", type=Path, default=ROOT / "core.lock.json")
    parser.add_argument("--snapshot", type=Path, default=ROOT / "vendor/engineering-workflow-core")
    parser.add_argument("--destination", type=Path)
    args = parser.parse_args()
    if (args.action == "stage") != (args.destination is not None):
        parser.error("--destination is required only for stage")
    try:
        if args.action == "stage":
            result = stage(args.lock, args.snapshot, args.destination)
        else:
            result, _ = verify(args.lock, args.snapshot)
    except SnapshotError as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        return 1
    except OSError as error:
        print(json.dumps({"status": "error", "error": "filesystem operation failed", "errno": error.errno}), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
