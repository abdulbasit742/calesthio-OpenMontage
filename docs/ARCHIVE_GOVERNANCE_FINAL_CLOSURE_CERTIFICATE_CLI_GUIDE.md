# Archive Governance Final Closure Certificate CLI Guide

This guide documents the `archive_governance_final_closure_certificate_cli.py` companion helper for OpenMontage Plus archive governance.

Use it when you want a quick way to inspect or generate the final closure certificate builder command without manually typing the full script path.

## Purpose

The final closure certificate CLI companion provides a small command registry for the archive governance final closure certificate builder.

It helps operators and reviewers:

- inspect final closure certificate tool metadata
- confirm the target script exists
- generate a runnable final closure certificate command
- see the expected JSON and Markdown certificate outputs
- keep final governance closeout consistent

## Available Commands

```bash
python extras/archive_governance_final_closure_certificate_cli.py show
python extras/archive_governance_final_closure_certificate_cli.py list
python extras/archive_governance_final_closure_certificate_cli.py command --acknowledgement archive_governance_final_delivery_acknowledgement.json --certificate-id archive-governance-final-closure --owner "Archive Owner" --closing-note "Final archive governance delivery is closed after reviewer acknowledgement." --out-json archive_governance_final_closure_certificate.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md
```

## Target Script

```text
extras/archive_governance_final_closure_certificate.py
```

## Output Files

- `archive_governance_final_closure_certificate.json`
- `ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md`

## Suggested Workflow

1. Generate the final delivery acknowledgement.
2. Confirm the acknowledgement status is `acknowledged`.
3. Run `python extras/archive_governance_final_closure_certificate_cli.py show` to verify closure certificate metadata.
4. Run the `command` helper to produce the full closure certificate command.
5. Execute the generated command.
6. Confirm the closure certificate status is `closed`.
7. Store `ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md` with the final archive package.

## Best Practice

Use the CLI companion during final closeout so the next reviewer can quickly find and run the exact final closure certificate command.
