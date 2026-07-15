# Upstream import procedure

## 1. Review the lock update

Before changing `upstream/openmontage.lock.json`:

1. inspect the target upstream commit and release notes;
2. confirm the repository URL is still the intended project;
3. confirm `LICENSE` remains GNU AGPL version 3;
4. record the exact commit and license blob SHAs;
5. review new dependencies, migrations, network calls, model providers, and media-processing commands.

Never replace the pin with a branch name or tag that can move.

## 2. Stage, do not merge

Run:

```bash
bash scripts/import_openmontage_plus.sh
```

The importer creates a verified copy under `.openmontage-import/stage/`. It rejects tracked working-tree changes, symlinks, unsafe destinations, and provenance mismatches. The stage is ignored by Git.

## 3. Inspect the conflict plan

Read `.openmontage-import/import-plan.json` and classify each conflicting path:

- keep the Plus-layer version;
- adopt the upstream version;
- merge both deliberately;
- rename the Plus extension to avoid an upstream collision.

Do not copy the staged root over the fork and do not use repository-wide delete synchronization.

## 4. Create a reviewed import branch

After inspection, create a dedicated branch and copy only approved paths. Preserve:

- upstream `LICENSE` and notices;
- Plus-layer docs and tools;
- existing secrets hygiene;
- generated-file ignores;
- test and CI gates.

Run the upstream project's own documented installation, tests, linting, and build commands after the source is imported. Do not invent success claims before those commands pass.

## 5. Record provenance

The staged `.openmontage-source.json` contains the repository, commit, license blob, fork HEAD, and SHA-256 for every staged file. `verify` fails when any staged source changes after creation.
