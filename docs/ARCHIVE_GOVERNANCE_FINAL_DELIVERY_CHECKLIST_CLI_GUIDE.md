# Archive Governance Final Delivery Checklist CLI Guide

This guide documents the `archive_governance_final_delivery_checklist_cli.py` companion helper for OpenMontage Plus archive governance.

Use it when you want a quick way to inspect or generate the final delivery checklist builder command without manually typing the full script path.

## Purpose

The final delivery checklist CLI companion provides a small command registry for the archive governance final delivery checklist builder.

It helps reviewers and operators:

- inspect final delivery checklist tool metadata
- confirm the target script exists
- generate a runnable final delivery checklist command
- see the expected JSON and Markdown outputs
- keep the final archive delivery gate consistent

## Available Commands

```bash
python extras/archive_governance_final_delivery_checklist_cli.py show
python extras/archive_governance_final_delivery_checklist_cli.py list
python extras/archive_governance_final_delivery_checklist_cli.py command --packet archive_governance_final_packet.json --handoff archive_governance_final_handoff_note.json --label archive-governance-final-delivery --out-json archive_governance_final_delivery_checklist.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md
```

## Target Script

```text
extras/archive_governance_final_delivery_checklist.py
```

## Output Files

- `archive_governance_final_delivery_checklist.json`
- `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md`

## Suggested Workflow

1. Generate the final governance packet.
2. Generate the final handoff note.
3. Run `python extras/archive_governance_final_delivery_checklist_cli.py show` to verify the checklist tool metadata.
4. Run the `command` helper to produce the full checklist command.
5. Execute the generated command.
6. Review `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md` before archive delivery.

## Best Practice

Use the CLI companion during final delivery so the next reviewer can quickly find and run the exact final delivery checklist command.
