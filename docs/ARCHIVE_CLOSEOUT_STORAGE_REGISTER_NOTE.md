# Archive Closeout Storage Register Note

This note starts the storage register layer after the storage receipt checkpoint.

## Purpose

The storage register layer gives the archived package a simple register reference after the storage receipt has been recorded.

Use this note after:

- `archive_closeout_storage_handoff.json`
- `archive_closeout_storage_receipt.json`
- `ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md`

## Register Fields

A storage register record should include:

- register ID
- storage receipt ID
- archive package label
- owner
- reviewer
- storage owner
- storage location
- register status
- notes for future lookup

## Suggested Status Values

- `registered`: storage receipt is available and the package has been logged in the storage register.
- `blocked`: storage receipt is missing, invalid, or not ready to be logged.

## Suggested Workflow

1. Generate the storage receipt.
2. Confirm storage receipt status is `received`.
3. Assign a register ID.
4. Add the register ID to the archive package index.
5. Store this note with the closeout package.
6. Ask the storage owner to confirm that the package can be located by register ID.

## Package Note

Keep the register ID beside the storage receipt so future reviewers can trace where the archive package was stored and how it can be located again.
