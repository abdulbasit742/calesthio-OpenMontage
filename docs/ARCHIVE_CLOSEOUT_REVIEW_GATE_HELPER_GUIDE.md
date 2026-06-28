# Archive Closeout Review Gate Helper Guide

This guide documents the `archive_closeout_review_gate_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect review gate metadata or generate the review gate command without manually typing the script path.

## Purpose

The archive closeout review gate helper provides a small command registry for the final review gate builder.

It helps operators and reviewers:

- inspect review gate tool metadata
- confirm the target review gate builder exists
- generate a runnable review gate command
- see the expected JSON and Markdown gate outputs
- keep final reviewer approval commands consistent

## Available Commands

```bash
python extras/archive_closeout_review_gate_helper.py show
python extras/archive_closeout_review_gate_helper.py list
python extras/archive_closeout_review_gate_helper.py command --rollup archive_closeout_rollup.json --reviewer "Archive Reviewer" --decision approve --out-json archive_closeout_review_gate.json --out-md ARCHIVE_CLOSEOUT_REVIEW_GATE.md
```

## Target Script

```text
extras/archive_closeout_review_gate.py
```

## Output Files

- `archive_closeout_review_gate.json`
- `ARCHIVE_CLOSEOUT_REVIEW_GATE.md`

## Suggested Workflow

1. Generate the archive closeout rollup.
2. Confirm the rollup status is `ready`.
3. Run `python extras/archive_closeout_review_gate_helper.py show` to verify helper metadata.
4. Run the `command` helper to produce the full review gate builder command.
5. Execute the generated command with `--decision approve` only after reviewer confirmation.
6. Confirm the gate status is `approved`.
7. Store `ARCHIVE_CLOSEOUT_REVIEW_GATE.md` with the final archive package.

## Best Practice

Use this helper as the final command reference during reviewer handoff. It gives the reviewer the exact command needed to recreate the final review gate from the rollup checkpoint.
