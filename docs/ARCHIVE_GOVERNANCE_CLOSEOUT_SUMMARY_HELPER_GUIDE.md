# Archive Governance Closeout Summary Helper Guide

This guide documents the `archive_governance_closeout_summary_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect the closeout summary builder metadata or generate its runnable command without manually typing the target script path.

## Purpose

The closeout summary helper provides a small command registry for the closeout summary builder.

It helps operators and reviewers:

- inspect the closeout summary tool metadata
- confirm the target builder script exists
- generate a runnable closeout summary command
- see the expected JSON and Markdown summary outputs
- keep reviewer handoff commands consistent

## Available Commands

```bash
python extras/archive_governance_closeout_summary_helper.py show
python extras/archive_governance_closeout_summary_helper.py list
python extras/archive_governance_closeout_summary_helper.py command --index archive_governance_final_closeout_index.json --title "Archive Governance Final Closeout Summary" --owner "Archive Owner" --out-json archive_governance_final_closeout_summary.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_SUMMARY.md
```

## Target Script

```text
extras/archive_governance_final_closeout_summary.py
```

## Output Files

- `archive_governance_final_closeout_summary.json`
- `ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_SUMMARY.md`

## Suggested Workflow

1. Generate the final closeout index.
2. Confirm the closeout index status is `closeout-ready`.
3. Run `python extras/archive_governance_closeout_summary_helper.py show` to verify helper metadata.
4. Run the `command` helper to produce the full summary builder command.
5. Execute the generated command.
6. Confirm the closeout summary status is `complete`.
7. Store `ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_SUMMARY.md` with the final archive package.

## Best Practice

Use this helper when handing the package to another reviewer. It gives them the exact command needed to recreate the executive closeout summary from the closeout index.
