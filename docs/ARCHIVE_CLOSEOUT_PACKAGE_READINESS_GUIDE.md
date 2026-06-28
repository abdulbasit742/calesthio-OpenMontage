# Archive Closeout Package Readiness Guide

This guide documents the `archive_closeout_package_readiness.py` builder for OpenMontage Plus archive governance.

Use it after the rollup, review gate, and milestone manifest have been generated.

## Purpose

The archive closeout package readiness builder combines the final machine-readable checkpoints into one package handoff status.

It reads:

- `archive_closeout_rollup.json`
- `archive_closeout_review_gate.json`
- `archive_closeout_milestone_manifest.json`

Then it checks whether the archive package is ready for final handoff.

## Required Statuses

The package is ready only when:

- rollup status is `ready`
- review gate status is `approved`
- milestone manifest status is `complete`

If any input is missing, invalid, or has an unexpected status, the readiness report is marked `blocked`.

## Command

```bash
python extras/archive_closeout_package_readiness.py --rollup archive_closeout_rollup.json --review-gate archive_closeout_review_gate.json --manifest archive_closeout_milestone_manifest.json --label archive-closeout-package-readiness --out-json archive_closeout_package_readiness.json --out-md ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md
```

## Output Files

- `archive_closeout_package_readiness.json`
- `ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md`

## Status Meaning

- `ready-for-handoff`: all required checkpoints loaded and passed.
- `blocked`: one or more required checkpoints are missing, invalid, or not approved.

## Suggested Workflow

1. Generate the closeout rollup.
2. Generate the review gate.
3. Generate the milestone manifest.
4. Run `archive_closeout_package_readiness.py`.
5. Confirm the readiness status is `ready-for-handoff`.
6. Attach the readiness Markdown to the final archive package.
7. Keep the readiness JSON as the machine-readable handoff status.

## Best Practice

Use this readiness report as the final package-level checkpoint. It should be generated after all lower-level reports are present so the final handoff has a single clear status.
