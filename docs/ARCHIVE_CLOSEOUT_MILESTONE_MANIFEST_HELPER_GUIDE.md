# Archive Closeout Milestone Manifest Helper Guide

This guide documents the `archive_closeout_milestone_manifest_helper.py` command helper for OpenMontage Plus archive governance.

Use it when you want to inspect manifest builder metadata or generate the milestone manifest command without manually typing the script path.

## Purpose

The archive closeout milestone manifest helper provides a small command registry for the milestone manifest builder.

It helps operators and reviewers:

- inspect manifest tool metadata
- confirm the target manifest builder exists
- generate a runnable milestone manifest command
- see the expected JSON and Markdown manifest outputs
- keep final artifact completeness commands consistent

## Available Commands

```bash
python extras/archive_closeout_milestone_manifest_helper.py show
python extras/archive_closeout_milestone_manifest_helper.py list
python extras/archive_closeout_milestone_manifest_helper.py command --label archive-closeout-feature-201-210-manifest --out-json archive_closeout_milestone_manifest.json --out-md ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md
```

## Target Script

```text
extras/archive_closeout_milestone_manifest.py
```

## Output Files

- `archive_closeout_milestone_manifest.json`
- `ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md`

## Suggested Workflow

1. Generate the archive closeout rollup.
2. Generate the archive closeout review gate.
3. Confirm the milestone summary exists.
4. Run `python extras/archive_closeout_milestone_manifest_helper.py show` to verify helper metadata.
5. Run the `command` helper to produce the full manifest builder command.
6. Execute the generated command.
7. Confirm the manifest status is `complete`.
8. Store `ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md` with the final archive package.

## Best Practice

Use this helper as the final command reference for artifact completeness review. It gives the reviewer the exact command needed to recreate the milestone manifest from the tracked feature 201-211 artifact set.
