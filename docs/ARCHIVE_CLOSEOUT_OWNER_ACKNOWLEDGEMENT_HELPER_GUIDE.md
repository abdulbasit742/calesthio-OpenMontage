# Archive Closeout Owner Acknowledgement Helper Guide

This guide documents the `archive_closeout_owner_acknowledgement_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the owner acknowledgement builder metadata or generate the final owner acknowledgement command without manually typing the script path.

## Purpose

The archive closeout owner acknowledgement helper provides a small command registry for the final owner signoff builder.

It helps archive operators and reviewers:

- inspect owner acknowledgement tool metadata
- confirm the target acknowledgement builder exists
- generate a runnable owner acknowledgement command
- see the expected JSON and Markdown acknowledgement outputs
- keep final owner-signoff commands consistent

## Available Commands

```bash
python extras/archive_closeout_owner_acknowledgement_helper.py show
python extras/archive_closeout_owner_acknowledgement_helper.py list
python extras/archive_closeout_owner_acknowledgement_helper.py command --checklist archive_closeout_handoff_checklist.json --owner "Archive Owner" --reviewer "Archive Reviewer" --decision acknowledge --label archive-closeout-owner-acknowledgement --out-json archive_closeout_owner_acknowledgement.json --out-md ARCHIVE_CLOSEOUT_OWNER_ACKNOWLEDGEMENT.md
```

## Target Script

```text
extras/archive_closeout_owner_acknowledgement.py
```

## Output Files

- `archive_closeout_owner_acknowledgement.json`
- `ARCHIVE_CLOSEOUT_OWNER_ACKNOWLEDGEMENT.md`

## Suggested Workflow

1. Generate the final archive closeout handoff checklist.
2. Confirm the handoff checklist status is `ready`.
3. Run `python extras/archive_closeout_owner_acknowledgement_helper.py show` to verify helper metadata.
4. Run the `command` helper to produce the full owner acknowledgement builder command.
5. Execute the generated command.
6. Confirm acknowledgement status is `acknowledged`.
7. Store `ARCHIVE_CLOSEOUT_OWNER_ACKNOWLEDGEMENT.md` with the final archive package.
8. Keep `archive_closeout_owner_acknowledgement.json` as the machine-readable owner signoff record.

## Best Practice

Use this helper as the final command reference for archive owner signoff. It gives reviewers and owners the exact command needed to recreate the owner acknowledgement from the handoff checklist checkpoint.
