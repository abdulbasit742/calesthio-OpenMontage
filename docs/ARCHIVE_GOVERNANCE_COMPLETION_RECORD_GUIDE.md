# Archive Governance Completion Record Guide

This guide documents the `archive_governance_completion_record.py` workflow for OpenMontage Plus archive governance.

Use it after the archive governance readiness summary has been generated and reviewed.

## Purpose

The completion record is the final governance closeout document. It confirms whether the archive governance package is complete or still needs attention.

It reads the readiness summary and creates a clear owner-facing record with:

- completion status
- owner name
- review note
- readiness source
- readiness status
- metrics
- blockers
- next steps

## Input File

The default input is:

```text
archive_governance_readiness_summary.json
```

## Command

```bash
python extras/archive_governance_completion_record.py --readiness archive_governance_readiness_summary.json --owner-name "Archive Owner" --note "Final governance readiness reviewed" --out-json archive_governance_completion_record.json --out-md ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md
```

## Output Files

- `archive_governance_completion_record.json`
- `ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md`

## Status Meaning

- `completed`: readiness status is `governance-ready` and no blockers remain.
- `needs-attention`: readiness summary is missing, invalid, not ready, or still has blockers.

## Suggested Review Order

1. Run `archive_toolchain_audit.py`.
2. Run `archive_portfolio_governance_packet.py`.
3. Run `archive_portfolio_governance_approval_record.py`.
4. Run `archive_governance_readiness_summary.py`.
5. Review `ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md`.
6. Run `archive_governance_completion_record.py`.
7. Store `ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md` with the final archive package.

## Best Practice

Use the completion record as the final sign-off artifact for the governance workflow. If it shows `needs-attention`, fix the readiness blockers first and regenerate the completion record.
