# Archive Governance Final Delivery Checklist Guide

This guide documents the `archive_governance_final_delivery_checklist.py` builder for OpenMontage Plus archive governance.

Use it after the final governance packet and final handoff note have both been generated.

## Purpose

The final delivery checklist builder creates the last delivery gate before archive governance handoff.

It confirms:

- the final governance packet JSON can be loaded
- the final governance packet status is `final-packet-ready`
- the final handoff note JSON can be loaded
- the final handoff note status is `ready-to-handoff`
- the final packet has no blockers
- the handoff note has no blockers

## Command

```bash
python extras/archive_governance_final_delivery_checklist.py --packet archive_governance_final_packet.json --handoff archive_governance_final_handoff_note.json --label archive-governance-final-delivery --out-json archive_governance_final_delivery_checklist.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md
```

## Output Files

- `archive_governance_final_delivery_checklist.json`
- `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md`

## Status Meaning

- `delivery-ready`: final packet and handoff note are both ready and no blockers are present.
- `needs-attention`: one or more delivery checks failed.

## Suggested Review Order

1. Run `archive_governance_final_packet.py`.
2. Run `archive_governance_final_handoff_note.py`.
3. Run `archive_governance_final_delivery_checklist.py`.
4. Review `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md`.
5. If status is `delivery-ready`, attach the final packet, handoff note, and checklist to the archive delivery package.
6. If status is `needs-attention`, resolve the failed checks and regenerate the outputs.

## Best Practice

Treat this checklist as the final archive governance delivery gate. Do not deliver the archive package until the checklist status is `delivery-ready`.
