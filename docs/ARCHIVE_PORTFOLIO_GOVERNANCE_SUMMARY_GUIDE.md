# Archive Portfolio Governance Summary Guide

This guide documents the final `portfolio-governance-summary` step for the OpenMontage Plus archive portfolio workflow.

Use it after these files are generated:

- `archive_portfolio_retention_review.json`
- `archive_portfolio_retention_policy.json`
- `archive_portfolio_handoff_receipt.json`
- `archive_portfolio_release_packet.json`
- `archive_portfolio_readiness_review.json`

## Purpose

The governance summary creates one short final report for archive owners. It checks the final governance sources and reports:

- overall status
- missing source count
- sources needing attention
- failed check count
- record files to keep together
- final governance actions

## Command

```bash
python extras/archive_portfolio_governance_summary.py --projects-root projects --summary-label archive-portfolio-governance-summary --owner-name "Archive Owner" --out-json archive_portfolio_governance_summary.json --out-md ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY.md
```

## Output Files

- `archive_portfolio_governance_summary.json`
- `ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY.md`

## CLI Registry Commands

```bash
python extras/archive_toolchain_cli.py show portfolio-governance-summary
python extras/archive_toolchain_cli.py command portfolio-governance-summary --projects-root projects --summary-label archive-portfolio-governance-summary --owner-name ArchiveOwner
python extras/archive_toolchain_cli.py list --area portfolio
```

## Suggested Review Order

1. Review `ARCHIVE_PORTFOLIO_READINESS_REVIEW.md`.
2. Review `ARCHIVE_PORTFOLIO_RELEASE_PACKET.md`.
3. Review `ARCHIVE_PORTFOLIO_HANDOFF_RECEIPT.md`.
4. Review `ARCHIVE_PORTFOLIO_RETENTION_POLICY.md`.
5. Review `ARCHIVE_PORTFOLIO_RETENTION_REVIEW.md`.
6. Review `ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY.md`.
7. Keep `ARCHIVE_PORTFOLIO_RUNBOOK.md` as the repeatable workflow reference.

## Status Meaning

- `governance-ready`: final governance sources are present and ready.
- `needs-attention`: at least one governance source is missing, has a non-ready status, or reports failed checks.

## Best Practice

Run the governance summary at the end of the archive workflow. Keep it with the retention review, retention policy, handoff receipt, release packet, and readiness review so the final archive package has one clear owner-facing summary.
