from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.openmontage_import import (  # noqa: E402
    ImportSafetyError,
    UpstreamLock,
    ensure_stage_destination,
    load_lock,
    stage_checkout,
    verify_stage,
)


AGPL_TEXT = "GNU AFFERO GENERAL PUBLIC LICENSE\nVersion 3, 19 November 2007\n"


def git(cwd: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def init_repo(path: Path) -> None:
    path.mkdir(parents=True)
    git(path, "init", "-q")
    git(path, "config", "user.email", "test@example.com")
    git(path, "config", "user.name", "Test")


def commit_all(path: Path, message: str = "test") -> str:
    git(path, "add", "-A")
    git(path, "commit", "-qm", message)
    return git(path, "rev-parse", "HEAD")


class ImportTests(unittest.TestCase):
    def make_source(self, root: Path, *, symlink: bool = False) -> tuple[Path, UpstreamLock]:
        source = root / "source"
        init_repo(source)
        (source / "LICENSE").write_text(AGPL_TEXT, encoding="utf-8")
        (source / "app.py").write_text("print('upstream')\n", encoding="utf-8")
        (source / "README.md").write_text("upstream readme\n", encoding="utf-8")
        if symlink:
            (source / "unsafe-link").symlink_to("/tmp")
        commit = commit_all(source)
        blob = git(source, "rev-parse", "HEAD:LICENSE")
        lock = UpstreamLock(
            repository="https://github.com/calesthio/OpenMontage.git",
            commit=commit,
            license_path="LICENSE",
            license_blob_sha=blob,
        )
        return source, lock

    def make_fork(self, root: Path) -> Path:
        fork = root / "fork"
        init_repo(fork)
        (fork / "README.md").write_text("plus readme\n", encoding="utf-8")
        (fork / "extras").mkdir()
        (fork / "extras" / "plus.py").write_text("PLUS = True\n", encoding="utf-8")
        (fork / ".gitignore").write_text(".openmontage-import/\n", encoding="utf-8")
        commit_all(fork)
        return fork

    def test_lock_requires_exact_schema_and_full_shas(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "lock.json"
            path.write_text(json.dumps({"repository": "http://example.com/x"}), encoding="utf-8")
            with self.assertRaises(ImportSafetyError):
                load_lock(path)

    def test_stage_destination_must_be_in_dedicated_repository_area(self):
        with tempfile.TemporaryDirectory() as temp:
            fork = self.make_fork(Path(temp))
            with self.assertRaises(ImportSafetyError):
                ensure_stage_destination(fork.resolve(), fork.resolve())
            with self.assertRaises(ImportSafetyError):
                ensure_stage_destination(fork.resolve(), fork / ".git" / "stage")
            with self.assertRaises(ImportSafetyError):
                ensure_stage_destination(fork.resolve(), fork.parent / "outside")
            with self.assertRaises(ImportSafetyError):
                ensure_stage_destination(fork.resolve(), fork / "random-stage")
            allowed = ensure_stage_destination(fork.resolve(), fork / ".openmontage-import" / "stage")
            self.assertEqual(allowed, (fork / ".openmontage-import" / "stage").resolve())

    def test_stage_is_review_only_and_builds_conflict_inventory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, lock = self.make_source(root)
            fork = self.make_fork(root)
            stage = fork / ".openmontage-import" / "stage"
            plan = stage_checkout(fork, source, stage, lock)
            self.assertTrue((stage / "app.py").exists())
            self.assertEqual((fork / "README.md").read_text(), "plus readme\n")
            self.assertIn("README.md", plan.conflicting_files)
            self.assertIn("app.py", plan.new_files)
            self.assertIn("extras/plus.py", plan.fork_only_files)
            self.assertEqual(plan.fork_head, git(fork, "rev-parse", "HEAD"))
            self.assertTrue((stage.parent / "import-plan.json").exists())
            verify_stage(stage, lock)

    def test_existing_stage_requires_explicit_replace(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, lock = self.make_source(root)
            fork = self.make_fork(root)
            stage = fork / ".openmontage-import" / "stage"
            stage_checkout(fork, source, stage, lock)
            with self.assertRaises(ImportSafetyError):
                stage_checkout(fork, source, stage, lock)
            stage_checkout(fork, source, stage, lock, replace=True)

    def test_dirty_tracked_tree_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, lock = self.make_source(root)
            fork = self.make_fork(root)
            (fork / "README.md").write_text("uncommitted\n", encoding="utf-8")
            with self.assertRaisesRegex(ImportSafetyError, "committed or stashed"):
                stage_checkout(fork, source, fork / ".openmontage-import" / "stage", lock)

    def test_commit_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, lock = self.make_source(root)
            bad_lock = replace(lock, commit="0" * 40)
            fork = self.make_fork(root)
            with self.assertRaises(ImportSafetyError):
                stage_checkout(fork, source, fork / ".openmontage-import" / "stage", bad_lock)

    def test_license_blob_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, lock = self.make_source(root)
            bad_lock = replace(lock, license_blob_sha="0" * 40)
            fork = self.make_fork(root)
            with self.assertRaises(ImportSafetyError):
                stage_checkout(fork, source, fork / ".openmontage-import" / "stage", bad_lock)

    def test_symlinked_upstream_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, lock = self.make_source(root, symlink=True)
            fork = self.make_fork(root)
            with self.assertRaises(ImportSafetyError):
                stage_checkout(fork, source, fork / ".openmontage-import" / "stage", lock)

    def test_verify_stage_detects_provenance_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, lock = self.make_source(root)
            fork = self.make_fork(root)
            stage = fork / ".openmontage-import" / "stage"
            stage_checkout(fork, source, stage, lock)
            provenance = json.loads((stage / ".openmontage-source.json").read_text())
            provenance["commit"] = "0" * 40
            (stage / ".openmontage-source.json").write_text(json.dumps(provenance), encoding="utf-8")
            with self.assertRaises(ImportSafetyError):
                verify_stage(stage, lock)

    def test_verify_stage_detects_source_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, lock = self.make_source(root)
            fork = self.make_fork(root)
            stage = fork / ".openmontage-import" / "stage"
            stage_checkout(fork, source, stage, lock)
            (stage / "app.py").write_text("print('tampered')\n", encoding="utf-8")
            with self.assertRaisesRegex(ImportSafetyError, "do not match"):
                verify_stage(stage, lock)


if __name__ == "__main__":
    unittest.main()
