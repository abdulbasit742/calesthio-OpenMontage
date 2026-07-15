# OpenMontage Plus staging layer

This repository contains an independently maintained **Plus layer** and a review-only importer for [`calesthio/OpenMontage`](https://github.com/calesthio/OpenMontage). The upstream application source has **not** been merged into this repository yet.

The old importer could copy a floating upstream branch over the current working tree with `rsync --delete`. That path has been removed. The supported workflow now stages one reviewed upstream commit in an ignored directory, verifies its AGPL-3.0 license, records provenance and file hashes, and produces a conflict plan. It never overwrites tracked fork files.

## Pinned upstream

`upstream/openmontage.lock.json` records:

- the reviewed HTTPS repository URL;
- the exact 40-character upstream commit;
- the license path;
- the expected Git blob SHA for the AGPL-3.0 license.

Changing any lock value requires a separate upstream review and updated documentation.

## Stage an upstream snapshot

Run from anywhere inside or outside the repository:

```bash
bash scripts/import_openmontage_plus.sh
```

This creates only ignored review artifacts:

```text
.openmontage-import/
├── import-plan.json
└── stage/
    ├── .openmontage-source.json
    └── ...pinned upstream files
```

The command fails when:

- tracked fork files are dirty;
- the commit or license blob does not match the lock;
- the upstream tree contains symbolic links;
- the stage exists and `--replace-stage` was not explicitly supplied;
- the requested stage is outside `.openmontage-import/`.

To replace an old stage deliberately:

```bash
bash scripts/import_openmontage_plus.sh --replace-stage
```

To verify an existing staged snapshot and its per-file SHA-256 inventory:

```bash
python scripts/openmontage_import.py verify
```

## Review and import

`import-plan.json` separates:

- files new to the fork;
- paths that conflict with tracked Plus-layer files;
- fork-only files that are absent upstream.

There is intentionally no automatic apply or delete command. Review the staged source, license obligations, secrets/configuration, dependencies, migrations, and conflicting paths before creating a dedicated import branch or pull request. Preserve the upstream AGPL-3.0 license and attribution.

## Verification

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/repository_check.py
python -m py_compile scripts/openmontage_import.py scripts/repository_check.py tests/test_openmontage_import.py
bash -n scripts/import_openmontage_plus.sh
```

CI also compiles the existing `extras/` helpers and runs their smoke commands in an isolated temporary directory so generated demo workspaces do not pollute the checkout.

## Plus helpers

The existing `extras/` directory contains project, budget, export, review, and publish-package helpers. They remain independent of the upstream staging process and must not send, publish, upload, or consume paid services without explicit operator action.

See:

- [`docs/UPSTREAM_IMPORT.md`](docs/UPSTREAM_IMPORT.md)
- [`docs/reference-review.md`](docs/reference-review.md)
- [`docs/security-audit.md`](docs/security-audit.md)
