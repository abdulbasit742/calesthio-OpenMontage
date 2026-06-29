# Archive Closeout Feature 270-274 Summary

This summary records the final storage receipt layer added across features 270 through 274.

## Purpose

Features 270-274 add a storage receipt checkpoint for the completed archive closeout package.

This layer sits after storage handoff and confirms that the package receipt can be marked received or blocked before the archive closeout package is considered final.

## Feature Map

| Feature | File | Purpose |
|---|---|---|
| 270 | `extras/archive_closeout_storage_receipt.py` | Builds final storage receipt from a ready-for-storage handoff record. |
| 271 | `docs/ARCHIVE_CLOSEOUT_STORAGE_RECEIPT_GUIDE.md` | Explains storage receipt usage, input file, output files, and status meaning. |
| 272 | `extras/archive_closeout_storage_receipt_helper.py` | Provides helper commands for the storage receipt builder. |
| 273 | `docs/ARCHIVE_CLOSEOUT_STORAGE_RECEIPT_HELPER_GUIDE.md` | Documents helper usage and workflow. |
| 274 | `docs/ARCHIVE_CLOSEOUT_STORAGE_RECEIPT_HELPER_AUDIT_NOTE.md` | Records audit coverage for the helper flow. |

## Main Command

```bash
python extras/archive_closeout_storage_receipt.py --handoff archive_closeout_storage_handoff.json --owner "Archive Owner" --reviewer "Archive Reviewer" --storage-owner "Storage Owner" --receipt-id ARCHIVE-STORAGE-RECEIPT-001 --label archive-closeout-storage-receipt --out-json archive_closeout_storage_receipt.json --out-md ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md
```

## Helper Commands

```bash
python extras/archive_closeout_storage_receipt_helper.py show
python extras/archive_closeout_storage_receipt_helper.py command --handoff archive_closeout_storage_handoff.json --owner "Archive Owner" --reviewer "Archive Reviewer" --storage-owner "Storage Owner" --receipt-id ARCHIVE-STORAGE-RECEIPT-001 --label archive-closeout-storage-receipt --out-json archive_closeout_storage_receipt.json --out-md ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md
python extras/archive_closeout_storage_receipt_helper.py list
```

## Completion Criteria

The feature set is complete when:

1. Storage handoff report exists and reports `ready-for-storage`.
2. Storage receipt report exists and reports `received`.
3. Receipt ID, owner, reviewer, and storage owner fields are present.
4. Guide, helper, helper guide, and audit note are present.
5. JSON and Markdown storage receipt outputs are stored with the final archive package.
6. The receipt is marked final after reviewer and storage owner signoff.

## Package Note

Keep this summary with the archived package so reviewers and storage owners can trace the storage receipt layer and reproduce the command sequence.
