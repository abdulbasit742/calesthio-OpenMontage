# Archive Closeout Delivery Index Helper Guide

This guide documents the `archive_closeout_delivery_index_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the final delivery index builder metadata or generate the delivery index command without manually typing the script path.

## Purpose

The archive closeout delivery index helper provides a small command registry for the final delivery index builder.

It helps archive operators and reviewers:

- inspect delivery index tool metadata
- confirm the target delivery index builder exists
- generate a runnable final delivery index command
- see the expected JSON and Markdown index outputs
- keep delivery index commands consistent

## Available Commands

```bash
python extras/archive_closeout_delivery_index_helper.py show
python extras/archive_closeout_delivery_index_helper.py list
python extras/archive_closeout_delivery_index_helper.py command --label archive-closeout-delivery-index --owner "Archive Owner" --out-json archive_closeout_delivery_index.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md
```

## Target Script

```text
extras/archive_closeout_delivery_index.py
```

## Output Files

- `archive_closeout_delivery_index.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md`

## Suggested Workflow

1. Generate all closeout JSON and Markdown records.
2. Generate the final delivery seal.
3. Run `python extras/archive_closeout_delivery_index_helper.py show` to verify helper metadata.
4. Run the `command` helper to produce the full delivery index builder command.
5. Execute the generated command.
6. Confirm delivery index status is `complete`.
7. Store `ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md` with the final archive package.
8. Keep `archive_closeout_delivery_index.json` as the machine-readable final closeout index.

## Best Practice

Use this helper as the final command reference for archive closeout delivery indexing. It gives reviewers and owners the exact command needed to recreate the final delivery index from the closeout record set.
