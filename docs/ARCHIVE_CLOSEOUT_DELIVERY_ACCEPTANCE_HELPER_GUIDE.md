# Archive Closeout Delivery Acceptance Helper Guide

This guide documents the `archive_closeout_delivery_acceptance_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the final delivery acceptance builder metadata or generate the delivery acceptance command without manually typing the script path.

## Purpose

The archive closeout delivery acceptance helper provides a small command registry for the final owner and reviewer acceptance builder.

It helps archive operators and reviewers:

- inspect delivery acceptance tool metadata
- confirm the target acceptance builder exists
- generate a runnable final delivery acceptance command
- see the expected JSON and Markdown acceptance outputs
- keep acceptance commands consistent across final archive package reviews

## Available Commands

```bash
python extras/archive_closeout_delivery_acceptance_helper.py show
python extras/archive_closeout_delivery_acceptance_helper.py list
python extras/archive_closeout_delivery_acceptance_helper.py command --delivery-check archive_closeout_delivery_check.json --owner "Archive Owner" --reviewer "Archive Reviewer" --label archive-closeout-delivery-acceptance --out-json archive_closeout_delivery_acceptance.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE.md
```

## Target Script

```text
extras/archive_closeout_delivery_acceptance.py
```

## Output Files

- `archive_closeout_delivery_acceptance.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE.md`

## Suggested Workflow

1. Generate the delivery seal report.
2. Generate the delivery index report.
3. Generate the delivery check report.
4. Confirm the delivery check status is `passed`.
5. Run `python extras/archive_closeout_delivery_acceptance_helper.py show` to verify helper metadata.
6. Run the `command` helper to produce the full delivery acceptance builder command.
7. Execute the generated command.
8. Confirm acceptance status is `accepted`.
9. Store `ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE.md` with the final archive package.
10. Keep `archive_closeout_delivery_acceptance.json` as the machine-readable final acceptance record.

## Best Practice

Use this helper as the final command reference for archive closeout delivery acceptance. It gives reviewers and owners the exact command needed to recreate the final acceptance record from a passed delivery check.
