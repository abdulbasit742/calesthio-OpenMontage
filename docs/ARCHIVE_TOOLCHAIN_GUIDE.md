# Archive Toolchain Guide

This guide explains the final delivery, feedback, closeout, and archive workflow for the OpenMontage Plus toolchain.

## Purpose

The archive toolchain helps you move a finished project from delivery into final closeout and long-term archive readiness.

It is designed for projects under the `projects/` folder and produces JSON plus Markdown reports that are easy to inspect, share, or attach to a client handoff.

## Recommended Workflow

Run the workflow in this order:

1. Build delivery manifest.
2. Build handoff checklist.
3. Generate client delivery email draft.
4. Track and resolve client feedback.
5. Build feedback report.
6. Build project closeout report.
7. Build archive manifest.
8. Refresh global archive status board.

## 1. Delivery Manifest

```bash
python extras/delivery_manifest_builder.py --project projects/demo-video --out-json projects/demo-video/delivery_manifest.json --out-md projects/demo-video/DELIVERY_MANIFEST.md
```

Use this to confirm the expected delivery files exist.

## 2. Handoff Checklist

```bash
python extras/delivery_handoff_checklist.py --project projects/demo-video --out-json projects/demo-video/delivery_handoff_checklist.json --out-md projects/demo-video/DELIVERY_HANDOFF_CHECKLIST.md
```

Use this before sending a delivery package to the client.

## 3. Client Delivery Email

```bash
python extras/client_delivery_email_builder.py --project projects/demo-video --client-name "Client Name" --sender-name "Your Name" --out-json projects/demo-video/client_delivery_email.json --out-md projects/demo-video/CLIENT_DELIVERY_EMAIL.md
```

Use this to prepare a client-ready delivery email draft.

## 4. Client Feedback Tracker

Add feedback:

```bash
python extras/client_feedback_tracker.py add --tracker projects/demo-video/client_feedback_tracker.json --note "Client wants CTA stronger" --priority high --owner editor
```

Mark feedback resolved:

```bash
python extras/client_feedback_tracker.py status --tracker projects/demo-video/client_feedback_tracker.json --id 1 --status-value resolved --resolution-note "CTA updated"
```

Show summary:

```bash
python extras/client_feedback_tracker.py summary --tracker projects/demo-video/client_feedback_tracker.json
```

## 5. Client Feedback Report

```bash
python extras/client_feedback_report.py --tracker projects/demo-video/client_feedback_tracker.json --out-json projects/demo-video/client_feedback_report.json --out-md projects/demo-video/CLIENT_FEEDBACK_REPORT.md
```

Use this before closeout to confirm feedback is resolved or clearly documented.

## 6. Project Closeout Report

```bash
python extras/project_closeout_builder.py --project projects/demo-video --out-json projects/demo-video/project_closeout.json --out-md projects/demo-video/PROJECT_CLOSEOUT.md
```

Closeout status can be:

- `needs-files`
- `needs-handoff-review`
- `needs-readiness-review`
- `feedback-open`
- `closed`

## 7. Closeout Ops Runner

Dry run:

```bash
python extras/closeout_ops_runner.py --project projects/demo-video --client-name "Client Name" --sender-name "Your Name" --dry-run
```

Real run:

```bash
python extras/closeout_ops_runner.py --project projects/demo-video --client-name "Client Name" --sender-name "Your Name" --stop-on-failure
```

Use this when you want to refresh the final closeout files in one command.

## 8. Archive Manifest

```bash
python extras/project_archive_manifest.py --project projects/demo-video --out-json projects/demo-video/project_archive_manifest.json --out-md projects/demo-video/PROJECT_ARCHIVE_MANIFEST.md
```

Archive status can be:

- `archive-ready`
- `needs-attention`

## 9. Archive Ops Runner

Dry run:

```bash
python extras/archive_ops_runner.py --project projects/demo-video --client-name "Client Name" --sender-name "Your Name" --dry-run
```

Real run:

```bash
python extras/archive_ops_runner.py --project projects/demo-video --client-name "Client Name" --sender-name "Your Name" --stop-on-failure
```

Use this to run closeout ops and archive manifest generation for one project.

## 10. Archive Status Board

```bash
python extras/archive_status_board.py --projects-root projects --out-json archive_status_board.json --out-md ARCHIVE_STATUS_BOARD.md
```

Use this to see archive readiness across all project folders.

## 11. Portfolio Archive Plan

```bash
python extras/portfolio_archive_plan.py --projects-root projects --client-name "Client Name" --sender-name "Your Name" --out-json portfolio_archive_plan.json --out-md PORTFOLIO_ARCHIVE_PLAN.md
```

Use this to generate safe per-project archive commands without executing them automatically.

## 12. Archive Toolchain CLI

List all archive toolchain commands:

```bash
python extras/archive_toolchain_cli.py list
```

Show areas:

```bash
python extras/archive_toolchain_cli.py areas
```

Show a single tool:

```bash
python extras/archive_toolchain_cli.py show archive-ops
```

Generate a shell command:

```bash
python extras/archive_toolchain_cli.py command archive-board --projects-root projects
```

## Final Review Checklist

Before marking a project archived, confirm:

- Delivery package exists.
- Delivery manifest is available.
- Handoff checklist is ready.
- Client feedback is resolved or closed.
- Project closeout status is `closed`.
- Project archive manifest status is `archive-ready`.
- Global archive status board is refreshed.

## Recommended Files to Keep

Keep these files with the project archive:

- `delivery.zip`
- `delivery_manifest.json`
- `DELIVERY_MANIFEST.md`
- `delivery_handoff_checklist.json`
- `DELIVERY_HANDOFF_CHECKLIST.md`
- `client_delivery_email.json`
- `CLIENT_DELIVERY_EMAIL.md`
- `client_feedback_tracker.json`
- `client_feedback_report.json`
- `CLIENT_FEEDBACK_REPORT.md`
- `project_closeout.json`
- `PROJECT_CLOSEOUT.md`
- `project_archive_manifest.json`
- `PROJECT_ARCHIVE_MANIFEST.md`

## Notes

The archive toolchain is intentionally report-first. It produces clear files that can be reviewed before any project is considered finished, closed, or archived.
