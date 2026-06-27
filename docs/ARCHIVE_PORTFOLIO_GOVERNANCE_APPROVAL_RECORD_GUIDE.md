# Archive Portfolio Governance Approval Record Guide

This guide documents the final `portfolio-governance-approval-record` step for the OpenMontage Plus archive portfolio workflow.

Use it after the governance packet is generated:

- `archive_portfolio_governance_packet.json`
- `ARCHIVE_PORTFOLIO_GOVERNANCE_PACKET.md`

## Purpose

The governance approval record is the final reviewer-facing check for the governance package. It reads the governance packet JSON and confirms whether the packet is ready for approval.

It checks:

- packet JSON exists
- packet status is `governance-packet-ready`
- no governance files are missing
- no attention sources remain
- reviewer name, reviewer role, and review note are captured

## Command

```bash
python extras/archive_portfolio_governance_approval_record.py --packet archive_portfolio_governance_packet.json --reviewer-name "Archive Owner" --reviewer-role "Owner" --review-note "Governance package reviewed" --out-json archive_portfolio_governance_approval_record.json --out-md ARCHIVE_PORTFOLIO_GOVERNANCE_APPROVAL_RECORD.md
```

## Output Files

- `archive_portfolio_governance_approval_record.json`
- `ARCHIVE_PORTFOLIO_GOVERNANCE_APPROVAL_RECORD.md`

## CLI Registry Commands

```bash
python extras/archive_toolchain_cli.py show portfolio-governance-approval-record
python extras/archive_toolchain_cli.py command portfolio-governance-approval-record --packet archive_portfolio_governance_packet.json --reviewer-name ArchiveOwner --reviewer-role Owner
python extras/archive_toolchain_cli.py list --area portfolio
```

## Status Meaning

- `approved`: the governance packet is ready, no files are missing, and no attention sources remain.
- `needs-attention`: the governance packet is missing, invalid, not ready, or still has unresolved items.

## Suggested Review Order

1. Generate the governance summary.
2. Generate the governance action tracker.
3. Generate the governance board.
4. Generate the governance packet.
5. Run the governance approval record command.
6. Review `ARCHIVE_PORTFOLIO_GOVERNANCE_APPROVAL_RECORD.md`.
7. If status is `needs-attention`, fix issues and rerun the packet and approval record.
8. If status is `approved`, keep the approval record with the final archive package.

## Best Practice

Run the approval record as the last governance step. It should be stored with the archive package so reviewers can confirm who reviewed the governance packet and whether the final package was approved.
