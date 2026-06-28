# Archive Closeout Delivery Check Helper Audit Note

This note records the audit coverage point for the archive closeout delivery check helper flow.

## Purpose

Use this note to confirm that the archive closeout delivery check builder, guide, helper, and helper guide are included in the final archive package.

The delivery check helper flow should verify that these files exist before the final pass or blocked delivery checkpoint is considered covered:

- `extras/archive_closeout_delivery_check.py`
- `docs/ARCHIVE_CLOSEOUT_DELIVERY_CHECK_GUIDE.md`
- `extras/archive_closeout_delivery_check_helper.py`
- `docs/ARCHIVE_CLOSEOUT_DELIVERY_CHECK_HELPER_GUIDE.md`

## Recommended Check

Run the helper to inspect delivery check tool metadata and generate the exact final delivery check command.

```bash
python extras/archive_closeout_delivery_check_helper.py show
python extras/archive_closeout_delivery_check_helper.py command --delivery-seal archive_closeout_delivery_seal.json --delivery-index archive_closeout_delivery_index.json --label archive-closeout-delivery-check --owner "Archive Owner" --out-json archive_closeout_delivery_check.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_CHECK.md
```

## Expected Outputs

- `archive_closeout_delivery_check.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_CHECK.md`

## Audit Result

The delivery check helper step is considered covered when the builder, guide, helper, helper guide, generated delivery check JSON, and generated delivery check Markdown are all present in the final archive package.

## Reviewer Checkpoint

This audit note should be reviewed after the delivery index is generated and before the archive closeout package is marked complete.
