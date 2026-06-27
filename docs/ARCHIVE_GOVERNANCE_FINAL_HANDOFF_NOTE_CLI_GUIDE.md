# Archive Governance Final Handoff Note CLI Guide

This guide documents the `archive_governance_final_handoff_note_cli.py` companion helper for OpenMontage Plus archive governance.

Use it when you want a quick way to inspect or generate the final handoff note builder command without manually typing the full script path.

## Purpose

The final handoff note CLI companion provides a small command registry for the archive governance final handoff note builder.

It helps reviewers and operators:

- inspect final handoff note tool metadata
- confirm the target script exists
- generate a runnable handoff note command
- see the expected JSON and Markdown outputs
- keep the final reviewer handoff flow consistent

## Available Commands

```bash
python extras/archive_governance_final_handoff_note_cli.py show
python extras/archive_governance_final_handoff_note_cli.py list
python extras/archive_governance_final_handoff_note_cli.py command --packet archive_governance_final_packet.json --sender-name "Archive Owner" --recipient-name "Archive Reviewer" --note "Final archive governance packet is ready for review." --out-json archive_governance_final_handoff_note.json --out-md ARCHIVE_GOVERNANCE_FINAL_HANDOFF_NOTE.md
```

## Target Script

```text
extras/archive_governance_final_handoff_note.py
```

## Output Files

- `archive_governance_final_handoff_note.json`
- `ARCHIVE_GOVERNANCE_FINAL_HANDOFF_NOTE.md`

## Suggested Workflow

1. Generate the final governance packet.
2. Run `python extras/archive_governance_final_handoff_note_cli.py show` to verify the handoff note tool metadata.
3. Run the `command` helper to produce the full handoff note command.
4. Execute the generated command.
5. Review `ARCHIVE_GOVERNANCE_FINAL_HANDOFF_NOTE.md` before giving the package to the archive reviewer.

## Best Practice

Use the CLI companion during final delivery so the next reviewer can quickly find and run the exact final handoff note command.
