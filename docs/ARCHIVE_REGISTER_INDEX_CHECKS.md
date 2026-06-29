# Archive Register Index Checks

This file gives quick checks for the archive package index after the register ID has been added.

## Purpose

The index checks confirm that the package index points to both the storage receipt ID and the register ID.

## Use With

- `docs/ARCHIVE_REGISTER_INDEX_NOTE.md`
- `docs/ARCHIVE_REGISTER_FEATURE_276_279_SUMMARY.md`
- `archive_closeout_storage_receipt.json`
- `ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md`

## Checks

- package label is present in the index
- storage receipt ID is present in the index
- register ID is present in the index
- storage owner is present in the index
- storage location is present in the index
- lookup note is present in the index
- register ID matches the register note
- receipt ID matches the storage receipt report

## Pass Rule

The index entry passes when the receipt ID and register ID are both visible in the package index and match the register reference documents.

## Review Note

Keep this checks file beside the index note so a reviewer can quickly confirm that the package lookup path is complete.
