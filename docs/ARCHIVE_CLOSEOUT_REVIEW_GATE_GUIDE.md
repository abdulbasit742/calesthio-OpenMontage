# Archive Closeout Review Gate Guide

This guide documents the `archive_closeout_review_gate.py` builder for OpenMontage Plus archive governance.

Use it after the archive closeout rollup has been generated and its status is `ready`.

## Purpose

The archive closeout review gate converts the rollup checkpoint into a final reviewer decision file.

It records:

- rollup source path
- rollup load state
- rollup status
- reviewer name
- reviewer decision
- gate status
- index status
- summary status
- closure status
- missing required files
- invalid JSON files
- review note
- next steps

## Command

```bash
python extras/archive_closeout_review_gate.py --rollup archive_closeout_rollup.json --reviewer "Archive Reviewer" --decision approve --out-json archive_closeout_review_gate.json --out-md ARCHIVE_CLOSEOUT_REVIEW_GATE.md
```

## Output Files

- `archive_closeout_review_gate.json`
- `ARCHIVE_CLOSEOUT_REVIEW_GATE.md`

## Status Meaning

- `approved`: the rollup loaded successfully, the rollup status is `ready`, and the reviewer decision is `approve`.
- `blocked`: the rollup is missing, invalid, not ready, or the reviewer decision is `hold`.

## Decision Values

- `approve`: reviewer confirms the rollup is ready for final handoff.
- `hold`: reviewer pauses the final handoff until issues are fixed.

## Suggested Workflow

1. Generate the final closeout index.
2. Generate the final closeout summary.
3. Generate the archive closeout rollup.
4. Confirm the rollup status is `ready`.
5. Run `archive_closeout_review_gate.py` with `--decision approve` only after review.
6. Confirm the gate status is `approved`.
7. Store `ARCHIVE_CLOSEOUT_REVIEW_GATE.md` with the final archive package.

## Best Practice

Use the review gate as the last human-readable checkpoint after the closeout rollup. The rollup proves the package is ready; the review gate records the reviewer decision.
