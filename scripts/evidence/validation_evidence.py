#!/usr/bin/env python3
"""Produce and verify this repository's evidence records.

A gate is verified once, locally, by the steward, and its result is committed as
an input-bound record under ``evidence/<gate>/<profile>.json``. Continuous
integration never executes a gate: it recomputes the input projections and
compares them with the committed record, so a stale or missing record fails with
"produce evidence locally" and the command that produces one.

The tracked registry (``scripts/evidence/validation-gates.json``) is the only
source of approved gates, their input scopes and their approved command sets. A
record binds:

* the gate scope digest (every tracked file the gate's paths select),
* the command digest per approved command (argv, environment, scope),
* the producing environment declared by the record's proof profile,
* the composed dependency records, for a catch-all gate.

Nothing named by a record is ever executed by ``verify``.

Usage:
  validation_evidence.py collect [--gate <id>]... [--all] [--profile <id>] [--force]
  validation_evidence.py verify --gate <id> [--profile <id>] [--json]

Because this repository's raster claim is only reproducible with the Linux
toolchain (the favicon ICO frames are zlib-compressed), every record is produced
inside the pinned producer container. Use ``scripts/evidence/linux-producer.sh``
rather than calling ``collect`` on the macOS host.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
SCOPE_DIGEST_VERSION = 1
COMMAND_DIGEST_VERSION = 1

SOURCE_HEADER = b"theory-cloud-design-evidence-source-v1\n"
RELEASE_HEADER = b"theory-cloud-design-evidence-release-v1\n"
NORMALIZED_HEADER = b"theory-cloud-design-evidence-release-normalized-v1\n"
SCOPE_HEADER = b"theory-cloud-design-evidence-scope-v1\n"
VERSION_TOKEN = b"<theory-cloud-design-version>"

EXIT_PASS = 0
EXIT_FAIL = 1

PRODUCE_HINT = (
    "produce evidence locally: run 'make rubric' (scripts/evidence/linux-producer.sh) "
    "on this tree and commit the record it writes; CI verifies records and never executes a gate"
)


class EvidenceError(Exception):
    """A record cannot be produced or does not apply to this tree."""


@dataclass(frozen=True)
class Registry:
    path: Path
    data: dict[str, Any]

    @property
    def evidence_directory(self) -> str:
        return str(self.data["evidenceDirectory"]).strip("/")

    @property
    def profiles(self) -> dict[str, Any]:
        profiles = self.data.get("proofProfiles")
        if not isinstance(profiles, dict) or not profiles:
            raise EvidenceError("the registry declares no proof profiles")
        return profiles

    @property
    def gates(self) -> dict[str, Any]:
        gates = self.data.get("gates")
        if not isinstance(gates, dict) or not gates:
            raise EvidenceError("the registry declares no gates")
        return gates

    @property
    def non_product_paths(self) -> list[str]:
        return [str(item) for item in self.data.get("nonProductPaths", [])]

    @property
    def host_metadata(self) -> list[str]:
        return [str(item) for item in self.data.get("hostMetadata", [])]


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_timestamp(text: Any, label: str) -> datetime:
    if not isinstance(text, str) or not text:
        raise EvidenceError(f"{label} is missing")
    candidate = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        return datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise EvidenceError(f"{label} is not an RFC 3339 timestamp: {text}") from exc


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load_registry(path: Path) -> Registry:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvidenceError(f"no evidence registry at {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"malformed evidence registry: {exc}") from exc
    if not isinstance(data, dict):
        raise EvidenceError("the evidence registry must be a JSON object")
    if int(data.get("schemaVersion", -1)) != SCHEMA_VERSION:
        raise EvidenceError(f"unsupported evidence registry schemaVersion {data.get('schemaVersion')}")
    directory = str(data.get("evidenceDirectory", "")).strip("/")
    if not directory:
        raise EvidenceError("the registry must declare an evidenceDirectory")
    registry = Registry(path=path, data=data)
    registry.profiles  # noqa: B018 - validated here so failures name the registry
    catch_all = [gate_id for gate_id, gate in registry.gates.items() if "**" in gate_paths(gate, gate_id)]
    if not catch_all:
        raise EvidenceError(
            "the registry declares no catch-all gate (paths '**'); an edit to the evidence tooling "
            "would otherwise leave a record that still applies"
        )
    for profile_id, profile in registry.profiles.items():
        environment = profile.get("environment") if isinstance(profile, dict) else None
        if not isinstance(environment, dict) or not environment:
            raise EvidenceError(f"proof profile {profile_id!r} declares no environment")
    return registry


def repo_root(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False
    )
    if completed.returncode != 0:
        raise EvidenceError("not inside a git work tree; the input surface cannot be enumerated")
    return Path(completed.stdout.strip()).resolve()


def matches_path(relative: str, pattern: str) -> bool:
    if pattern == "**":
        return True
    if pattern.endswith("/"):
        return relative.startswith(pattern)
    return fnmatch.fnmatchcase(relative, pattern)


def matches_any(relative: str, patterns: list[str]) -> bool:
    return any(matches_path(relative, pattern) for pattern in patterns)


def is_evidence_path(relative: str, evidence_directory: str) -> bool:
    return relative == evidence_directory or relative.startswith(evidence_directory + "/")


def repo_files(root: Path, registry: Registry) -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise EvidenceError("git ls-files failed; the input surface cannot be enumerated")
    metadata = registry.host_metadata
    return sorted(
        {
            path
            for path in completed.stdout.decode("utf-8", "surrogateescape").split("\0")
            if path and not matches_any(path, metadata)
        }
    )


def read_input_bytes(root: Path, relative: str) -> tuple[int, bytes]:
    path = root / relative
    try:
        metadata = os.lstat(path)
    except FileNotFoundError as exc:
        raise EvidenceError(f"relevant input is missing from the working tree: {relative}") from exc
    if os.path.islink(path):
        return metadata.st_mode & 0o7777, b"symlink:" + os.readlink(path).encode("utf-8", "surrogateescape")
    if not os.path.isfile(path):
        raise EvidenceError(f"relevant input is not a regular file: {relative}")
    try:
        return metadata.st_mode & 0o7777, path.read_bytes()
    except OSError as exc:
        raise EvidenceError(f"cannot read relevant input {relative}: {exc}") from exc


def read_version(root: Path) -> str:
    try:
        text = (root / "VERSION").read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    for line in text.splitlines():
        stripped = line.split("#", 1)[0].strip()
        if stripped:
            return stripped
    return ""


def normalize_release_bytes(data: bytes, version: str) -> bytes:
    """Fold the release-please version stamp so a version bump alone does not stale a record."""
    if not version:
        return data
    literal = version.encode("utf-8")
    return data.replace(b"v" + literal, VERSION_TOKEN).replace(literal, VERSION_TOKEN)


def matches_release_only(relative: str, registry: Registry) -> bool:
    policy = registry.data.get("releaseOnly") or {}
    if relative in set(policy.get("exact", [])):
        return True
    if any(relative.startswith(prefix) for prefix in policy.get("prefixes", [])):
        return True
    return any(fnmatch.fnmatchcase(relative, pattern) for pattern in policy.get("patterns", []))


@dataclass(frozen=True)
class FileEntry:
    mode: int
    data: bytes
    release_only: bool


@dataclass(frozen=True)
class Snapshot:
    files: dict[str, FileEntry]
    source_digest: str
    source_count: int
    release_digest: str
    release_normalized_digest: str
    release_count: int
    release_version: str


def load_snapshot(root: Path, registry: Registry) -> Snapshot:
    version = read_version(root)
    files: dict[str, FileEntry] = {}
    source_lines: list[bytes] = []
    release_lines: list[bytes] = []
    normalized_lines: list[bytes] = []
    source_count = release_count = 0
    for relative in repo_files(root, registry):
        if is_evidence_path(relative, registry.evidence_directory):
            continue
        mode, data = read_input_bytes(root, relative)
        release_only = matches_release_only(relative, registry)
        files[relative] = FileEntry(mode=mode, data=data, release_only=release_only)
        digest = sha256_bytes(data).encode("ascii")
        line = b"%d\t%s\t%s\n" % (mode, relative.encode("utf-8"), digest)
        if release_only:
            release_count += 1
            release_lines.append(line)
            normalized = normalize_release_bytes(data, version)
            normalized_lines.append(
                b"%d\t%s\t%s\n" % (mode, relative.encode("utf-8"), sha256_bytes(normalized).encode("ascii"))
            )
        else:
            source_count += 1
            source_lines.append(line)
    return Snapshot(
        files=files,
        source_digest=sha256_bytes(SOURCE_HEADER + b"".join(sorted(source_lines))),
        source_count=source_count,
        release_digest=sha256_bytes(RELEASE_HEADER + b"".join(sorted(release_lines))),
        release_normalized_digest=sha256_bytes(NORMALIZED_HEADER + b"".join(sorted(normalized_lines))),
        release_count=release_count,
        release_version=version,
    )


def scope_digest(snapshot: Snapshot, patterns: list[str]) -> tuple[str, int]:
    lines: list[bytes] = []
    count = 0
    for relative in sorted(snapshot.files):
        if not matches_any(relative, patterns):
            continue
        entry = snapshot.files[relative]
        if entry.release_only:
            data = normalize_release_bytes(entry.data, snapshot.release_version)
            kind = b"release-normalized"
        else:
            data = entry.data
            kind = b"source"
        lines.append(
            b"%d\t%s\t%s\t%s\n" % (entry.mode, relative.encode("utf-8"), kind, sha256_bytes(data).encode("ascii"))
        )
        count += 1
    payload = SCOPE_HEADER + canonical_json({"version": SCOPE_DIGEST_VERSION, "patterns": patterns}) + b"\n"
    return sha256_bytes(payload + b"".join(lines)), count


def unmatched_inputs(snapshot: Snapshot, registry: Registry) -> list[str]:
    """Tracked files no narrow gate claims, so their impact on a product gate is unknown."""
    scopes = [
        gate_paths(gate, gate_id)
        for gate_id, gate in registry.gates.items()
        if "**" not in gate_paths(gate, gate_id)
    ]
    unknown: list[str] = []
    for relative, entry in snapshot.files.items():
        if entry.release_only or matches_any(relative, registry.non_product_paths):
            continue
        if any(matches_any(relative, patterns) for patterns in scopes):
            continue
        unknown.append(relative)
    return sorted(unknown)


def gate_paths(gate: Any, gate_id: str) -> list[str]:
    if not isinstance(gate, dict):
        raise EvidenceError(f"gate {gate_id!r} must be an object")
    paths = gate.get("paths")
    if not isinstance(paths, list) or not paths or not all(isinstance(item, str) and item for item in paths):
        raise EvidenceError(f"gate {gate_id!r} must declare a non-empty paths array")
    return [str(item) for item in paths]


def gate_profile_ids(gate: dict[str, Any], gate_id: str) -> list[str]:
    profiles = gate.get("profiles") or []
    if not isinstance(profiles, list) or not profiles:
        raise EvidenceError(f"gate {gate_id!r} must declare at least one proof profile")
    return [str(item) for item in profiles]


def resolve_profile(registry: Registry, gate_id: str, requested: str | None) -> str:
    gate = registry.gates.get(gate_id)
    if not isinstance(gate, dict):
        raise EvidenceError(f"gate {gate_id!r} is not approved in the tracked registry")
    allowed = gate_profile_ids(gate, gate_id)
    profile_id = requested or allowed[0]
    if profile_id not in registry.profiles:
        raise EvidenceError(f"proof profile {profile_id!r} is not declared in the tracked registry")
    if profile_id not in allowed:
        raise EvidenceError(
            f"gate {gate_id!r} does not support proof profile {profile_id!r} "
            f"(supported: {', '.join(allowed)})"
        )
    return profile_id


def profile_environment(registry: Registry, profile_id: str) -> dict[str, Any]:
    profile = registry.profiles.get(profile_id)
    if not isinstance(profile, dict):
        raise EvidenceError(f"proof profile {profile_id!r} is not declared in the tracked registry")
    environment = profile.get("environment")
    if not isinstance(environment, dict):
        raise EvidenceError(f"proof profile {profile_id!r} has no declared environment")
    return dict(environment)


def probe_environment() -> dict[str, Any]:
    node = ""
    completed = subprocess.run(["node", "--version"], capture_output=True, text=True, check=False)
    if completed.returncode == 0:
        node = completed.stdout.strip()
    libcairo = ""
    try:  # the raster toolchain is only importable where the gate runs
        import cairocffi  # noqa: PLC0415

        libcairo = str(cairocffi.cairo_version_string())
    except Exception:  # noqa: BLE001 - an absent raster toolchain is recorded as absent
        libcairo = ""
    return {
        "node": node,
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "libcairo": libcairo,
        "platform": {
            "os": "darwin" if sys.platform == "darwin" else "linux" if sys.platform.startswith("linux") else sys.platform,
            "arch": platform.machine(),
        },
    }


_ARCH_ALIASES = {
    "x86_64": "x64",
    "x86-64": "x64",
    "amd64": "x64",
    "x64": "x64",
    "aarch64": "arm64",
    "arm64": "arm64",
}


def _canonical_arch(value: Any) -> str:
    return _ARCH_ALIASES.get(str(value or "").strip().lower(), str(value or "").strip().lower())


def _major(value: Any) -> str:
    return str(value or "").strip().lstrip("v").split(".", 1)[0]


def _major_minor(value: Any) -> str:
    parts = str(value or "").strip().split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else ""


def environment_mismatch(recorded: Any, declared: Any) -> str:
    """Compare a recorded or probed environment with the tracked profile declaration.

    Node is matched at its supported major, Python at its supported major.minor,
    the OS/arch by canonical spelling, and any other declared key exactly. Patch
    levels are deliberately excluded, and the machine that verifies a record is
    not part of the comparison: verification reads the record, not the runner.
    """
    if not isinstance(recorded, dict):
        return "recorded environment is missing"
    if not isinstance(declared, dict):
        return "tracked profile environment is missing"
    for key, expected in declared.items():
        if key == "platform":
            recorded_platform = recorded.get("platform")
            if not isinstance(recorded_platform, dict):
                return "platform binding requires a recorded os/arch"
            if (
                str(recorded_platform.get("os", "")).strip().lower() != str(expected.get("os", "")).strip().lower()
                or _canonical_arch(recorded_platform.get("arch")) != _canonical_arch(expected.get("arch"))
            ):
                return (
                    f"platform {recorded_platform.get('os')}/{recorded_platform.get('arch')} "
                    f"!= profile {expected.get('os')}/{expected.get('arch')}"
                )
            continue
        value = recorded.get(key)
        if not isinstance(value, str) or not value:
            return f"recorded {key} is missing"
        if key == "node":
            if _major(value) != str(expected):
                return f"node {value} != profile major {expected}"
            continue
        if key == "python":
            if _major_minor(value) != str(expected):
                return f"python {value} != profile {expected}"
            continue
        if value != str(expected):
            return f"{key} {value} != profile {expected}"
    return ""


def require_live_environment(registry: Registry, profile_id: str) -> dict[str, Any]:
    """A record must be produced on the host its profile declares."""
    declared = profile_environment(registry, profile_id)
    probed = probe_environment()
    mismatch = environment_mismatch(probed, declared)
    if mismatch:
        raise EvidenceError(
            f"producing environment does not match proof profile {profile_id!r}: {mismatch} "
            "(produce the record on the profile's declared producer)"
        )
    return probed


def gate_commands(gate: dict[str, Any], gate_id: str) -> list[dict[str, Any]]:
    commands = gate.get("commands") or []
    if not isinstance(commands, list):
        raise EvidenceError(f"gate {gate_id!r} commands must be an array")
    depends = gate.get("dependsOn") or []
    if not commands and not depends:
        raise EvidenceError(f"gate {gate_id!r} declares neither commands nor dependencies")
    seen: set[str] = set()
    for command in commands:
        if not isinstance(command, dict):
            raise EvidenceError(f"gate {gate_id!r} commands must be objects")
        command_id = command.get("id")
        argv = command.get("argv")
        if not isinstance(command_id, str) or not command_id or command_id in seen:
            raise EvidenceError(f"gate {gate_id!r} command ids must be unique non-empty strings")
        seen.add(command_id)
        if not isinstance(argv, list) or not argv or not all(isinstance(item, str) and item for item in argv):
            raise EvidenceError(f"gate {gate_id!r} command {command_id} must declare a non-empty argv array")
        cwd = command.get("cwd", "")
        if not isinstance(cwd, str):
            raise EvidenceError(f"gate {gate_id!r} command {command_id} cwd must be a string")
        if cwd.startswith("/") or ".." in Path(cwd).parts:
            raise EvidenceError(f"gate {gate_id!r} command {command_id} cwd must stay inside the repository")
    return commands


def command_cwd(command: dict[str, Any]) -> str:
    return str(command.get("cwd", ""))


def gate_dependencies(gate: dict[str, Any], gate_id: str) -> list[str]:
    depends = gate.get("dependsOn") or []
    if not isinstance(depends, list) or not all(isinstance(item, str) and item for item in depends):
        raise EvidenceError(f"gate {gate_id!r} dependsOn must be an array of gate ids")
    return [str(item) for item in depends]


def command_inputs_digest(
    command: dict[str, Any], scope: str, environment: dict[str, Any], gate: dict[str, Any]
) -> str:
    payload = {
        "version": COMMAND_DIGEST_VERSION,
        "id": command["id"],
        "argv": command["argv"],
        "cwd": command_cwd(command),
        "scope": scope,
        "environment": environment,
        "resource": str(command.get("resource", gate.get("resource", "cpu"))),
    }
    return sha256_bytes(canonical_json(payload))


def record_path_for(root: Path, registry: Registry, gate_id: str, profile_id: str) -> Path:
    return root / registry.evidence_directory / gate_id / f"{profile_id}.json"


def working_tree_dirt(root: Path, registry: Registry) -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise EvidenceError("git status failed; the candidate cannot be proven clean")
    records = [item for item in completed.stdout.decode("utf-8", "surrogateescape").split("\0") if item]
    metadata = registry.host_metadata
    dirty: list[str] = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if len(record) < 4:
            continue
        status = record[:2]
        candidates = [record[3:]]
        if "R" in status or "C" in status:
            if index < len(records):
                candidates.append(records[index])
                index += 1
        for candidate in candidates:
            if is_evidence_path(candidate, registry.evidence_directory):
                continue
            if matches_any(candidate, metadata):
                continue
            dirty.append(candidate)
    return sorted(set(dirty))


def validate_record_shape(
    registry: Registry, gate_id: str, gate: dict[str, Any], record: Any, profile_id: str
) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise EvidenceError("malformed evidence record: not a JSON object")
    if int(record.get("schemaVersion", -1)) != SCHEMA_VERSION:
        raise EvidenceError(f"record schemaVersion {record.get('schemaVersion')} is not supported")
    if record.get("gate") != gate_id:
        raise EvidenceError(f"record names gate {record.get('gate')!r}, not {gate_id!r}")
    if record.get("kind") != gate.get("kind"):
        raise EvidenceError(f"record names kind {record.get('kind')!r}, not {gate.get('kind')!r}")
    if record.get("profile") != profile_id:
        raise EvidenceError(f"record is for proof profile {record.get('profile')!r}, not {profile_id!r}")
    if record.get("verdict") != "PASS":
        raise EvidenceError(f"recorded verdict is {record.get('verdict')!r}")
    parse_timestamp(record.get("recordedAt"), "recordedAt")
    scope = record.get("scope")
    if not isinstance(scope, dict):
        raise EvidenceError("record has no scope binding")
    if int(scope.get("version", -1)) != SCOPE_DIGEST_VERSION:
        raise EvidenceError(f"record scope digest version {scope.get('version')} is not supported")
    if [str(item) for item in scope.get("paths", [])] != gate_paths(gate, gate_id):
        raise EvidenceError("record scope paths do not match the tracked gate")
    if not isinstance(record.get("commands"), list):
        raise EvidenceError("record commands are malformed")
    if not isinstance(record.get("consumed"), list):
        raise EvidenceError("record consumed coverage is malformed")
    return record


def command_digests_for(
    gate: dict[str, Any], gate_id: str, scope: str, declared_environment: dict[str, Any]
) -> dict[str, str]:
    return {
        str(command["id"]): command_inputs_digest(command, scope, declared_environment, gate)
        for command in gate_commands(gate, gate_id)
    }


def verify_gate(
    root: Path, registry: Registry, gate_id: str, profile_id: str, snapshot: Snapshot
) -> dict[str, Any]:
    """Return the gate's applicable record, or raise with the reason it does not apply."""
    gate = registry.gates.get(gate_id)
    if not isinstance(gate, dict):
        raise EvidenceError(f"gate {gate_id!r} is not approved in the tracked registry")
    declared_environment = profile_environment(registry, profile_id)
    record_path = record_path_for(root, registry, gate_id, profile_id)
    if not record_path.is_file():
        raise EvidenceError(
            f"no evidence record at {record_path.relative_to(root)} for proof profile {profile_id!r}"
        )
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"malformed evidence record: {exc}") from exc
    record = validate_record_shape(registry, gate_id, gate, record, profile_id)

    mismatch = environment_mismatch(record.get("environment"), declared_environment)
    if mismatch:
        raise EvidenceError(f"environment-mismatch: {mismatch}")

    unknown = unmatched_inputs(snapshot, registry)
    if unknown and "**" not in gate_paths(gate, gate_id):
        raise EvidenceError(
            "unknown-inputs: " + ", ".join(unknown[:10]) + " (no declared gate scope; re-run the affected gate)"
        )

    rules = gate_paths(gate, gate_id)
    scope, _ = scope_digest(snapshot, rules)
    if record["scope"]["digest"] != scope:
        raise EvidenceError(
            f"gate-scope-inputs-changed: recorded {record['scope']['digest']} candidate {scope} "
            "(the affected gate must run again)"
        )

    expected = command_digests_for(gate, gate_id, scope, declared_environment)
    recorded = {str(entry.get("id")): entry for entry in record["commands"] if isinstance(entry, dict)}
    for command_id, digest in expected.items():
        entry = recorded.get(command_id)
        if entry is None:
            raise EvidenceError(f"record lacks command {command_id}")
        if entry.get("inputsDigest") != digest:
            raise EvidenceError(f"command-inputs-changed: {command_id} recorded {entry.get('inputsDigest')} candidate {digest}")
        if entry.get("exitCode") != 0:
            raise EvidenceError(f"command {command_id} did not pass")
    for command_id in recorded:
        if command_id not in expected:
            raise EvidenceError(f"record names command {command_id!r}, which the tracked gate does not approve")

    declared_dependencies = set(gate_dependencies(gate, gate_id))
    consumed = record.get("consumed") or []
    for item in consumed:
        if not isinstance(item, dict):
            raise EvidenceError("consumed coverage is malformed")
        consumed_gate = str(item.get("gate", ""))
        if consumed_gate not in declared_dependencies:
            raise EvidenceError(f"consumed coverage names undeclared dependency {consumed_gate!r}")
    if declared_dependencies and {str(item.get("gate")) for item in consumed} != declared_dependencies:
        missing = ", ".join(sorted(declared_dependencies - {str(item.get("gate")) for item in consumed}))
        raise EvidenceError(f"record does not consume every declared dependency (missing: {missing})")
    for item in consumed:
        consumed_gate = str(item.get("gate"))
        dependency_gate = registry.gates.get(consumed_gate)
        if not isinstance(dependency_gate, dict):
            raise EvidenceError(f"consumed dependency {consumed_gate!r} is not an approved gate")
        dependency_profile = resolve_profile(registry, consumed_gate, profile_id)
        dependency_scope, _ = scope_digest(snapshot, gate_paths(dependency_gate, consumed_gate))
        if item.get("digest") != dependency_scope:
            raise EvidenceError(
                f"consumed dependency {consumed_gate!r} inputs changed; the composed proof is not applicable"
            )
        verify_gate(root, registry, consumed_gate, dependency_profile, snapshot)
    return record


def verify(args: argparse.Namespace) -> int:
    registry = load_registry(args.registry)
    root = repo_root(args.root)
    gate_id = args.gate
    if not gate_id or gate_id not in registry.gates:
        raise EvidenceError(f"gate {gate_id!r} is not approved in the tracked registry")
    profile_id = resolve_profile(registry, gate_id, args.profile)
    snapshot = load_snapshot(root, registry)
    record = verify_gate(root, registry, gate_id, profile_id, snapshot)
    scope, _ = scope_digest(snapshot, gate_paths(registry.gates[gate_id], gate_id))
    mode = "evidence-verified"
    release = record.get("releaseOnly") or {}
    if record.get("source", {}).get("digest") != snapshot.source_digest:
        if release.get("normalizedDigest") == snapshot.release_normalized_digest:
            mode = "release-transformation-verified"
        else:
            mode = "evidence-verified-declared-out-of-scope-inputs"
    print(
        "validation-evidence: "
        f"gate={gate_id} profile={profile_id} mode={mode} scope={scope} source={record.get('source', {}).get('digest')} "
        f"recorded={record['recordedAt']} environment=node{record.get('environment', {}).get('node', '?')}/"
        f"python{record.get('environment', {}).get('python', '?')} "
        f"platform={(record.get('environment', {}).get('platform') or {}).get('os', '?')}/"
        f"{(record.get('environment', {}).get('platform') or {}).get('arch', '?')} (declared, unauthenticated)"
    )
    if args.json:
        print(
            json.dumps(
                {"gate": gate_id, "profile": profile_id, "mode": mode, "scopeDigest": scope, "recordedAt": record["recordedAt"]},
                sort_keys=True,
            )
        )
    return EXIT_PASS


def record_applicable(root: Path, registry: Registry, gate_id: str, profile_id: str, snapshot: Snapshot) -> tuple[bool, str]:
    try:
        verify_gate(root, registry, gate_id, profile_id, snapshot)
    except EvidenceError as exc:
        return False, str(exc)
    return True, ""


def execute_command(command: dict[str, Any], root: Path) -> dict[str, Any]:
    argv = [str(item) for item in command["argv"]]
    cwd = command_cwd(command)
    print(f"+ {' '.join(argv)}{(' (cwd ' + cwd + ')') if cwd else ''}", flush=True)
    started = time.monotonic()
    started_at = format_timestamp(utc_now())
    completed = subprocess.run(argv, cwd=root / cwd if cwd else root, check=False, capture_output=True, text=True)
    duration = time.monotonic() - started
    if completed.stdout:
        sys.stdout.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    sys.stdout.flush()
    if completed.returncode != 0:
        print(f"  -> exit {completed.returncode} after {duration:.1f}s", flush=True)
    entry: dict[str, Any] = {
        "id": str(command["id"]),
        "argv": argv,
        "exitCode": int(completed.returncode if completed.returncode is not None else -1),
        "durationSeconds": round(duration, 3),
        "startedAt": started_at,
        "finishedAt": format_timestamp(utc_now()),
        "executed": True,
    }
    if cwd:
        entry["cwd"] = cwd
    return entry


def write_record(root: Path, registry: Registry, record: dict[str, Any]) -> Path:
    directory = root / registry.evidence_directory / str(record["gate"])
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{record['profile']}.json"
    payload = json.dumps(record, indent=2, sort_keys=True) + "\n"
    temporary = directory / f".{target.name}.tmp"
    temporary.write_text(payload, encoding="utf-8")
    os.replace(temporary, target)
    return target


def build_record(
    registry: Registry,
    gate_id: str,
    gate: dict[str, Any],
    profile_id: str,
    environment: dict[str, Any],
    snapshot: Snapshot,
    scope: str,
    scope_count: int,
    commands: list[dict[str, Any]],
    consumed: list[dict[str, Any]],
    verdict: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "gate": gate_id,
        "kind": gate.get("kind"),
        "profile": profile_id,
        "description": str(gate.get("description", "")),
        "verdict": verdict,
        "reason": reason,
        "recordedAt": format_timestamp(utc_now()),
        "environment": environment,
        "scope": {
            "version": SCOPE_DIGEST_VERSION,
            "digest": scope,
            "fileCount": scope_count,
            "paths": gate_paths(gate, gate_id),
        },
        "source": {"digest": snapshot.source_digest, "fileCount": snapshot.source_count},
        "releaseOnly": {
            "digest": snapshot.release_digest,
            "normalizedDigest": snapshot.release_normalized_digest,
            "fileCount": snapshot.release_count,
            "version": snapshot.release_version,
        },
        "commands": commands,
        "consumed": consumed,
        "reviews": [],
        "producer": {"tool": "scripts/evidence/validation_evidence.py", "registry": registry.path.name},
    }


def collect_one(
    root: Path, registry: Registry, gate_id: str, profile_id: str, force: bool
) -> dict[str, Any]:
    gate = registry.gates[gate_id]
    environment = require_live_environment(registry, profile_id)
    declared_environment = profile_environment(registry, profile_id)
    snapshot = load_snapshot(root, registry)
    scope, scope_count = scope_digest(snapshot, gate_paths(gate, gate_id))
    dependencies = gate_dependencies(gate, gate_id)

    if not force:
        applicable, _ = record_applicable(root, registry, gate_id, profile_id, snapshot)
        if applicable:
            print(f"validation-evidence: gate={gate_id} profile={profile_id} reusing the record that already applies")
            return json.loads(record_path_for(root, registry, gate_id, profile_id).read_text(encoding="utf-8"))

    dirt = working_tree_dirt(root, registry)
    if dirt:
        raise EvidenceError(
            "the working tree is not clean; a record must bind a committed tree: " + ", ".join(dirt[:10])
        )

    print(f"validation-evidence: collecting gate={gate_id} profile={profile_id}")
    commands: list[dict[str, Any]] = []
    for command in gate_commands(gate, gate_id):
        result = execute_command(command, root)
        result["inputsDigest"] = command_inputs_digest(command, scope, declared_environment, gate)
        commands.append(result)

    consumed: list[dict[str, Any]] = []
    for dependency in dependencies:
        dependency_gate = registry.gates.get(dependency)
        if not isinstance(dependency_gate, dict):
            raise EvidenceError(f"gate {gate_id!r} depends on {dependency!r}, which is not an approved gate")
        dependency_profile = resolve_profile(registry, dependency, profile_id)
        collect_one(root, registry, dependency, dependency_profile, force)
        dependency_scope, _ = scope_digest(snapshot, gate_paths(dependency_gate, dependency))
        consumed.append({"gate": dependency, "profile": dependency_profile, "digest": dependency_scope})

    verdict = "PASS"
    reason = ""
    failed = [entry["id"] for entry in commands if entry["exitCode"] != 0]
    if failed:
        verdict, reason = "FAIL", "command failed: " + ", ".join(failed)
    else:
        after = load_snapshot(root, registry)
        after_scope, _ = scope_digest(after, gate_paths(gate, gate_id))
        if after_scope != scope:
            verdict, reason = "FAIL", "inputs changed during the run (re-run on a clean tree)"

    record = build_record(
        registry,
        gate_id,
        gate,
        profile_id,
        environment,
        snapshot,
        scope,
        scope_count,
        commands,
        consumed,
        verdict,
        reason,
    )
    path = write_record(root, registry, record)
    print(f"validation-evidence: wrote {path.relative_to(root)} verdict={verdict}{(' (' + reason + ')') if reason else ''}")
    if verdict != "PASS":
        raise EvidenceError(f"gate {gate_id!r} did not pass: {reason}")
    return record


def collect(args: argparse.Namespace) -> int:
    registry = load_registry(args.registry)
    root = repo_root(args.root)
    gate_ids = list(args.gate or [])
    if args.all:
        gate_ids = list(registry.gates)
    if not gate_ids:
        raise EvidenceError("select at least one --gate or pass --all")
    for gate_id in gate_ids:
        if gate_id not in registry.gates:
            raise EvidenceError(f"gate {gate_id!r} is not approved in the tracked registry")
    if shutil.which("git") is None:
        raise EvidenceError("git is required to enumerate the input surface")
    for gate_id in gate_ids:
        profile_id = resolve_profile(registry, gate_id, args.profile)
        collect_one(root, registry, gate_id, profile_id, bool(args.force))
    dirt = [
        relative
        for relative in working_tree_dirt(root, registry)
        if not is_evidence_path(relative, registry.evidence_directory)
    ]
    if dirt:
        raise EvidenceError("the run left the tracked tree dirty: " + ", ".join(dirt[:10]))
    print("validation-evidence: done; commit the record files only")
    return EXIT_PASS


def build_parser() -> argparse.ArgumentParser:
    default_registry = Path(__file__).resolve().parent / "validation-gates.json"
    parser = argparse.ArgumentParser(description="Produce or verify this repository's evidence records.")
    parser.add_argument("--registry", type=Path, default=default_registry, help="path to validation-gates.json")
    parser.add_argument("--root", type=Path, default=None, help="repository root (defaults to the git top level)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect_parser = subparsers.add_parser("collect", help="execute the approved commands and write the record")
    collect_parser.add_argument("--gate", action="append", help="gate id to collect (repeatable)")
    collect_parser.add_argument("--all", action="store_true", help="collect every approved gate")
    collect_parser.add_argument("--profile", help="proof profile to collect under")
    collect_parser.add_argument("--force", action="store_true", help="re-execute even when a record already applies")
    collect_parser.set_defaults(handler=collect)

    verify_parser = subparsers.add_parser("verify", help="verify a tracked record against this tree")
    verify_parser.add_argument("--gate", required=True, help="gate id to verify")
    verify_parser.add_argument("--profile", help="proof profile to verify under")
    verify_parser.add_argument("--json", action="store_true", help="also print a machine-readable summary line")
    verify_parser.set_defaults(handler=verify)
    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except EvidenceError as exc:
        print(f"validation-evidence: FAIL ({exc})", file=sys.stderr)
        print(PRODUCE_HINT, file=sys.stderr)
        return EXIT_FAIL


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
