# Archive Closeout Package Completion Guide

This guide documents the `archive_closeout_package_completion.py` builder for OpenMontage Plus archive governance.

Use it after the delivery acceptance report has been generated. It creates the final package completion record for the archive closeout delivery package.

## Purpose

The archive closeout package completion builder converts the delivery acceptance result into a final package completion state.

It checks that:

- `archive_closeout_delivery_acceptance.json` exists
- the file loads correctly as JSON
- `acceptance_status` is `accepted`

If the delivery acceptance is accepted, the package completion record reports `complete`. If not, it reports `blocked` and lists the blocker.

## Command

```bash
python extras/archive_closeout_package_completion.py --acceptance archive_closeout_delivery_acceptance.json --owner "Archive Owner" --reviewer "Archive Reviewer" --label archive-closeout-package-completion --out-json archive_closeout_package_completion.json --out-md ARCHIVE_CLOSEOUT_PACKAGE_COMPLETION.md
```

## Output Files

- `archive_closeout_package_completion.json`
- `ARCHIVE_CLOSEOUT_PACKAGE_COMPLETION.md`

## Status Meaning

- `complete`: delivery acceptance exists, loads correctly, and reports `accepted`.
- `blocked`: delivery acceptance is missing, invalid, or not accepted.

## Suggested Workflow

1. Generate delivery seal.
2. Generate delivery index.
3. Generate delivery check.
4. Generate delivery acceptance.
5. Confirm delivery acceptance status is `accepted`.
6. Run the package completion builder.
7. Confirm package completion status is `complete`.
8. Store the JSON and Markdown completion records with the final archive package.
9. Move the package to archival storage after reviewer signoff.

## Reviewer Checklist

Before marking package completion final, confirm:

- delivery acceptance JSON is present
- delivery acceptance status is `accepted`
- package completion status is `complete`
- owner and reviewer names are correct
- no blockers are listed
- Markdown completion report is included in the final archive package

## Best Practice

Use the package completion record as the final closeout checkpoint. It should sit after delivery acceptance and act as the final package-ready record before archival storage or external handoff.
