# Archive Governance Final Closeout Index Guide

This guide documents the `archive_governance_final_closeout_index.py` builder for OpenMontage Plus archive governance.

Use it after the final closure certificate has been generated and its closure status is `closed`.

## Purpose

The final closeout index builder creates a package table of contents for the completed archive governance delivery workflow.

It verifies and records:

- final governance packet
- final handoff note
- final delivery checklist
- final delivery receipt
- final delivery acknowledgement
- final closure certificate JSON
- final closure certificate Markdown
- missing required files
- invalid JSON files
- final closeout readiness status

## Command

```bash
python extras/archive_governance_final_closeout_index.py --label archive-governance-final-closeout --owner "Archive Owner" --out-json archive_governance_final_closeout_index.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md
```

## Output Files

- `archive_governance_final_closeout_index.json`
- `ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md`

## Status Meaning

- `closeout-ready`: all required package files exist, no required JSON file is invalid, and the final closure certificate has `closure_status` set to `closed`.
- `needs-attention`: at least one required file is missing, invalid JSON is found, or the final closure certificate is not closed.

## Suggested Closeout Order

1. Generate the final governance packet.
2. Generate the final handoff note.
3. Generate the final delivery checklist.
4. Generate the final delivery receipt.
5. Generate the final delivery acknowledgement.
6. Generate the final closure certificate.
7. Confirm the closure certificate status is `closed`.
8. Run `archive_governance_final_closeout_index.py`.
9. Store the closeout index with the final archive package.

## Best Practice

Use this index as the final archive package table of contents. It should be the first file a reviewer opens when checking whether the archive governance delivery is fully closed.
