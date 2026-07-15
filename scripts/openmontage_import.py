#!/usr/bin/env python3
"""Stage a pinned OpenMontage snapshot without mutating tracked fork files."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Iterable

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCK = DEFAULT_REPO_ROOT / "upstream/openmontage.lock.json"
DEFAULT_STAGE = DEFAULT_REPO_ROOT / ".openmontage-import/stage"
ALLOWED_STAGE_ROOT = ".openmontage-import"


class ImportSafetyError(RuntimeError):
    """Raised when the import cannot continue without weakening a safety boundary."""


@dataclass(frozen=True)
class UpstreamLock:
    repository: str
    commit: str
    license_path: str
    license_blob_sha: str


@dataclass(frozen=True)
class ImportPlan:
    repository: str
    commit: str
    fork_head: str
    staged_at: str
    stage_dir: str
    new_files: tuple[str, ...]
    conflicting_files: tuple[str, ...]
    fork_only_files: tuple[str, ...]


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise ImportSafetyError(detail)
    return result.stdout.strip()


def _safe_relative_path(value: str, label: str) -> str:
    path = Path(value)
    if path.is_absolute() or not value or ".." in path.parts:
        raise ImportSafetyError(f"{label} must be a non-empty relative path")
    return path.as_posix()


def load_lock(path: Path) -> UpstreamLock:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ImportSafetyError(f"Unable to read lock file: {error}") from error

    expected = {"repository", "commit", "license_path", "license_blob_sha"}
    if not isinstance(raw, dict) or set(raw) != expected:
        raise ImportSafetyError(f"Lock file keys must be exactly: {sorted(expected)}")

    repository = str(raw["repository"])
    if not repository.startswith("https://github.com/") or not repository.endswith(".git"):
        raise ImportSafetyError("repository must be an HTTPS GitHub clone URL")
    commit = str(raw["commit"]).lower()
    license_blob_sha = str(raw["license_blob_sha"]).lower()
    if not SHA_RE.fullmatch(commit):
        raise ImportSafetyError("commit must be a full 40-character lowercase SHA")
    if not SHA_RE.fullmatch(license_blob_sha):
        raise ImportSafetyError("license_blob_sha must be a full 40-character lowercase SHA")

    return UpstreamLock(
        repository=repository,
        commit=commit,
        license_path=_safe_relative_path(str(raw["license_path"]), "license_path"),
        license_blob_sha=license_blob_sha,
    )


def ensure_repo_root(root: Path) -> Path:
    root = root.resolve()
    if not (root / ".git").exists():
        raise ImportSafetyError("repo root must contain .git")
    actual = Path(run_git(["rev-parse", "--show-toplevel"], root)).resolve()
    if actual != root:
        raise ImportSafetyError(f"repo root mismatch: expected {root}, got {actual}")
    return root


def ensure_clean_tracked_tree(repo_root: Path) -> None:
    tracked_changes = run_git(["status", "--porcelain", "--untracked-files=no"], repo_root)
    if tracked_changes:
        raise ImportSafetyError("tracked working-tree changes must be committed or stashed before staging")


def ensure_stage_destination(repo_root: Path, stage_dir: Path) -> Path:
    repo_root = repo_root.resolve()
    stage_dir = stage_dir.resolve()
    try:
        relative = stage_dir.relative_to(repo_root)
    except ValueError as error:
        raise ImportSafetyError("stage directory must remain inside the repository") from error
    if not relative.parts or relative.parts[0] != ALLOWED_STAGE_ROOT:
        raise ImportSafetyError(f"stage directory must be inside {ALLOWED_STAGE_ROOT}/")
    git_dir = (repo_root / ".git").resolve()
    if stage_dir == git_dir or git_dir in stage_dir.parents:
        raise ImportSafetyError("stage directory cannot be inside .git")
    return stage_dir


def list_files(root: Path, *, excluded_top_level: Iterable[str] = ()) -> set[str]:
    excluded = set(excluded_top_level)
    files: set[str] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] in excluded:
            continue
        if path.is_symlink():
            raise ImportSafetyError(
                f"Symbolic links are not accepted in staged source: {relative.as_posix()}"
            )
        if path.is_file():
            files.add(relative.as_posix())
    return files


def file_digests(root: Path, *, excluded: Iterable[str] = ()) -> dict[str, str]:
    excluded_set = set(excluded)
    digests: dict[str, str] = {}
    for relative in sorted(list_files(root)):
        if relative in excluded_set:
            continue
        digest = sha256()
        with (root / relative).open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        digests[relative] = digest.hexdigest()
    return digests


def verify_checkout(checkout: Path, lock: UpstreamLock) -> None:
    head = run_git(["rev-parse", "HEAD"], checkout)
    if head != lock.commit:
        raise ImportSafetyError(f"Pinned commit mismatch: expected {lock.commit}, got {head}")
    license_blob = run_git(["rev-parse", f"HEAD:{lock.license_path}"], checkout)
    if license_blob != lock.license_blob_sha:
        raise ImportSafetyError(
            f"License blob mismatch: expected {lock.license_blob_sha}, got {license_blob}"
        )
    try:
        license_text = (checkout / lock.license_path).read_text(
            encoding="utf-8", errors="strict"
        )
    except OSError as error:
        raise ImportSafetyError(f"Unable to read pinned license: {error}") from error
    if "GNU AFFERO GENERAL PUBLIC LICENSE" not in license_text or "Version 3" not in license_text:
        raise ImportSafetyError("Pinned license is not recognized as GNU AGPL v3")
    list_files(checkout, excluded_top_level={".git"})


def clone_pinned(lock: UpstreamLock, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    run_git(["init", "--quiet"], destination)
    run_git(["remote", "add", "origin", lock.repository], destination)
    run_git(["fetch", "--depth", "1", "--no-tags", "origin", lock.commit], destination)
    run_git(["checkout", "--detach", "FETCH_HEAD"], destination)
    verify_checkout(destination, lock)


def create_plan(repo_root: Path, checkout: Path, lock: UpstreamLock, stage_dir: Path) -> ImportPlan:
    upstream_files = list_files(checkout, excluded_top_level={".git"})
    fork_files = set(filter(None, run_git(["ls-files"], repo_root).splitlines()))
    new_files = sorted(upstream_files - fork_files)
    conflicting_files = sorted(upstream_files & fork_files)
    fork_only_files = sorted(fork_files - upstream_files)
    return ImportPlan(
        repository=lock.repository,
        commit=lock.commit,
        fork_head=run_git(["rev-parse", "HEAD"], repo_root),
        staged_at=datetime.now(timezone.utc).isoformat(),
        stage_dir=str(stage_dir),
        new_files=tuple(new_files),
        conflicting_files=tuple(conflicting_files),
        fork_only_files=tuple(fork_only_files),
    )


def stage_checkout(
    repo_root: Path,
    checkout: Path,
    stage_dir: Path,
    lock: UpstreamLock,
    *,
    replace: bool = False,
) -> ImportPlan:
    repo_root = ensure_repo_root(repo_root)
    ensure_clean_tracked_tree(repo_root)
    stage_dir = ensure_stage_destination(repo_root, stage_dir)
    verify_checkout(checkout, lock)

    if stage_dir.exists():
        if not replace:
            raise ImportSafetyError("Stage directory already exists; pass --replace-stage to replace it")
        shutil.rmtree(stage_dir)
    stage_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(checkout, stage_dir, ignore=shutil.ignore_patterns(".git"), symlinks=False)

    plan = create_plan(repo_root, checkout, lock, stage_dir)
    source_files = file_digests(stage_dir)
    provenance = {
        "schema_version": 1,
        "repository": lock.repository,
        "commit": lock.commit,
        "license_path": lock.license_path,
        "license_blob_sha": lock.license_blob_sha,
        "fork_head": plan.fork_head,
        "staged_at": plan.staged_at,
        "mode": "review-only",
        "file_count": len(source_files),
        "files": source_files,
    }
    (stage_dir / ".openmontage-source.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (stage_dir.parent / "import-plan.json").write_text(
        json.dumps(asdict(plan), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return plan


def stage_from_remote(repo_root: Path, lock: UpstreamLock, stage_dir: Path, replace: bool) -> ImportPlan:
    with tempfile.TemporaryDirectory(prefix="openmontage-import-") as temporary:
        checkout = Path(temporary) / "checkout"
        clone_pinned(lock, checkout)
        return stage_checkout(repo_root, checkout, stage_dir, lock, replace=replace)


def verify_stage(stage_dir: Path, lock: UpstreamLock) -> None:
    stage_dir = stage_dir.resolve()
    provenance_path = stage_dir / ".openmontage-source.json"
    try:
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ImportSafetyError(f"Unable to read staged provenance: {error}") from error
    for key, expected in {
        "schema_version": 1,
        "repository": lock.repository,
        "commit": lock.commit,
        "license_path": lock.license_path,
        "license_blob_sha": lock.license_blob_sha,
        "mode": "review-only",
    }.items():
        if provenance.get(key) != expected:
            raise ImportSafetyError(f"Staged provenance mismatch for {key}")
    try:
        license_text = (stage_dir / lock.license_path).read_text(encoding="utf-8")
    except OSError as error:
        raise ImportSafetyError(f"Unable to read staged license: {error}") from error
    if "GNU AFFERO GENERAL PUBLIC LICENSE" not in license_text or "Version 3" not in license_text:
        raise ImportSafetyError("Staged license is missing or invalid")

    expected_files = provenance.get("files")
    if not isinstance(expected_files, dict) or provenance.get("file_count") != len(expected_files):
        raise ImportSafetyError("Staged provenance file inventory is invalid")
    actual_files = file_digests(stage_dir, excluded={".openmontage-source.json"})
    if actual_files != expected_files:
        raise ImportSafetyError("Staged source files do not match the recorded provenance")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stage and verify a pinned OpenMontage snapshot without modifying tracked files"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    stage = subparsers.add_parser("stage", help="clone, verify, and stage the pinned snapshot")
    stage.add_argument("--repo-root", type=Path, default=DEFAULT_REPO_ROOT)
    stage.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    stage.add_argument("--stage-dir", type=Path, default=DEFAULT_STAGE)
    stage.add_argument("--replace-stage", action="store_true")

    verify = subparsers.add_parser("verify", help="verify an existing staged snapshot")
    verify.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    verify.add_argument("--stage-dir", type=Path, default=DEFAULT_STAGE)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        lock = load_lock(args.lock)
        if args.command == "stage":
            plan = stage_from_remote(
                args.repo_root,
                lock,
                args.stage_dir,
                replace=args.replace_stage,
            )
            print(json.dumps(asdict(plan), indent=2))
            print("\nReview the staged snapshot and import-plan.json. No tracked files were changed.")
        else:
            verify_stage(args.stage_dir, lock)
            print("Staged OpenMontage snapshot matches the pinned provenance.")
    except ImportSafetyError as error:
        print(f"ERROR: {error}", file=__import__("sys").stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
