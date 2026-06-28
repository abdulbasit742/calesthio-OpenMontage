# Archive Governance Final Closeout Index Audit Note

This note records the audit coverage point for the final archive governance closeout index flow.

## Purpose

Use this note to confirm that the final closeout index builder and its operator documentation are included in the final archive governance package.

The final closeout index flow should verify that these files exist before the archive governance delivery is considered package-closeout-ready:

- `extras/archive_governance_final_closeout_index.py`
- `docs/ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX_GUIDE.md`
- `extras/archive_governance_final_closeout_index_cli.py`
- `docs/ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX_CLI_GUIDE.md`

## Recommended Check

Run the CLI companion to inspect the closeout index tool metadata and generate the exact closeout index command.

```bash
python extras/archive_governance_final_closeout_index_cli.py show
python extras/archive_governance_final_closeout_index_cli.py command --label archive-governance-final-closeout --owner "Archive Owner" --out-json archive_governance_final_closeout_index.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md
```

## Expected Outputs

- `archive_governance_final_closeout_index.json`
- `ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md`

## Audit Result

The final closeout index step is considered covered when the builder, guide, CLI companion, CLI guide, generated closeout index JSON, and generated closeout index Markdown are all present in the final archive package.
