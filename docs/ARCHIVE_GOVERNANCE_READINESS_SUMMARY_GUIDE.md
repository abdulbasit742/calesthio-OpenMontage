# Archive Governance Readiness Summary Guide

This guide documents the `archive_governance_readiness_summary.py` workflow for OpenMontage Plus archive governance.

Use it after the archive toolchain audit and governance approval record are generated.

## Purpose

The readiness summary gives one final governance readiness result by combining two important records:

- `archive_toolchain_audit.json`
- `archive_portfolio_governance_approval_record.json`

It helps reviewers see whether the archive governance workflow is ready or still needs attention before final delivery.

## What It Checks

The summary checks:

- audit status
- governance missing count
- audit missing file count
- approval record status
- governance packet status
- attention source count
- approval record missing file count

## Command

```bash
python extras/archive_governance_readiness_summary.py --audit archive_toolchain_audit.json --approval archive_portfolio_governance_approval_record.json --out-json archive_governance_readiness_summary.json --out-md ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md
```

## Output Files

- `archive_governance_readiness_summary.json`
- `ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md`

## CLI Companion Commands

```bash
python extras/archive_governance_readiness_cli.py show
python extras/archive_governance_readiness_cli.py command --audit archive_toolchain_audit.json --approval archive_portfolio_governance_approval_record.json
python extras/archive_governance_readiness_cli.py list
```

## Status Meaning

- `governance-ready`: audit passed, approval record is approved, and no blockers remain.
- `needs-attention`: audit, packet, approval, or source metrics still need review.

## Suggested Review Order

1. Run `archive_toolchain_audit.py`.
2. Run `archive_portfolio_governance_packet.py`.
3. Run `archive_portfolio_governance_approval_record.py`.
4. Run `archive_governance_readiness_summary.py`.
5. Review `ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md`.
6. If blockers exist, fix them and regenerate the audit, packet, approval record, and readiness summary.

## Best Practice

Use this summary as the last governance readiness checkpoint before final archive delivery. It is intentionally short so a reviewer can quickly confirm whether the archive governance package is ready.
