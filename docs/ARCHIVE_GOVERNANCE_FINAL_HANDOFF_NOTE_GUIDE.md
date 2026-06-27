# Archive Governance Final Handoff Note Guide

This guide documents the `archive_governance_final_handoff_note.py` builder for OpenMontage Plus archive governance.

Use it after `archive_governance_final_packet.py` has generated the final governance packet outputs.

## Purpose

The final handoff note builder creates a reviewer-ready note for the final archive governance package.

It helps teams confirm:

- the final packet JSON can be loaded
- the final packet status is visible
- the sender and recipient are recorded
- blockers are clearly shown
- next steps are included for the reviewer
- the final handoff status is easy to understand

## Command

```bash
python extras/archive_governance_final_handoff_note.py --packet archive_governance_final_packet.json --sender-name "Archive Owner" --recipient-name "Archive Reviewer" --note "Final archive governance packet is ready for review." --out-json archive_governance_final_handoff_note.json --out-md ARCHIVE_GOVERNANCE_FINAL_HANDOFF_NOTE.md
```

## Output Files

- `archive_governance_final_handoff_note.json`
- `ARCHIVE_GOVERNANCE_FINAL_HANDOFF_NOTE.md`

## Status Meaning

- `ready-to-handoff`: final packet status is `final-packet-ready` and no blockers are listed.
- `needs-attention`: final packet is missing, invalid, not ready, or contains blockers.

## Suggested Review Order

1. Run `archive_governance_final_packet.py`.
2. Review `ARCHIVE_GOVERNANCE_FINAL_PACKET.md`.
3. Run `archive_governance_final_handoff_note.py`.
4. Share `ARCHIVE_GOVERNANCE_FINAL_HANDOFF_NOTE.md` with the archive reviewer or owner.
5. If the status is `needs-attention`, fix the blockers and regenerate the final packet and handoff note.

## Best Practice

Use the handoff note as the final human-readable cover page for archive governance delivery. It should be stored beside the final governance packet so reviewers can quickly see status, blockers, sender, recipient, and next steps.
