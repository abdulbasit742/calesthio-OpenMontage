# Archive Closeout Milestone Manifest Guide

This guide documents the `archive_closeout_milestone_manifest.py` builder for OpenMontage Plus archive governance.

Use it after the feature 201-210 milestone summary has been added and the rollup/review-gate files are present.

## Purpose

The archive closeout milestone manifest verifies the artifact coverage for the final closeout milestone.

It checks the feature 201-211 artifact set and records:

- feature number
- artifact path
- artifact kind
- artifact purpose
- whether the file exists locally
- file size in bytes
- missing artifact list
- manifest status
- next steps

## Command

```bash
python extras/archive_closeout_milestone_manifest.py --label archive-closeout-feature-201-210-manifest --out-json archive_closeout_milestone_manifest.json --out-md ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md
```

## Output Files

- `archive_closeout_milestone_manifest.json`
- `ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md`

## Status Meaning

- `complete`: all tracked closeout milestone artifacts are present.
- `needs-attention`: one or more tracked artifacts are missing.

## Suggested Workflow

1. Generate the closeout rollup.
2. Generate the review gate.
3. Confirm the feature 201-210 milestone summary exists.
4. Run `archive_closeout_milestone_manifest.py`.
5. Confirm the manifest status is `complete`.
6. Store the manifest JSON and Markdown with the final archive package.

## Best Practice

Use this manifest as the final artifact completeness check for features 201-210. It does not replace the rollup or review gate. Instead, it verifies that the supporting builders, guides, helpers, audit notes, and milestone summary are present before final handoff.
