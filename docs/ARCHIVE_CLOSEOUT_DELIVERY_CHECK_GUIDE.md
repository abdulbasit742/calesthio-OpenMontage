# Archive Closeout Delivery Check Guide

This guide documents the `archive_closeout_delivery_check.py` builder for OpenMontage Plus archive governance.

Use it after the final delivery seal and final delivery index are generated. It gives reviewers one quick pass or blocked report for the closeout delivery package.

## Purpose

The archive closeout delivery check builder validates the final closeout delivery state.

It checks that:

- `archive_closeout_delivery_seal.json` exists, loads correctly, and reports `sealed`
- `archive_closeout_delivery_index.json` exists, loads correctly, and reports `complete`

The builder writes a JSON report and a Markdown report with the final status, source states, blockers, and next steps.

## Command

```bash
python extras/archive_closeout_delivery_check.py --delivery-seal archive_closeout_delivery_seal.json --delivery-index archive_closeout_delivery_index.json --label archive-closeout-delivery-check --owner "Archive Owner" --out-json archive_closeout_delivery_check.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_CHECK.md
```

## Output Files

- `archive_closeout_delivery_check.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_CHECK.md`

## Status Meaning

- `passed`: delivery seal is `sealed` and delivery index is `complete`.
- `blocked`: one or both source records are missing, invalid, or not in the expected final state.

## Suggested Workflow

1. Generate owner acknowledgement.
2. Generate delivery seal.
3. Generate delivery index.
4. Run delivery check.
5. Confirm delivery check status is `passed`.
6. Store the JSON and Markdown check reports with the final archive package.

## Reviewer Checklist

Before marking delivery complete, confirm:

- delivery seal JSON is present
- delivery index JSON is present
- delivery check status is `passed`
- no blockers are listed
- the Markdown report is included in the final archive package

## Best Practice

Use the delivery check as the final fast reviewer checkpoint. It does not replace the detailed closeout records; it summarizes the final delivery state so owners and reviewers can quickly see whether the package is ready.
