# Archive Register Index Note

This note explains how the register ID should be written into the archive package index.

## Purpose

The package index should point to the register ID so the stored package can be found again without searching through every closeout file.

## Add To Package Index

Add these fields to the package index entry:

- package label
- storage receipt ID
- register ID
- storage owner
- storage location
- index update date
- lookup note

## Required Links

The package index should link back to:

- `archive_closeout_storage_receipt.json`
- `ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md`
- `docs/ARCHIVE_CLOSEOUT_STORAGE_REGISTER_NOTE.md`
- `docs/ARCHIVE_REGISTER_FEATURE_276_279_SUMMARY.md`

## Index Entry Example

```text
Package: OpenMontage archive closeout
Receipt ID: ARCHIVE-STORAGE-RECEIPT-001
Register ID: ARCHIVE-STORAGE-REGISTER-001
Storage Owner: Storage Owner
Storage Location: Approved Archive Storage
```

## Reviewer Check

The index link is ready when the register ID and receipt ID appear together in the package index and match the storage receipt record.
