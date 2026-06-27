# Archive Governance Final Packet Guide

This guide documents the `archive_governance_final_packet.py` builder for OpenMontage Plus archive governance.

Use it after audit, governance packet, approval record, readiness summary, and completion record outputs have been generated.

## Purpose

The final packet builder creates the last governance packet manifest. It checks that the important final governance source files exist and that the completion record is marked completed.

It helps reviewers confirm:

- required audit outputs are present
- governance packet outputs are present
- approval record outputs are present
- readiness summary outputs are present
- completion record outputs are present
- source JSON statuses are readable
- blockers are visible before final delivery

## Command

```bash
python extras/archive_governance_final_packet.py --label archive-governance-final-packet --out-json archive_governance_final_packet.json --out-md ARCHIVE_GOVERNANCE_FINAL_PACKET.md
```

## Output Files

- `archive_governance_final_packet.json`
- `ARCHIVE_GOVERNANCE_FINAL_PACKET.md`

## Status Meaning

- `final-packet-ready`: all included files exist and the completion record status is `completed`.
- `needs-attention`: required files are missing, the completion record is not completed, or source statuses show blockers.

## Default Included Files

The default packet includes audit, governance packet, approval record, readiness summary, completion record, and completion CLI guide files.

You can override the included files with:

```bash
python extras/archive_governance_final_packet.py --include file1.json file2.md --out-json archive_governance_final_packet.json --out-md ARCHIVE_GOVERNANCE_FINAL_PACKET.md
```

## Suggested Review Order

1. Run `archive_toolchain_audit.py`.
2. Run `archive_portfolio_governance_packet.py`.
3. Run `archive_portfolio_governance_approval_record.py`.
4. Run `archive_governance_readiness_summary.py`.
5. Run `archive_governance_completion_record.py`.
6. Run `archive_governance_final_packet.py`.
7. Review `ARCHIVE_GOVERNANCE_FINAL_PACKET.md`.
8. Store the final packet with the archive delivery package.

## Best Practice

Treat `ARCHIVE_GOVERNANCE_FINAL_PACKET.md` as the final governance delivery manifest. If it shows `needs-attention`, fix the listed blockers and regenerate the packet before handoff.
