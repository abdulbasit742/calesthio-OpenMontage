# Archive Governance Final Closure Certificate Guide

This guide documents the `archive_governance_final_closure_certificate.py` builder for OpenMontage Plus archive governance.

Use it after the final delivery acknowledgement has been generated and its status is `acknowledged`.

## Purpose

The final closure certificate builder creates the last closure proof for the archive governance delivery workflow.

It records:

- certificate ID
- archive owner
- closing note
- acknowledgement source
- acknowledgement status
- package ID
- reviewer name
- reviewer role
- reviewer decision
- closure status
- final next steps

## Command

```bash
python extras/archive_governance_final_closure_certificate.py --acknowledgement archive_governance_final_delivery_acknowledgement.json --certificate-id archive-governance-final-closure --owner "Archive Owner" --closing-note "Final archive governance delivery is closed after reviewer acknowledgement." --out-json archive_governance_final_closure_certificate.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md
```

## Output Files

- `archive_governance_final_closure_certificate.json`
- `ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md`

## Status Meaning

- `closed`: the final acknowledgement loaded successfully and its status is `acknowledged`.
- `needs-attention`: the acknowledgement is missing, invalid, or not acknowledged.

## Suggested Closeout Order

1. Generate the final governance packet.
2. Generate the final handoff note.
3. Generate the final delivery checklist.
4. Generate the final delivery receipt.
5. Generate the reviewer acknowledgement.
6. Confirm the acknowledgement status is `acknowledged`.
7. Run `archive_governance_final_closure_certificate.py`.
8. Store the closure certificate with the final archive package.

## Best Practice

Treat this certificate as the last package-level closeout proof. Do not mark the archive governance delivery as fully closed until this certificate status is `closed`.
