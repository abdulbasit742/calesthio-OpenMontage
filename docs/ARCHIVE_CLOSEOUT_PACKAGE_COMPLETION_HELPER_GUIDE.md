# Archive Closeout Package Completion Helper Guide

This guide documents the `archive_closeout_package_completion_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the final package completion builder metadata or generate the package completion command without manually typing the script path.

## Purpose

The archive closeout package completion helper provides a small command registry for the final package completion builder.

It helps archive operators and reviewers:

- inspect package completion tool metadata
- confirm the target package completion builder exists
- generate a runnable final package completion command
- see the expected JSON and Markdown package completion outputs
- keep completion commands consistent across final archive package reviews

## Available Commands

```bash
python extras/archive_closeout_package_completion_helper.py show
python extras/archive_closeout_package_completion_helper.py list
python extras/archive_closeout_package_completion_helper.py command --acceptance archive_closeout_delivery_acceptance.json --owner "Archive Owner" --reviewer "Archive Reviewer" --label archive-closeout-package-completion --out-json archive_closeout_package_completion.json --out-md ARCHIVE_CLOSEOUT_PACKAGE_COMPLETION.md
```

## Target Script

```text
extras/archive_closeout_package_completion.py
```

## Output Files

- `archive_closeout_package_completion.json`
- `ARCHIVE_CLOSEOUT_PACKAGE_COMPLETION.md`

## Suggested Workflow

1. Generate the delivery seal report.
2. Generate the delivery index report.
3. Generate the delivery check report.
4. Generate the delivery acceptance report.
5. Confirm the delivery acceptance status is `accepted`.
6. Run `python extras/archive_closeout_package_completion_helper.py show` to verify helper metadata.
7. Run the `command` helper to produce the full package completion builder command.
8. Execute the generated command.
9. Confirm package completion status is `complete`.
10. Store `ARCHIVE_CLOSEOUT_PACKAGE_COMPLETION.md` with the final archive package.
11. Keep `archive_closeout_package_completion.json` as the machine-readable final completion record.

## Best Practice

Use this helper as the final command reference for archive closeout package completion. It gives reviewers and owners the exact command needed to recreate the final completion record from an accepted delivery acceptance report.
