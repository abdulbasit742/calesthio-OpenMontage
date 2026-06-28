# Archive Closeout Handoff Checklist Helper Guide

This guide documents the `archive_closeout_handoff_checklist_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the handoff checklist builder metadata or generate the final handoff checklist command without manually typing the script path.

## Purpose

The archive closeout handoff checklist helper provides a small command registry for the final handoff checklist builder.

It helps archive operators and reviewers:

- inspect handoff checklist tool metadata
- confirm the target checklist builder exists
- generate a runnable handoff checklist command
- see the expected JSON and Markdown checklist outputs
- keep final delivery commands consistent

## Available Commands

```bash
python extras/archive_closeout_handoff_checklist_helper.py show
python extras/archive_closeout_handoff_checklist_helper.py list
python extras/archive_closeout_handoff_checklist_helper.py command --readiness archive_closeout_package_readiness.json --label archive-closeout-handoff-checklist --owner "Archive Owner" --out-json archive_closeout_handoff_checklist.json --out-md ARCHIVE_CLOSEOUT_HANDOFF_CHECKLIST.md
```

## Target Script

```text
extras/archive_closeout_handoff_checklist.py
```

## Output Files

- `archive_closeout_handoff_checklist.json`
- `ARCHIVE_CLOSEOUT_HANDOFF_CHECKLIST.md`

## Suggested Workflow

1. Generate the archive closeout package readiness report.
2. Run `python extras/archive_closeout_handoff_checklist_helper.py show` to verify helper metadata.
3. Run the `command` helper to produce the full handoff checklist builder command.
4. Execute the generated command.
5. Confirm checklist status is `ready`.
6. Store `ARCHIVE_CLOSEOUT_HANDOFF_CHECKLIST.md` with the final archive package.
7. Keep `archive_closeout_handoff_checklist.json` as the machine-readable delivery checklist.

## Best Practice

Use this helper as the final command reference before archive package delivery. It gives reviewers the exact command needed to recreate the handoff checklist from the package readiness checkpoint.
