# Archive Governance Final Closeout Index CLI Guide

This guide documents the `archive_governance_final_closeout_index_cli.py` companion helper for OpenMontage Plus archive governance.

Use it when you want a quick way to inspect or generate the final closeout index builder command without manually typing the full script path.

## Purpose

The final closeout index CLI companion provides a small command registry for the archive governance final closeout index builder.

It helps operators and reviewers:

- inspect final closeout index tool metadata
- confirm the target script exists
- generate a runnable final closeout index command
- see the expected JSON and Markdown index outputs
- keep final package closeout consistent

## Available Commands

```bash
python extras/archive_governance_final_closeout_index_cli.py show
python extras/archive_governance_final_closeout_index_cli.py list
python extras/archive_governance_final_closeout_index_cli.py command --label archive-governance-final-closeout --owner "Archive Owner" --out-json archive_governance_final_closeout_index.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md
```

## Target Script

```text
extras/archive_governance_final_closeout_index.py
```

## Output Files

- `archive_governance_final_closeout_index.json`
- `ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md`

## Suggested Workflow

1. Generate the final closure certificate.
2. Confirm the closure certificate status is `closed`.
3. Run `python extras/archive_governance_final_closeout_index_cli.py show` to verify closeout index metadata.
4. Run the `command` helper to produce the full closeout index command.
5. Execute the generated command.
6. Confirm the closeout index status is `closeout-ready`.
7. Store `ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md` with the final archive package.

## Best Practice

Use the CLI companion during final package closeout so the next reviewer can quickly find and run the exact final closeout index command.
