# Archive Closeout Handoff Checklist Guide

This guide documents the `archive_closeout_handoff_checklist.py` builder for OpenMontage Plus archive governance.

Use it after the package readiness report has been generated and reports `ready-for-handoff`.

## Purpose

The archive closeout handoff checklist builder creates a final delivery checklist for the archive package.

It checks whether these handoff files exist:

- `archive_closeout_package_readiness.json`
- `ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md`
- `archive_closeout_milestone_manifest.json`
- `ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md`
- `ARCHIVE_CLOSEOUT_ROLLUP.md`
- `ARCHIVE_CLOSEOUT_REVIEW_GATE.md`

It also verifies that the package readiness source reports `ready-for-handoff`.

## Command

```bash
python extras/archive_closeout_handoff_checklist.py --readiness archive_closeout_package_readiness.json --label archive-closeout-handoff-checklist --owner "Archive Owner" --out-json archive_closeout_handoff_checklist.json --out-md ARCHIVE_CLOSEOUT_HANDOFF_CHECKLIST.md
```

## Output Files

- `archive_closeout_handoff_checklist.json`
- `ARCHIVE_CLOSEOUT_HANDOFF_CHECKLIST.md`

## Status Meaning

- `ready`: all handoff checklist items exist and package readiness is `ready-for-handoff`.
- `blocked`: one or more handoff files are missing or package readiness is not ready.

## Suggested Workflow

1. Generate the archive closeout rollup.
2. Generate the review gate.
3. Generate the milestone manifest.
4. Generate the package readiness report.
5. Run `archive_closeout_handoff_checklist.py`.
6. Confirm checklist status is `ready`.
7. Attach all Markdown reports to the final archive package.
8. Keep all JSON outputs as the machine-readable handoff record.
9. Record final owner acknowledgement after package delivery.

## Best Practice

Use this checklist as the last pre-delivery validation step. It gives the archive owner and reviewer one compact view of the final package files before handoff.
