# Archive Governance Completion CLI Guide

This guide documents the `archive_governance_completion_cli.py` companion helper for OpenMontage Plus archive governance.

Use it when you want a quick way to inspect or generate the completion record command without manually typing the full script path.

## Purpose

The completion CLI companion provides a small command registry for the final archive governance completion record.

It helps reviewers and operators:

- inspect the completion record tool metadata
- confirm the target script exists
- generate a runnable completion record command
- see the expected JSON and Markdown outputs

## Available Commands

```bash
python extras/archive_governance_completion_cli.py show
python extras/archive_governance_completion_cli.py list
python extras/archive_governance_completion_cli.py command --readiness archive_governance_readiness_summary.json --owner-name ArchiveOwner --note "Final governance readiness reviewed"
```

## Target Script

```text
extras/archive_governance_completion_record.py
```

## Output Files

- `archive_governance_completion_record.json`
- `ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md`

## Suggested Workflow

1. Generate the governance readiness summary.
2. Run `python extras/archive_governance_completion_cli.py show` to verify the completion tool metadata.
3. Run the `command` helper to produce the final completion command.
4. Execute the generated command.
5. Store `ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md` with the final governance package.

## Best Practice

Use the CLI companion when handing the workflow to another reviewer. It gives them a simple and consistent way to find the correct completion record command.
