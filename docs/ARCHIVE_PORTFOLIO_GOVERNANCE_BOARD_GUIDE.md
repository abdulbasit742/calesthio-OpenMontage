# Archive Portfolio Governance Board Guide

This guide documents the final `portfolio-governance-board` step for the OpenMontage Plus archive portfolio workflow.

Use it after these files are generated:

- `archive_portfolio_governance_summary.json`
- `archive_portfolio_governance_action_tracker.json`

## Purpose

The governance board combines the governance summary and action tracker into one final status board. It helps owners quickly see whether the governance package is ready or still needs attention.

It reports:

- summary source status
- tracker source status
- missing source count
- attention source count
- failed check count
- total action count
- open action count
- high-priority open action count
- top open governance actions

## Command

```bash
python extras/archive_portfolio_governance_board.py --summary archive_portfolio_governance_summary.json --tracker archive_portfolio_governance_action_tracker.json --out-json archive_portfolio_governance_board.json --out-md ARCHIVE_PORTFOLIO_GOVERNANCE_BOARD.md
```

## Output Files

- `archive_portfolio_governance_board.json`
- `ARCHIVE_PORTFOLIO_GOVERNANCE_BOARD.md`

## CLI Registry Commands

```bash
python extras/archive_toolchain_cli.py show portfolio-governance-board
python extras/archive_toolchain_cli.py command portfolio-governance-board --summary archive_portfolio_governance_summary.json --tracker archive_portfolio_governance_action_tracker.json
python extras/archive_toolchain_cli.py list --area portfolio
```

## Status Meaning

- `governance-board-ready`: summary and tracker files exist, and there are no high-priority open actions.
- `needs-attention`: summary or tracker is missing, or high-priority open actions are still present.

## Suggested Review Order

1. Review `ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY.md`.
2. Review `ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER.md`.
3. Run the governance board command.
4. Review `ARCHIVE_PORTFOLIO_GOVERNANCE_BOARD.md`.
5. Resolve high-priority open actions first.
6. Keep the board with the final governance package.

## Best Practice

Run the governance board as the last reporting step in the archive workflow. It gives archive owners one quick view of governance readiness and unresolved action items.
