# Archive Closeout Storage Handoff Guide

This guide documents the `archive_closeout_storage_handoff.py` builder for OpenMontage Plus archive governance.

Use it after the package completion report has been generated. It creates the storage handoff record for the final archive closeout package.

## Purpose

The archive closeout storage handoff builder converts the package completion result into a storage-ready handoff state.

It checks that:

- `archive_closeout_package_completion.json` exists
- the file loads correctly as JSON
- `package_completion_status` is `complete`

If the package completion status is complete, the storage handoff record reports `ready-for-storage`. If not, it reports `blocked` and lists the blocker.

## Command

```bash
python extras/archive_closeout_storage_handoff.py --completion archive_closeout_package_completion.json --owner "Archive Owner" --reviewer "Archive Reviewer" --storage-owner "Storage Owner" --storage-location "Approved Archive Storage" --label archive-closeout-storage-handoff --out-json archive_closeout_storage_handoff.json --out-md ARCHIVE_CLOSEOUT_STORAGE_HANDOFF.md
```

## Output Files

- `archive_closeout_storage_handoff.json`
- `ARCHIVE_CLOSEOUT_STORAGE_HANDOFF.md`

## Status Meaning

- `ready-for-storage`: package completion exists, loads correctly, and reports `complete`.
- `blocked`: package completion is missing, invalid, or not complete.

## Suggested Workflow

1. Generate delivery seal.
2. Generate delivery index.
3. Generate delivery check.
4. Generate delivery acceptance.
5. Generate package completion.
6. Confirm package completion status is `complete`.
7. Run the storage handoff builder.
8. Confirm storage handoff status is `ready-for-storage`.
9. Copy the final archive package to the approved storage location.
10. Ask the storage owner to confirm receipt.
11. Store the JSON and Markdown handoff records with the archived package.

## Reviewer Checklist

Before marking storage handoff ready, confirm:

- package completion JSON is present
- package completion status is `complete`
- storage handoff status is `ready-for-storage`
- owner, reviewer, storage owner, and storage location are correct
- no blockers are listed
- Markdown storage handoff report is included in the final archive package

## Best Practice

Use the storage handoff record as the final transfer checkpoint before archive storage. It should sit after package completion and act as the formal record that the completed package is ready to be moved into approved archival storage.
