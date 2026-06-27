# Archive Portfolio Governance Packet Guide

This guide documents the final `portfolio-governance-packet` step for the OpenMontage Plus archive portfolio workflow.

Use it after these governance outputs are generated:

- `ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY.md`
- `archive_portfolio_governance_summary.json`
- `ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER.md`
- `archive_portfolio_governance_action_tracker.json`
- `ARCHIVE_PORTFOLIO_GOVERNANCE_BOARD.md`
- `archive_portfolio_governance_board.json`

## Purpose

The governance packet creates a final manifest of all governance deliverables. It checks whether the expected markdown files, JSON records, and governance guides are present before the archive package is considered complete.

It reports:

- expected governance files
- available governance files
- missing governance files
- governance summary status
- governance action tracker status
- governance board status
- attention source count
- final packet readiness status

## Command

```bash
python extras/archive_portfolio_governance_packet.py --packet-label archive-portfolio-governance-packet --out-json archive_portfolio_governance_packet.json --out-md ARCHIVE_PORTFOLIO_GOVERNANCE_PACKET.md
```

## Output Files

- `archive_portfolio_governance_packet.json`
- `ARCHIVE_PORTFOLIO_GOVERNANCE_PACKET.md`

## CLI Registry Commands

```bash
python extras/archive_toolchain_cli.py show portfolio-governance-packet
python extras/archive_toolchain_cli.py command portfolio-governance-packet --packet-label archive-portfolio-governance-packet
python extras/archive_toolchain_cli.py list --area portfolio
```

## Status Meaning

- `governance-packet-ready`: all expected files exist and all governance source statuses are ready.
- `needs-attention`: one or more expected files are missing, invalid, or not ready.

## Suggested Review Order

1. Generate the governance summary.
2. Generate the governance action tracker.
3. Generate the governance board.
4. Run the governance packet command.
5. Review `ARCHIVE_PORTFOLIO_GOVERNANCE_PACKET.md`.
6. Fix any missing files or attention sources.
7. Keep the packet manifest with the final archive handoff package.

## Best Practice

Run the governance packet after the board. It should be treated as the final governance packaging checklist before archive delivery, handoff, or long-term storage.
