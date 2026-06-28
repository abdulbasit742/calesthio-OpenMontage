# Archive Governance Final Closure Certificate Audit Note

This note records the audit coverage point for the final archive governance closure certificate flow.

## Purpose

Use this note to confirm that the final closure certificate builder and its operator documentation are included in the final archive governance package.

The final closure certificate flow should verify that these files exist before the archive governance delivery is considered fully closed:

- `extras/archive_governance_final_closure_certificate.py`
- `docs/ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE_GUIDE.md`
- `extras/archive_governance_final_closure_certificate_cli.py`
- `docs/ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE_CLI_GUIDE.md`

## Recommended Check

Run the CLI companion to inspect the closure certificate tool metadata and generate the exact closure command.

```bash
python extras/archive_governance_final_closure_certificate_cli.py show
python extras/archive_governance_final_closure_certificate_cli.py command --acknowledgement archive_governance_final_delivery_acknowledgement.json --certificate-id archive-governance-final-closure --owner "Archive Owner" --closing-note "Final archive governance delivery is closed after reviewer acknowledgement." --out-json archive_governance_final_closure_certificate.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md
```

## Expected Outputs

- `archive_governance_final_closure_certificate.json`
- `ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md`

## Audit Result

The final closure certificate step is considered covered when the builder, guide, CLI companion, CLI guide, generated certificate JSON, and generated certificate Markdown are all present in the final archive package.
