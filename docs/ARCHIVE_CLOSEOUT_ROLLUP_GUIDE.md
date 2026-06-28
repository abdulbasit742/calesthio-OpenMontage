# Archive Closeout Rollup Guide

This guide documents the `archive_closeout_rollup.py` builder for OpenMontage Plus archive governance.

Use it after the closeout index and closeout summary have both been generated.

## Purpose

The archive closeout rollup combines the detailed closeout index and the short closeout summary into one reviewer checkpoint file.

It records:

- closeout index path
- closeout summary path
- index load state
- summary load state
- index status
- summary status
- closure status
- total indexed items
- missing required files
- invalid JSON files
- reviewer note
- next steps

## Command

```bash
python extras/archive_closeout_rollup.py --index archive_governance_final_closeout_index.json --summary archive_governance_final_closeout_summary.json --label archive-closeout-rollup --out-json archive_closeout_rollup.json --out-md ARCHIVE_CLOSEOUT_ROLLUP.md
```

## Output Files

- `archive_closeout_rollup.json`
- `ARCHIVE_CLOSEOUT_ROLLUP.md`

## Status Meaning

- `ready`: the closeout index reports `closeout-ready` and the closeout summary reports `complete`.
- `needs-attention`: the closeout index or summary is missing, invalid, or not ready.

## Suggested Workflow

1. Generate the final closeout index.
2. Generate the final closeout summary.
3. Confirm the index status is `closeout-ready`.
4. Confirm the summary status is `complete`.
5. Run `archive_closeout_rollup.py`.
6. Confirm the rollup status is `ready`.
7. Store `ARCHIVE_CLOSEOUT_ROLLUP.md` with the final archive package.

## Best Practice

Use the rollup after the detailed index and executive summary. It gives reviewers a compact checkpoint that shows whether both upstream closeout files agree that the package is ready.
