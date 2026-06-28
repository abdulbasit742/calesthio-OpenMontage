# Archive Closeout Delivery Acceptance Guide

This guide documents the `archive_closeout_delivery_acceptance.py` builder for OpenMontage Plus archive governance.

Use it after the delivery check report has been generated. It creates the final owner and reviewer acceptance record for the archive closeout delivery package.

## Purpose

The archive closeout delivery acceptance builder converts the delivery check result into a final acceptance state.

It checks that:

- `archive_closeout_delivery_check.json` exists
- the file loads correctly as JSON
- `delivery_check_status` is `passed`

If the delivery check is passed, the acceptance record reports `accepted`. If not, it reports `blocked` and lists the blocker.

## Command

```bash
python extras/archive_closeout_delivery_acceptance.py --delivery-check archive_closeout_delivery_check.json --owner "Archive Owner" --reviewer "Archive Reviewer" --label archive-closeout-delivery-acceptance --out-json archive_closeout_delivery_acceptance.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE.md
```

## Output Files

- `archive_closeout_delivery_acceptance.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE.md`

## Status Meaning

- `accepted`: delivery check exists, loads correctly, and reports `passed`.
- `blocked`: delivery check is missing, invalid, or not passed.

## Suggested Workflow

1. Generate delivery seal.
2. Generate delivery index.
3. Generate delivery check.
4. Confirm delivery check status is `passed`.
5. Run the delivery acceptance builder.
6. Confirm acceptance status is `accepted`.
7. Store the JSON and Markdown acceptance records with the final archive package.

## Reviewer Checklist

Before marking acceptance complete, confirm:

- delivery check JSON is present
- delivery check status is `passed`
- acceptance status is `accepted`
- owner and reviewer names are correct
- no blockers are listed
- Markdown acceptance report is included in the final archive package

## Best Practice

Use the acceptance record as the final human-readable closeout checkpoint. It should sit after the delivery check and act as the owner/reviewer acknowledgement that the package is ready for final archival.
