# Archive Closeout Rollup Helper Audit Note

This note records the audit coverage point for the archive closeout rollup helper flow.

## Purpose

Use this note to confirm that the archive closeout rollup builder, guide, helper, and helper guide are included in the final archive package.

The rollup helper flow should verify that these files exist before the rollup checkpoint is considered covered:

- `extras/archive_closeout_rollup.py`
- `docs/ARCHIVE_CLOSEOUT_ROLLUP_GUIDE.md`
- `extras/archive_closeout_rollup_helper.py`
- `docs/ARCHIVE_CLOSEOUT_ROLLUP_HELPER_GUIDE.md`

## Recommended Check

Run the helper to inspect rollup tool metadata and generate the exact rollup command.

```bash
python extras/archive_closeout_rollup_helper.py show
python extras/archive_closeout_rollup_helper.py command --index archive_governance_final_closeout_index.json --summary archive_governance_final_closeout_summary.json --label archive-closeout-rollup --out-json archive_closeout_rollup.json --out-md ARCHIVE_CLOSEOUT_ROLLUP.md
```

## Expected Outputs

- `archive_closeout_rollup.json`
- `ARCHIVE_CLOSEOUT_ROLLUP.md`

## Audit Result

The rollup helper step is considered covered when the builder, guide, helper, helper guide, generated rollup JSON, and generated rollup Markdown are all present in the final archive package.
