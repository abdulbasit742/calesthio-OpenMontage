# Archive Closeout Delivery Seal Helper Guide

This guide documents the `archive_closeout_delivery_seal_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the final delivery seal builder metadata or generate the sealed-delivery command without manually typing the script path.

## Purpose

The archive closeout delivery seal helper provides a small command registry for the final delivery seal builder.

It helps archive operators and reviewers:

- inspect delivery seal tool metadata
- confirm the target delivery seal builder exists
- generate a runnable final delivery seal command
- see the expected JSON and Markdown seal outputs
- keep sealed-delivery commands consistent

## Available Commands

```bash
python extras/archive_closeout_delivery_seal_helper.py show
python extras/archive_closeout_delivery_seal_helper.py list
python extras/archive_closeout_delivery_seal_helper.py command --acknowledgement archive_closeout_owner_acknowledgement.json --label archive-closeout-final-delivery-seal --owner "Archive Owner" --reviewer "Archive Reviewer" --release-tag archive-closeout-delivery --out-json archive_closeout_delivery_seal.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md
```

## Target Script

```text
extras/archive_closeout_delivery_seal.py
```

## Output Files

- `archive_closeout_delivery_seal.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md`

## Suggested Workflow

1. Generate owner acknowledgement.
2. Confirm owner acknowledgement status is `acknowledged`.
3. Run `python extras/archive_closeout_delivery_seal_helper.py show` to verify helper metadata.
4. Run the `command` helper to produce the full delivery seal builder command.
5. Execute the generated command.
6. Confirm delivery seal status is `sealed`.
7. Store `ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md` with the final archive package.
8. Keep `archive_closeout_delivery_seal.json` as the machine-readable final delivery record.

## Best Practice

Use this helper as the final command reference for archive closeout delivery sealing. It gives reviewers and owners the exact command needed to recreate the final delivery seal from the owner acknowledgement checkpoint.
