# Archive Closeout Owner Acknowledgement Guide

This guide documents the `archive_closeout_owner_acknowledgement.py` builder for OpenMontage Plus archive governance.

Use it after the final handoff checklist has been generated and reports `ready`.

## Purpose

The archive closeout owner acknowledgement builder creates the final owner signoff record for the archive package.

It verifies that:

- the handoff checklist JSON can be loaded
- the checklist status is `ready`
- the owner decision is `acknowledge`

When these conditions pass, the acknowledgement status becomes `acknowledged`.

## Command

```bash
python extras/archive_closeout_owner_acknowledgement.py --checklist archive_closeout_handoff_checklist.json --owner "Archive Owner" --reviewer "Archive Reviewer" --decision acknowledge --label archive-closeout-owner-acknowledgement --out-json archive_closeout_owner_acknowledgement.json --out-md ARCHIVE_CLOSEOUT_OWNER_ACKNOWLEDGEMENT.md
```

## Output Files

- `archive_closeout_owner_acknowledgement.json`
- `ARCHIVE_CLOSEOUT_OWNER_ACKNOWLEDGEMENT.md`

## Status Meaning

- `acknowledged`: checklist is ready and owner decision is `acknowledge`.
- `blocked`: checklist is missing, invalid, not ready, or owner decision is `hold`.

## Suggested Workflow

1. Generate package readiness.
2. Generate the handoff checklist.
3. Confirm the handoff checklist status is `ready`.
4. Run `archive_closeout_owner_acknowledgement.py` with `--decision acknowledge`.
5. Confirm acknowledgement status is `acknowledged`.
6. Store the Markdown acknowledgement with the final archive package.
7. Keep the JSON acknowledgement as the machine-readable owner signoff record.

## Best Practice

Use this builder as the final owner signoff step. It should be the last generated archive governance record after readiness, manifest, review gate, and handoff checklist reports are complete.
