# Archive Closeout Delivery Check Helper Guide

This guide documents the `archive_closeout_delivery_check_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the final delivery check builder metadata or generate the delivery check command without manually typing the script path.

## Purpose

The archive closeout delivery check helper provides a small command registry for the final pass or blocked delivery check builder.

It helps archive operators and reviewers:

- inspect delivery check tool metadata
- confirm the target delivery check builder exists
- generate a runnable final delivery check command
- see the expected JSON and Markdown check outputs
- keep delivery check commands consistent

## Available Commands

```bash
python extras/archive_closeout_delivery_check_helper.py show
python extras/archive_closeout_delivery_check_helper.py list
python extras/archive_closeout_delivery_check_helper.py command --delivery-seal archive_closeout_delivery_seal.json --delivery-index archive_closeout_delivery_index.json --label archive-closeout-delivery-check --owner "Archive Owner" --out-json archive_closeout_delivery_check.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_CHECK.md
```

## Target Script

```text
extras/archive_closeout_delivery_check.py
```

## Output Files

- `archive_closeout_delivery_check.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_CHECK.md`

## Suggested Workflow

1. Generate the delivery seal report.
2. Generate the delivery index report.
3. Run `python extras/archive_closeout_delivery_check_helper.py show` to verify helper metadata.
4. Run the `command` helper to produce the full delivery check builder command.
5. Execute the generated command.
6. Confirm delivery check status is `passed`.
7. Store `ARCHIVE_CLOSEOUT_DELIVERY_CHECK.md` with the final archive package.
8. Keep `archive_closeout_delivery_check.json` as the machine-readable final pass or blocked record.

## Best Practice

Use this helper as the final command reference for archive closeout delivery checking. It gives reviewers and owners the exact command needed to recreate the final pass or blocked check from the delivery seal and delivery index records.
