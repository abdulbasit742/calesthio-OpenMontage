# Archive Toolchain Governance Audit Guide

This guide documents the expanded `archive_toolchain_audit.py` coverage for the OpenMontage Plus archive and governance workflow.

Use it to confirm that core archive tools, portfolio workflow files, governance scripts, governance guides, packet files, and approval record support are present before final delivery.

## Purpose

The governance audit helps archive owners verify that the latest archive toolchain is complete. It checks both scripts and documentation so the final workflow can be generated, reviewed, packaged, and approved consistently.

It reports:

- total expected file count
- available file count
- missing file count
- script count
- docs count
- governance file count
- governance missing count
- keyword hits for delivery, handoff, feedback, closeout, archive, portfolio, governance, packet, and approval

## Command

```bash
python extras/archive_toolchain_audit.py --out-json archive_toolchain_audit.json --out-md ARCHIVE_TOOLCHAIN_AUDIT.md
```

## Output Files

- `archive_toolchain_audit.json`
- `ARCHIVE_TOOLCHAIN_AUDIT.md`

## What The Audit Covers

The audit now includes governance coverage for:

- governance summary script and guide
- governance action tracker script and guide
- governance board script and guide
- governance packet script and guide
- governance approval record script and guide
- archive portfolio runbook
- archive portfolio operations guide
- archive toolchain CLI registry

## Status Meaning

- `passed`: all expected archive and governance files exist.
- `needs-attention`: one or more expected files are missing.

## Suggested Review Order

1. Run the audit command.
2. Open `ARCHIVE_TOOLCHAIN_AUDIT.md`.
3. Check `Missing files` and `Governance missing` counts.
4. If anything is missing, restore or regenerate the file.
5. Run `python extras/archive_toolchain_cli.py list --area portfolio`.
6. Run the portfolio runbook after audit passes.

## Best Practice

Run this audit before generating the final archive portfolio runbook. It gives one quick readiness check before the governance summary, tracker, board, packet, and approval record are produced.
