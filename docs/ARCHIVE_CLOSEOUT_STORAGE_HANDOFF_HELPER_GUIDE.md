# Archive Closeout Storage Handoff Helper Guide

This guide documents the `archive_closeout_storage_handoff_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the storage handoff builder metadata or generate the storage handoff command without manually typing the script path.

## Purpose

The archive closeout storage handoff helper provides a small command registry for the storage handoff builder.

It helps archive operators and reviewers:

- inspect storage handoff tool metadata
- confirm the target storage handoff builder exists
- generate a runnable storage handoff command
- see the expected JSON and Markdown storage handoff outputs
- keep storage handoff commands consistent across final archive package reviews

## Available Commands

```bash
python extras/archive_closeout_storage_handoff_helper.py show
python extras/archive_closeout_storage_handoff_helper.py list
python extras/archive_closeout_storage_handoff_helper.py command --completion archive_closeout_package_completion.json --owner "Archive Owner" --reviewer "Archive Reviewer" --storage-owner "Storage Owner" --storage-location "Approved Archive Storage" --label archive-closeout-storage-handoff --out-json archive_closeout_storage_handoff.json --out-md ARCHIVE_CLOSEOUT_STORAGE_HANDOFF.md
```

## Target Script

```text
extras/archive_closeout_storage_handoff.py
```

## Output Files

- `archive_closeout_storage_handoff.json`
- `ARCHIVE_CLOSEOUT_STORAGE_HANDOFF.md`

## Suggested Workflow

1. Generate the delivery seal report.
2. Generate the delivery index report.
3. Generate the delivery check report.
4. Generate the delivery acceptance report.
5. Generate the package completion report.
6. Confirm the package completion status is `complete`.
7. Run `python extras/archive_closeout_storage_handoff_helper.py show` to verify helper metadata.
8. Run the `command` helper to produce the full storage handoff builder command.
9. Execute the generated command.
10. Confirm storage handoff status is `ready-for-storage`.
11. Store `ARCHIVE_CLOSEOUT_STORAGE_HANDOFF.md` with the archived package.
12. Keep `archive_closeout_storage_handoff.json` as the machine-readable storage handoff record.

## Best Practice

Use this helper as the final command reference for archive closeout storage handoff. It gives reviewers, owners, and storage owners the exact command needed to recreate the final handoff record from a complete package completion report.
