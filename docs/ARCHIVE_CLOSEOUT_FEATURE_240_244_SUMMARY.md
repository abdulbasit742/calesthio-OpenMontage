# Archive Closeout Feature 240-244 Summary

This summary records the final delivery index layer added across features 240 through 244.

## Purpose

Features 240-244 add a reviewer-friendly index for the archive closeout delivery package.

## Feature Map

| Feature | File | Purpose |
|---|---|---|
| 240 | `extras/archive_closeout_delivery_index.py` | Builds delivery index JSON and Markdown across closeout records. |
| 241 | `docs/ARCHIVE_CLOSEOUT_DELIVERY_INDEX_GUIDE.md` | Explains delivery index usage, status meaning, and outputs. |
| 242 | `extras/archive_closeout_delivery_index_helper.py` | Provides helper commands for the delivery index builder. |
| 243 | `docs/ARCHIVE_CLOSEOUT_DELIVERY_INDEX_HELPER_GUIDE.md` | Documents helper usage and workflow. |
| 244 | `docs/ARCHIVE_CLOSEOUT_DELIVERY_INDEX_HELPER_AUDIT_NOTE.md` | Records audit coverage for the helper flow. |

## Main Command

```bash
python extras/archive_closeout_delivery_index.py --label archive-closeout-delivery-index --owner "Archive Owner" --out-json archive_closeout_delivery_index.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md
```

## Helper Commands

```bash
python extras/archive_closeout_delivery_index_helper.py show
python extras/archive_closeout_delivery_index_helper.py command --label archive-closeout-delivery-index --owner "Archive Owner" --out-json archive_closeout_delivery_index.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md
python extras/archive_closeout_delivery_index_helper.py list
```

## Acceptance Criteria

The feature set is complete when:

1. Delivery seal exists before index generation.
2. Delivery index report exists and reports `complete`.
3. Guide, helper, helper guide, and audit note are present.
4. JSON and Markdown index outputs are stored with the final archive package.

## Package Note

Keep this summary with the final package so reviewers can trace the delivery index layer and reproduce the command sequence.
