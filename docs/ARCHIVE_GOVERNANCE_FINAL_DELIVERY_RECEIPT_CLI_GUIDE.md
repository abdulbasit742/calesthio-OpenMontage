# Archive Governance Final Delivery Receipt CLI Guide

This guide documents the `archive_governance_final_delivery_receipt_cli.py` companion helper for OpenMontage Plus archive governance.

Use it when you want a quick way to inspect or generate the final delivery receipt builder command without manually typing the full script path.

## Purpose

The final delivery receipt CLI companion provides a small command registry for the archive governance final delivery receipt builder.

It helps reviewers and operators:

- inspect final delivery receipt tool metadata
- confirm the target script exists
- generate a runnable final delivery receipt command
- see the expected JSON and Markdown receipt outputs
- keep the reviewer acknowledgement flow consistent

## Available Commands

```bash
python extras/archive_governance_final_delivery_receipt_cli.py show
python extras/archive_governance_final_delivery_receipt_cli.py list
python extras/archive_governance_final_delivery_receipt_cli.py command --checklist archive_governance_final_delivery_checklist.json --sender "Archive Owner" --recipient "Archive Reviewer" --package-id archive-governance-final-package --note "Final archive governance package delivered for reviewer acknowledgement." --out-json archive_governance_final_delivery_receipt.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_RECEIPT.md
```

## Target Script

```text
extras/archive_governance_final_delivery_receipt.py
```

## Output Files

- `archive_governance_final_delivery_receipt.json`
- `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_RECEIPT.md`

## Suggested Workflow

1. Generate the final governance packet.
2. Generate the final handoff note.
3. Generate the final delivery checklist.
4. Confirm the checklist status is `delivery-ready`.
5. Run `python extras/archive_governance_final_delivery_receipt_cli.py show` to verify receipt tool metadata.
6. Run the `command` helper to produce the full receipt command.
7. Execute the generated command.
8. Store `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_RECEIPT.md` with the final archive package.

## Best Practice

Use the CLI companion during final delivery so the next reviewer can quickly find and run the exact final delivery receipt command.
