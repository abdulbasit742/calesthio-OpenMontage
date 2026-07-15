# AGENTS.md

## Scope

These instructions apply to the entire `abdulbasit742/calesthio-OpenMontage` repository.

Project: **OpenMontage Plus**, currently a helper/tooling layer with a pinned, review-only upstream staging workflow. The upstream OpenMontage application has not yet been merged.

## Source boundaries

- `upstream/openmontage.lock.json` is the reviewed source lock.
- `scripts/openmontage_import.py` may stage and verify source only; it must never apply, overwrite, or delete tracked fork files.
- `.openmontage-import/` contains ignored review artifacts and is the only allowed staging root.
- `extras/` contains independent Plus helpers. They must not publish, upload, send messages, or consume paid services without explicit operator action.

## Verified commands

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/repository_check.py
python -m py_compile scripts/openmontage_import.py scripts/repository_check.py tests/test_openmontage_import.py
bash -n scripts/import_openmontage_plus.sh
```

## Upstream import rules

1. Never use a floating branch or mutable tag as the import source; pin a full commit SHA.
2. Review the upstream commit and verify the AGPL-3.0 license before changing the lock.
3. Require a clean tracked working tree before staging.
4. Reject symbolic links and unsafe stage paths.
5. Preserve provenance, fork HEAD, conflict inventory, and per-file hashes.
6. Never reintroduce repository-root `rsync --delete`, broad copy/delete synchronization, fixed shared temporary paths, or an automatic apply command.
7. Review staged conflicts manually on a dedicated branch. Preserve upstream license and attribution.
8. After source import, discover and run the upstream project's documented install, test, lint, migration, and build commands before claiming readiness.

## Completion checklist

- Import safety tests and repository check pass.
- Staging remains review-only and ignored by Git.
- Any lock update names the reviewed commit and license blob.
- Documentation records new conflicts, dependencies, licenses, and residual risks.
