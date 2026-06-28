# Archive Governance Final Delivery Acknowledgement Guide

This guide documents the `archive_governance_final_delivery_acknowledgement.py` builder for OpenMontage Plus archive governance.

Use it after the final delivery receipt has been generated and its status is `delivered`.

## Purpose

The final delivery acknowledgement builder creates reviewer-side proof that the final archive governance package was received and acknowledged.

It records:

- reviewer name
- reviewer role
- decision
- acknowledgement note
- receipt source
- receipt status
- package ID
- sender and recipient
- acknowledgement status
- next steps for final governance closure

## Command

```bash
python extras/archive_governance_final_delivery_acknowledgement.py --receipt archive_governance_final_delivery_receipt.json --reviewer-name "Archive Reviewer" --reviewer-role "Final Delivery Reviewer" --decision acknowledged --note "Reviewer acknowledges receipt of the final archive governance package." --out-json archive_governance_final_delivery_acknowledgement.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_ACKNOWLEDGEMENT.md
```

## Output Files

- `archive_governance_final_delivery_acknowledgement.json`
- `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_ACKNOWLEDGEMENT.md`

## Status Meaning

- `acknowledged`: the receipt loaded successfully, receipt status is `delivered`, and the reviewer decision is `accepted`, `acknowledged`, or `approved`.
- `needs-attention`: the receipt is missing, invalid, not delivered, or the reviewer decision is not accepted.

## Suggested Review Order

1. Generate the final governance packet.
2. Generate the final handoff note.
3. Generate the final delivery checklist.
4. Generate the final delivery receipt.
5. Confirm the receipt status is `delivered`.
6. Run `archive_governance_final_delivery_acknowledgement.py`.
7. Store the acknowledgement with the receipt and final archive package.
8. Mark the archive governance delivery as reviewer-acknowledged.

## Best Practice

Treat this acknowledgement as the final reviewer proof. Do not close the archive governance delivery until the acknowledgement status is `acknowledged`.
