# Archive Governance Closeout Summary Operations

This operations note documents the `archive_governance_final_closeout_summary.py` builder for OpenMontage Plus archive governance.

Use it after the closeout index has been generated and the index reports `closeout-ready`.

## Purpose

The closeout summary builder converts the detailed closeout index into a short reviewer note.

It summarizes:

- closeout index source
- index load status
- index readiness status
- closure certificate status
- total indexed files
- required files
- existing files
- missing required file count
- invalid JSON file count
- reviewer note
- next steps

## Command

```bash
python extras/archive_governance_final_closeout_summary.py --index archive_governance_final_closeout_index.json --title "Archive Governance Final Closeout Summary" --owner "Archive Owner" --out-json archive_governance_final_closeout_summary.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_SUMMARY.md
```

## Output Files

- `archive_governance_final_closeout_summary.json`
- `ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_SUMMARY.md`

## Status Meaning

- `complete`: the closeout index loaded successfully and has `index_status` set to `closeout-ready`.
- `needs-attention`: the closeout index is missing, invalid, or not closeout-ready.

## Suggested Review Order

1. Generate the closeout index.
2. Confirm the index status is `closeout-ready`.
3. Run `archive_governance_final_closeout_summary.py`.
4. Confirm the summary status is `complete`.
5. Store the summary Markdown with the archive governance package.
6. Use the summary as the short reviewer note after the detailed closeout index.

## Best Practice

Keep this summary next to the closeout index. The index gives file-level proof, while the summary gives a quick reviewer-ready status view.
