# Archive Closeout Feature 252-256 Summary

This summary records the final delivery acceptance layer added across features 252 through 256.

## Purpose

Features 252-256 add a final owner and reviewer acceptance checkpoint for the archive closeout delivery package.

## Feature Map

| Feature | File | Purpose |
|---|---|---|
| 252 | `extras/archive_closeout_delivery_acceptance.py` | Builds final acceptance from a passed delivery check record. |
| 253 | `docs/ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE_GUIDE.md` | Explains delivery acceptance usage, input file, output files, and status meaning. |
| 254 | `extras/archive_closeout_delivery_acceptance_helper.py` | Provides helper commands for the delivery acceptance builder. |
| 255 | `docs/ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE_HELPER_GUIDE.md` | Documents helper usage and workflow. |
| 256 | `docs/ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE_HELPER_AUDIT_NOTE.md` | Records audit coverage for the helper flow. |

## Main Command

```bash
python extras/archive_closeout_delivery_acceptance.py --delivery-check archive_closeout_delivery_check.json --owner "Archive Owner" --reviewer "Archive Reviewer" --label archive-closeout-delivery-acceptance --out-json archive_closeout_delivery_acceptance.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE.md
```

## Helper Commands

```bash
python extras/archive_closeout_delivery_acceptance_helper.py show
python extras/archive_closeout_delivery_acceptance_helper.py command --delivery-check archive_closeout_delivery_check.json --owner "Archive Owner" --reviewer "Archive Reviewer" --label archive-closeout-delivery-acceptance --out-json archive_closeout_delivery_acceptance.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE.md
python extras/archive_closeout_delivery_acceptance_helper.py list
```

## Acceptance Criteria

The feature set is complete when:

1. Delivery check report exists and reports `passed`.
2. Delivery acceptance report exists and reports `accepted`.
3. Owner and reviewer fields are present.
4. Guide, helper, helper guide, and audit note are present.
5. JSON and Markdown acceptance outputs are stored with the final archive package.

## Package Note

Keep this summary with the final package so reviewers can trace the delivery acceptance layer and reproduce the command sequence.
