# Archive Closeout Register Guide

This guide explains how to keep a simple register reference after the storage receipt step.

## Purpose

A register reference helps reviewers find the archived package later. It connects the storage receipt to one stable register ID.

## Required Records

Confirm these records are available before assigning the register ID:

- `archive_closeout_storage_receipt.json`
- `ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md`
- `docs/ARCHIVE_CLOSEOUT_STORAGE_REGISTER_NOTE.md`

## Register Fields

Use these fields for the register reference:

- register ID
- storage receipt ID
- package label
- owner
- reviewer
- storage owner
- storage location
- status
- lookup note

## Status Values

- `registered`: receipt is available and the package has a register ID.
- `blocked`: receipt is missing or not ready.

## Workflow

1. Generate the storage receipt.
2. Confirm receipt status is `received`.
3. Assign one register ID.
4. Add the register ID to the package index.
5. Store the register note with the package.
6. Confirm the package can be found by register ID.

## Checklist

- Receipt status is `received`.
- Receipt ID is present.
- Register ID is assigned.
- Storage location is clear.
- Package index includes the register ID.
- Register note is stored with the package.

## Best Practice

Use a stable register ID such as `ARCHIVE-STORAGE-REGISTER-001` and keep it beside the storage receipt record.
