# Archive Closeout Final Delivery Seal Guide

This guide documents the `archive_closeout_delivery_seal.py` builder for OpenMontage Plus archive governance.

Use it after the owner acknowledgement has been generated and reports `acknowledged`.

## Purpose

The archive closeout final delivery seal builder creates the final sealed-delivery record for the archive package.

It verifies that:

- the owner acknowledgement JSON can be loaded
- the owner acknowledgement status is `acknowledged`
- the release tag and seal metadata are recorded

When these conditions pass, the delivery seal status becomes `sealed`.

## Command

```bash
python extras/archive_closeout_delivery_seal.py --acknowledgement archive_closeout_owner_acknowledgement.json --label archive-closeout-final-delivery-seal --owner "Archive Owner" --reviewer "Archive Reviewer" --release-tag archive-closeout-delivery --out-json archive_closeout_delivery_seal.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md
```

## Output Files

- `archive_closeout_delivery_seal.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md`

## Status Meaning

- `sealed`: owner acknowledgement is present and reports `acknowledged`.
- `blocked`: acknowledgement is missing, invalid, or not acknowledged.

## Suggested Workflow

1. Generate package readiness.
2. Generate the handoff checklist.
3. Generate owner acknowledgement.
4. Confirm owner acknowledgement status is `acknowledged`.
5. Run `archive_closeout_delivery_seal.py`.
6. Confirm delivery seal status is `sealed`.
7. Store the Markdown seal with the final archive package.
8. Keep the JSON seal as the machine-readable final delivery record.

## Best Practice

Use this builder as the final archive closeout record. It should be generated only after readiness, manifest, review gate, handoff checklist, and owner acknowledgement records are complete.
