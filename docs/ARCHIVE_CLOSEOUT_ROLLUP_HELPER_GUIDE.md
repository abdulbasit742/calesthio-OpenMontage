# Archive Closeout Rollup Helper Guide

This guide documents the `archive_closeout_rollup_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect rollup builder metadata or generate the rollup command without manually typing the script path.

## Purpose

The archive closeout rollup helper provides a small command registry for the rollup builder.

It helps operators and reviewers:

- inspect rollup tool metadata
- confirm the target rollup builder exists
- generate a runnable rollup command
- see the expected JSON and Markdown rollup outputs
- keep reviewer checkpoint commands consistent

## Available Commands

```bash
python extras/archive_closeout_rollup_helper.py show
python extras/archive_closeout_rollup_helper.py list
python extras/archive_closeout_rollup_helper.py command --index archive_governance_final_closeout_index.json --summary archive_governance_final_closeout_summary.json --label archive-closeout-rollup --out-json archive_closeout_rollup.json --out-md ARCHIVE_CLOSEOUT_ROLLUP.md
```

## Target Script

```text
extras/archive_closeout_rollup.py
```

## Output Files

- `archive_closeout_rollup.json`
- `ARCHIVE_CLOSEOUT_ROLLUP.md`

## Suggested Workflow

1. Generate the final closeout index.
2. Generate the final closeout summary.
3. Run `python extras/archive_closeout_rollup_helper.py show` to verify helper metadata.
4. Run the `command` helper to produce the full rollup builder command.
5. Execute the generated command.
6. Confirm the rollup status is `ready`.
7. Store `ARCHIVE_CLOSEOUT_ROLLUP.md` with the final archive package.

## Best Practice

Use this helper when handing the final package to another reviewer. It gives them the exact command needed to recreate the rollup from the closeout index and summary.
