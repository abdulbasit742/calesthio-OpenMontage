# Archive Closeout Storage Receipt Guide

This guide documents the `archive_closeout_storage_receipt.py` builder for OpenMontage Plus archive governance.

Use it after the storage handoff report has been generated. It creates the storage receipt record for the final archive closeout package.

## Purpose

The archive closeout storage receipt builder converts the storage handoff result into a receipt state.

It checks that:

- `archive_closeout_storage_handoff.json` exists
- the file loads correctly as JSON
- `storage_handoff_status` is `ready-for-storage`

If the storage handoff status is ready for storage, the storage receipt record reports `received`. If not, it reports `blocked` and lists the blocker.

## Command

```bash
python extras/archive_closeout_storage_receipt.py --handoff archive_closeout_storage_handoff.json --owner "Archive Owner" --reviewer "Archive Reviewer" --storage-owner "Storage Owner" --receipt-id ARCHIVE-STORAGE-RECEIPT-001 --label archive-closeout-storage-receipt --out-json archive_closeout_storage_receipt.json --out-md ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md
```

## Output Files

- `archive_closeout_storage_receipt.json`
- `ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md`

## Status Meaning

- `received`: storage handoff exists, loads correctly, and reports `ready-for-storage`.
- `blocked`: storage handoff is missing, invalid, or not ready for storage.

## Suggested Workflow

1. Generate delivery seal.
2. Generate delivery index.
3. Generate delivery check.
4. Generate delivery acceptance.
5. Generate package completion.
6. Generate storage handoff.
7. Confirm storage handoff status is `ready-for-storage`.
8. Run the storage receipt builder.
9. Confirm storage receipt status is `received`.
10. Record the receipt ID in the final archive package index.
11. Store the JSON and Markdown receipt records with the archived package.
12. Notify the reviewer that storage receipt has been recorded.

## Reviewer Checklist

Before marking storage receipt final, confirm:

- storage handoff JSON is present
- storage handoff status is `ready-for-storage`
- storage receipt status is `received`
- receipt ID is present and unique
- owner, reviewer, and storage owner fields are correct
- no blockers are listed
- Markdown storage receipt report is included in the final archive package

## Best Practice

Use the storage receipt record as the final confirmation that the completed archive closeout package has been accepted by storage. It should sit after storage handoff and act as the formal receipt record for the archived package.
