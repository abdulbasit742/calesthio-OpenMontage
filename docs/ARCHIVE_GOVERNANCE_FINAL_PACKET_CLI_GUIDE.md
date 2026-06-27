# Archive Governance Final Packet CLI Guide

This guide documents the `archive_governance_final_packet_cli.py` companion helper for OpenMontage Plus archive governance.

Use it when you want a quick way to inspect or generate the final packet builder command without manually typing the full script path.

## Purpose

The final packet CLI companion provides a small command registry for the archive governance final packet builder.

It helps reviewers and operators:

- inspect the final packet tool metadata
- confirm the target script exists
- generate a runnable final packet command
- see the expected JSON and Markdown outputs

## Available Commands

```bash
python extras/archive_governance_final_packet_cli.py show
python extras/archive_governance_final_packet_cli.py list
python extras/archive_governance_final_packet_cli.py command --label archive-governance-final-packet --out-json archive_governance_final_packet.json --out-md ARCHIVE_GOVERNANCE_FINAL_PACKET.md
```

## Target Script

```text
extras/archive_governance_final_packet.py
```

## Output Files

- `archive_governance_final_packet.json`
- `ARCHIVE_GOVERNANCE_FINAL_PACKET.md`

## Suggested Workflow

1. Generate audit, governance packet, approval record, readiness summary, and completion record outputs.
2. Run `python extras/archive_governance_final_packet_cli.py show` to verify the final packet tool metadata.
3. Run the `command` helper to produce the final packet command.
4. Execute the generated command.
5. Review `ARCHIVE_GOVERNANCE_FINAL_PACKET.md` before final delivery.

## Best Practice

Use the CLI companion during handoff so the next reviewer can quickly find and run the exact final packet builder command.
