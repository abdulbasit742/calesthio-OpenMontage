# Archive Closeout Package Readiness Helper Guide

This guide documents the `archive_closeout_package_readiness_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect package readiness builder metadata or generate the final package readiness command without manually typing the script path.

## Purpose

The archive closeout package readiness helper provides a small command registry for the final readiness builder.

It helps operators and reviewers:

- inspect package readiness tool metadata
- confirm the target readiness builder exists
- generate a runnable package readiness command
- see the expected JSON and Markdown readiness outputs
- keep final handoff commands consistent

## Available Commands

```bash
python extras/archive_closeout_package_readiness_helper.py show
python extras/archive_closeout_package_readiness_helper.py list
python extras/archive_closeout_package_readiness_helper.py command --rollup archive_closeout_rollup.json --review-gate archive_closeout_review_gate.json --manifest archive_closeout_milestone_manifest.json --label archive-closeout-package-readiness --out-json archive_closeout_package_readiness.json --out-md ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md
```

## Target Script

```text
extras/archive_closeout_package_readiness.py
```

## Output Files

- `archive_closeout_package_readiness.json`
- `ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md`

## Suggested Workflow

1. Generate the archive closeout rollup.
2. Generate the archive closeout review gate.
3. Generate the archive closeout milestone manifest.
4. Run `python extras/archive_closeout_package_readiness_helper.py show` to verify helper metadata.
5. Run the `command` helper to produce the full package readiness builder command.
6. Execute the generated command.
7. Confirm the readiness status is `ready-for-handoff`.
8. Store `ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md` with the final archive package.

## Best Practice

Use this helper as the final command reference for package-level handoff review. It gives the reviewer the exact command needed to recreate the final readiness report from the rollup, review gate, and milestone manifest checkpoints.
