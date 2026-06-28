# Archive Closeout Delivery Index Guide

This guide documents the `archive_closeout_delivery_index.py` builder for OpenMontage Plus archive governance.

Use it after the final delivery seal has been generated so reviewers can see one index of all closeout JSON and Markdown records.

## Purpose

The archive closeout delivery index builder creates a compact final index of the archive closeout records.

It checks the expected JSON and Markdown files for:

- rollup
- review gate
- milestone manifest
- package readiness
- handoff checklist
- owner acknowledgement
- delivery seal

The builder reports whether every required pair is present.

## Command

```bash
python extras/archive_closeout_delivery_index.py --label archive-closeout-delivery-index --owner "Archive Owner" --out-json archive_closeout_delivery_index.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md
```

## Output Files

- `archive_closeout_delivery_index.json`
- `ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md`

## Status Meaning

- `complete`: all expected JSON and Markdown records are present.
- `incomplete`: one or more expected records are missing.

## Custom Records

You can add custom records with the `--record` option using this format:

```text
name:json_path:markdown_path
```

Example:

```bash
python extras/archive_closeout_delivery_index.py --record delivery_seal:archive_closeout_delivery_seal.json:ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md
```

## Suggested Workflow

1. Generate closeout rollup.
2. Generate review gate.
3. Generate milestone manifest.
4. Generate package readiness.
5. Generate handoff checklist.
6. Generate owner acknowledgement.
7. Generate final delivery seal.
8. Run the delivery index builder.
9. Confirm index status is `complete`.
10. Store the index JSON and Markdown with the final package.

## Best Practice

Use the delivery index as the final reviewer map for archive closeout. It should be stored beside the delivery seal so reviewers can verify the full closeout chain quickly.
