# Archive Governance Final Delivery Receipt Guide

This guide documents the `archive_governance_final_delivery_receipt.py` builder for OpenMontage Plus archive governance.

Use it after the final delivery checklist has been generated and its status is `delivery-ready`.

## Purpose

The final delivery receipt builder creates reviewer-facing proof that the archive governance package was delivered.

It records:

- package ID
- sender name
- recipient name
- delivery note
- final delivery checklist source
- checklist status
- passed and failed check counts
- receipt status
- next steps for reviewer acknowledgement

## Command

```bash
python extras/archive_governance_final_delivery_receipt.py --checklist archive_governance_final_delivery_checklist.json --sender "Archive Owner" --recipient "Archive Reviewer" --package-id archive-governance-final-package --note "Final archive governance package delivered for reviewer acknowledgement." --out-json archive_governance_final_delivery_receipt.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_RECEIPT.md
```

## Output Files

- `archive_governance_final_delivery_receipt.json`
- `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_RECEIPT.md`

## Status Meaning

- `delivered`: the final delivery checklist loaded successfully and its status is `delivery-ready`.
- `needs-attention`: the checklist is missing, invalid, not delivery-ready, or contains failed checks.

## Suggested Review Order

1. Run `archive_governance_final_packet.py`.
2. Run `archive_governance_final_handoff_note.py`.
3. Run `archive_governance_final_delivery_checklist.py`.
4. Confirm the checklist status is `delivery-ready`.
5. Run `archive_governance_final_delivery_receipt.py`.
6. Store the receipt with the final packet, handoff note, and checklist.
7. Ask the archive reviewer to acknowledge receipt.

## Best Practice

Treat this receipt as the final delivery proof. Do not mark the archive governance package as delivered until the receipt status is `delivered`.
