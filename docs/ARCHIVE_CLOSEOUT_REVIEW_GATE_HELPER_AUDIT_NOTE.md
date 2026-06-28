# Archive Closeout Review Gate Helper Audit Note

This note records the audit coverage point for the archive closeout review gate helper flow.

## Purpose

Use this note to confirm that the archive closeout review gate builder, guide, helper, and helper guide are included in the final archive package.

The review gate helper flow should verify that these files exist before the final reviewer gate checkpoint is considered covered:

- `extras/archive_closeout_review_gate.py`
- `docs/ARCHIVE_CLOSEOUT_REVIEW_GATE_GUIDE.md`
- `extras/archive_closeout_review_gate_helper.py`
- `docs/ARCHIVE_CLOSEOUT_REVIEW_GATE_HELPER_GUIDE.md`

## Recommended Check

Run the helper to inspect review gate tool metadata and generate the exact review gate command.

```bash
python extras/archive_closeout_review_gate_helper.py show
python extras/archive_closeout_review_gate_helper.py command --rollup archive_closeout_rollup.json --reviewer "Archive Reviewer" --decision approve --out-json archive_closeout_review_gate.json --out-md ARCHIVE_CLOSEOUT_REVIEW_GATE.md
```

## Expected Outputs

- `archive_closeout_review_gate.json`
- `ARCHIVE_CLOSEOUT_REVIEW_GATE.md`

## Audit Result

The review gate helper step is considered covered when the builder, guide, helper, helper guide, generated review gate JSON, and generated review gate Markdown are all present in the final archive package.

## Reviewer Checkpoint

This audit note should be reviewed after the rollup is marked `ready` and before the final handoff is considered approved.
