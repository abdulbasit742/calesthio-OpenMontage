# Archive Closeout Storage Receipt Helper Guide

This guide documents the `archive_closeout_storage_receipt_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the storage receipt builder metadata or generate the storage receipt command without manually typing the script path.

## Purpose

The archive closeout storage receipt helper provides a small command registry for the storage receipt builder.

It helps archive operators, reviewers, and storage owners:

- inspect storage receipt tool metadata
- confirm the target storage receipt builder exists
- generate a runnable storage receipt command
- see the expected JSON and Markdown storage receipt outputs
- keep storage receipt commands consistent across final archive package reviews

## Available Commands

```bash
python extras/archive_closeout_storage_receipt_helper.py show
python extras/archive_closeout_storage_receipt_helper.py list
python extras/archive_closeout_storage_receipt_helper.py command --handoff archive_closeout_storage_handoff.json --owner "Archive Owner" --reviewer "Archive Reviewer" --storage-owner "Storage Owner" --receipt-id ARCHIVE-STORAGE-RECEIPT-001 --label archive-closeout-storage-receipt --out-json archive_closeout_storage_receipt.json --out-md ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md
```

## Target Script

```text
extras/archive_closeout_storage_receipt.py
```

## Output Files

- `archive_closeout_storage_receipt.json`
- `ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md`

## Suggested Workflow

1. Generate the delivery seal report.
2. Generate the delivery index report.
3. Generate the delivery check report.
4. Generate the delivery acceptance report.
5. Generate the package completion report.
6. Generate the storage handoff report.
7. Confirm the storage handoff status is `ready-for-storage`.
8. Run `python extras/archive_closeout_storage_receipt_helper.py show` to verify helper metadata.
9. Run the `command` helper to produce the full storage receipt builder command.
10. Execute the generated command.
11. Confirm storage receipt status is `received`.
12. Store `ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md` with the archived package.
13. Keep `archive_closeout_storage_receipt.json` as the machine-readable storage receipt record.

## Best Practice

Use this helper as the final command reference for archive closeout storage receipt. It gives reviewers, owners, and storage owners the exact command needed to recreate the final receipt record from a ready-for-storage handoff report.
