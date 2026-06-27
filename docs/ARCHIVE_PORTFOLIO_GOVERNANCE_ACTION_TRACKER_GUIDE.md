# Archive Portfolio Governance Action Tracker Guide

This guide documents the final `portfolio-governance-action-tracker` step for the OpenMontage Plus archive portfolio workflow.

Use it after this file is generated:

- `archive_portfolio_governance_summary.json`

## Purpose

The action tracker converts governance summary actions into a clean owner-facing table. It helps archive owners track what is still open after the governance summary is created.

It reports:

- action IDs such as `GOV-001`
- priority level
- owner name
- open status
- action text
- notes column for manual follow-up

## Command

```bash
python extras/archive_portfolio_governance_action_tracker.py --summary archive_portfolio_governance_summary.json --owner-name "Archive Owner" --out-json archive_portfolio_governance_action_tracker.json --out-md ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER.md
```

## Output Files

- `archive_portfolio_governance_action_tracker.json`
- `ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER.md`

## CLI Registry Commands

```bash
python extras/archive_toolchain_cli.py show portfolio-governance-action-tracker
python extras/archive_toolchain_cli.py command portfolio-governance-action-tracker --summary archive_portfolio_governance_summary.json --owner-name ArchiveOwner
python extras/archive_toolchain_cli.py list --area portfolio
```

## Priority Rules

The tracker sets priority automatically:

- `high`: action mentions missing, failed, non-ready, attention, or invalid.
- `medium`: action mentions review, approve, or schedule.
- `normal`: all other actions.

## Suggested Review Order

1. Review `ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY.md`.
2. Run the action tracker command.
3. Review `ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER.md`.
4. Assign or update owners if needed.
5. Update status and notes as actions are completed.
6. Keep the tracker with the final archive governance files.

## Best Practice

Run this tracker at the end of the archive workflow. It is not a replacement for the governance summary; it is a follow-up list for the owner or team responsible for final archive governance.
