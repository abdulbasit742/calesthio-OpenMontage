# Archive Portfolio Operations Guide

This guide documents the newer OpenMontage Plus archive portfolio tools added after the base archive workflow. Use it after delivery, feedback, closeout, and archive manifest files already exist for each project.

## Goal

The goal is to move from single-project archive files to portfolio-level visibility:

1. audit the toolchain
2. generate per-project badge plans
3. build global badge boards
4. generate per-project completion reports
5. build global completion boards
6. summarize the archive portfolio
7. build a final portfolio packlist
8. build a searchable portfolio index
9. build a one-page portfolio dashboard
10. build an executive portfolio digest
11. build a timestamped portfolio snapshot
12. build a final readiness review checklist
13. build a final release packet manifest
14. build a final handoff note
15. build a handoff receipt and acknowledgement record
16. build a final retention policy and cleanup governance record
17. create a repeatable runbook
18. use the CLI registry to inspect and call tools

## Recommended Full Workflow

Run the portfolio runbook generator first when you want a single Markdown command file. The runbook includes audit, plans, boards, summary, packlist, searchable index, dashboard, executive digest, snapshot, readiness review, release packet, handoff note, handoff receipt, and retention policy steps.

```bash
python extras/archive_portfolio_runbook.py --projects-root projects --client-name "Client Name" --sender-name "Your Name" --out-json archive_portfolio_runbook.json --out-md ARCHIVE_PORTFOLIO_RUNBOOK.md
```

Then follow the generated `ARCHIVE_PORTFOLIO_RUNBOOK.md` step by step.

## Toolchain Audit

Use this to confirm the archive scripts and guide files are present.

```bash
python extras/archive_toolchain_audit.py --out-json archive_toolchain_audit.json --out-md ARCHIVE_TOOLCHAIN_AUDIT.md
```

Main output:

- `archive_toolchain_audit.json`
- `ARCHIVE_TOOLCHAIN_AUDIT.md`

## Archive Readiness Badge Flow

Use this flow after project archive manifests exist.

### Per-project badge

```bash
python extras/archive_readiness_badge.py --project projects/demo-video --out-json projects/demo-video/archive_readiness_badge.json --out-md projects/demo-video/ARCHIVE_READINESS_BADGE.md
```

### Badge command plan for all projects

```bash
python extras/archive_badge_plan.py --projects-root projects --out-json archive_badge_plan.json --out-md ARCHIVE_BADGE_PLAN.md
```

### Global badge board

```bash
python extras/archive_badge_board.py --projects-root projects --out-json archive_badge_board.json --out-md ARCHIVE_BADGE_BOARD.md
```

## Archive Completion Flow

Use this flow after closeout, feedback report, archive manifest, and badge files exist.

### Per-project completion report

```bash
python extras/archive_completion_report.py --project projects/demo-video --out-json projects/demo-video/archive_completion_report.json --out-md projects/demo-video/ARCHIVE_COMPLETION_REPORT.md
```

### Completion command plan for all projects

```bash
python extras/archive_completion_plan.py --projects-root projects --out-json archive_completion_plan.json --out-md ARCHIVE_COMPLETION_PLAN.md
```

### Global completion board

```bash
python extras/archive_completion_board.py --projects-root projects --out-json archive_completion_board.json --out-md ARCHIVE_COMPLETION_BOARD.md
```

## Portfolio Summary

Use this after status board, badge board, completion board, and toolchain audit files exist.

```bash
python extras/archive_portfolio_summary.py --out-json archive_portfolio_summary.json --out-md ARCHIVE_PORTFOLIO_SUMMARY.md
```

Main output:

- `archive_portfolio_summary.json`
- `ARCHIVE_PORTFOLIO_SUMMARY.md`

## Portfolio Packlist

Use this as the final packaging checklist after summary and board files are generated. It checks portfolio-level files and each project folder for expected delivery, feedback, closeout, archive, badge, and completion outputs.

```bash
python extras/archive_portfolio_packlist.py --projects-root projects --out-json archive_portfolio_packlist.json --out-md ARCHIVE_PORTFOLIO_PACKLIST.md
```

Main output:

- `archive_portfolio_packlist.json`
- `ARCHIVE_PORTFOLIO_PACKLIST.md`

## Portfolio Index

Use this after the packlist is generated. It creates a searchable document index for runbook, summary, packlist, boards, plans, audit files, and per-project archive documents.

```bash
python extras/archive_portfolio_index.py --projects-root projects --out-json archive_portfolio_index.json --out-md ARCHIVE_PORTFOLIO_INDEX.md
```

Main output:

- `archive_portfolio_index.json`
- `ARCHIVE_PORTFOLIO_INDEX.md`

## Portfolio Dashboard

Use this as the final review screen after summary, packlist, index, boards, and audit files are generated. It combines those source files into one dashboard with status cards, missing source counts, attention counts, and next steps.

```bash
python extras/archive_portfolio_dashboard.py --projects-root projects --out-json archive_portfolio_dashboard.json --out-md ARCHIVE_PORTFOLIO_DASHBOARD.md
```

Main output:

- `archive_portfolio_dashboard.json`
- `ARCHIVE_PORTFOLIO_DASHBOARD.md`

## Portfolio Executive Digest

Use this after the dashboard is generated. It creates a short executive review file from the dashboard, summary, packlist, and index sources with headline status, executive metrics, source snapshot, and final next steps.

```bash
python extras/archive_portfolio_digest.py --projects-root projects --out-json archive_portfolio_digest.json --out-md ARCHIVE_PORTFOLIO_DIGEST.md
```

Main output:

- `archive_portfolio_digest.json`
- `ARCHIVE_PORTFOLIO_DIGEST.md`

## Portfolio Snapshot

Use this as the freeze/record step after the digest is generated. It records expected Markdown and JSON portfolio outputs with existence, size, modified time, missing-file counts, and a timestamped snapshot label.

```bash
python extras/archive_portfolio_snapshot.py --projects-root projects --label archive-portfolio-final --out-json archive_portfolio_snapshot.json --out-md ARCHIVE_PORTFOLIO_SNAPSHOT.md
```

Main output:

- `archive_portfolio_snapshot.json`
- `ARCHIVE_PORTFOLIO_SNAPSHOT.md`

## Portfolio Readiness Review

Use this after the snapshot is generated. It checks the snapshot, digest, and dashboard source files, then creates one final readiness checklist with source statuses, passed checks, missing source counts, failed check counts, and source notes.

```bash
python extras/archive_portfolio_readiness_review.py --projects-root projects --reviewer-name "Reviewer Name" --review-note "Final package review" --out-json archive_portfolio_readiness_review.json --out-md ARCHIVE_PORTFOLIO_READINESS_REVIEW.md
```

Main output:

- `archive_portfolio_readiness_review.json`
- `ARCHIVE_PORTFOLIO_READINESS_REVIEW.md`

## Portfolio Release Packet

Use this after the readiness review is generated. It builds the final release packet manifest by checking all expected portfolio Markdown files and key source JSON files, then reports whether the archive portfolio is ready to package or still needs attention.

```bash
python extras/archive_portfolio_release_packet.py --projects-root projects --packet-label archive-portfolio-release --out-json archive_portfolio_release_packet.json --out-md ARCHIVE_PORTFOLIO_RELEASE_PACKET.md
```

Main output:

- `archive_portfolio_release_packet.json`
- `ARCHIVE_PORTFOLIO_RELEASE_PACKET.md`

## Portfolio Handoff Note

Use this after the release packet is generated. It builds a client/team-ready handoff note from the release packet, readiness review, and digest sources, then lists recommended handoff attachments and next actions.

```bash
python extras/archive_portfolio_handoff_note.py --projects-root projects --recipient-name "Client Team" --sender-name "Your Name" --handoff-label archive-portfolio-handoff --out-json archive_portfolio_handoff_note.json --out-md ARCHIVE_PORTFOLIO_HANDOFF_NOTE.md
```

Main output:

- `archive_portfolio_handoff_note.json`
- `ARCHIVE_PORTFOLIO_HANDOFF_NOTE.md`

## Portfolio Handoff Receipt

Use this after the handoff note is generated. It builds a receipt and acknowledgement record from the handoff note, release packet, and readiness review sources, then lists receipt attachments, counts, and confirmation fields.

```bash
python extras/archive_portfolio_handoff_receipt.py --projects-root projects --recipient-name "Client Team" --sender-name "Your Name" --receipt-label archive-portfolio-receipt --out-json archive_portfolio_handoff_receipt.json --out-md ARCHIVE_PORTFOLIO_HANDOFF_RECEIPT.md
```

Main output:

- `archive_portfolio_handoff_receipt.json`
- `ARCHIVE_PORTFOLIO_HANDOFF_RECEIPT.md`

## Portfolio Retention Policy

Use this after the handoff receipt is generated. It builds a retention and cleanup governance record from the handoff receipt, handoff note, release packet, and snapshot sources, then groups key files by owner role, retention period, and review cadence.

```bash
python extras/archive_portfolio_retention_policy.py --projects-root projects --policy-label archive-portfolio-retention-policy --owner-name "Archive Owner" --out-json archive_portfolio_retention_policy.json --out-md ARCHIVE_PORTFOLIO_RETENTION_POLICY.md
```

Main output:

- `archive_portfolio_retention_policy.json`
- `ARCHIVE_PORTFOLIO_RETENTION_POLICY.md`

## CLI Registry Usage

The archive CLI can list, inspect, and generate command arrays for the archive tools.

```bash
python extras/archive_toolchain_cli.py areas
python extras/archive_toolchain_cli.py list
python extras/archive_toolchain_cli.py list --area badge
python extras/archive_toolchain_cli.py list --area completion
python extras/archive_toolchain_cli.py list --area portfolio
python extras/archive_toolchain_cli.py show portfolio-runbook
python extras/archive_toolchain_cli.py show portfolio-packlist
python extras/archive_toolchain_cli.py show portfolio-index
python extras/archive_toolchain_cli.py show portfolio-dashboard
python extras/archive_toolchain_cli.py show portfolio-digest
python extras/archive_toolchain_cli.py show portfolio-snapshot
python extras/archive_toolchain_cli.py show portfolio-readiness-review
python extras/archive_toolchain_cli.py show portfolio-release-packet
python extras/archive_toolchain_cli.py show portfolio-handoff-note
python extras/archive_toolchain_cli.py show portfolio-handoff-receipt
python extras/archive_toolchain_cli.py show portfolio-retention-policy
python extras/archive_toolchain_cli.py command archive-completion-board --projects-root projects
python extras/archive_toolchain_cli.py command portfolio-packlist --projects-root projects
python extras/archive_toolchain_cli.py command portfolio-index --projects-root projects
python extras/archive_toolchain_cli.py command portfolio-dashboard --projects-root projects
python extras/archive_toolchain_cli.py command portfolio-digest --projects-root projects
python extras/archive_toolchain_cli.py command portfolio-snapshot --projects-root projects --label archive-portfolio-final
python extras/archive_toolchain_cli.py command portfolio-readiness-review --projects-root projects
python extras/archive_toolchain_cli.py command portfolio-release-packet --projects-root projects --packet-label archive-portfolio-release
python extras/archive_toolchain_cli.py command portfolio-handoff-note --projects-root projects --recipient-name Client --sender-name Team --handoff-label archive-portfolio-handoff
python extras/archive_toolchain_cli.py command portfolio-handoff-receipt --projects-root projects --recipient-name Client --sender-name Team --receipt-label archive-portfolio-receipt
python extras/archive_toolchain_cli.py command portfolio-retention-policy --projects-root projects --policy-label archive-portfolio-retention-policy --owner-name ArchiveOwner
```

## Suggested Review Order

1. Review `ARCHIVE_TOOLCHAIN_AUDIT.md`.
2. Review `PORTFOLIO_ARCHIVE_PLAN.md`.
3. Review `ARCHIVE_STATUS_BOARD.md`.
4. Review `ARCHIVE_BADGE_BOARD.md`.
5. Review `ARCHIVE_COMPLETION_BOARD.md`.
6. Review `ARCHIVE_PORTFOLIO_SUMMARY.md`.
7. Review `ARCHIVE_PORTFOLIO_PACKLIST.md`.
8. Review `ARCHIVE_PORTFOLIO_INDEX.md`.
9. Review `ARCHIVE_PORTFOLIO_DASHBOARD.md`.
10. Review `ARCHIVE_PORTFOLIO_DIGEST.md`.
11. Review `ARCHIVE_PORTFOLIO_SNAPSHOT.md`.
12. Review `ARCHIVE_PORTFOLIO_READINESS_REVIEW.md`.
13. Review `ARCHIVE_PORTFOLIO_RELEASE_PACKET.md`.
14. Review `ARCHIVE_PORTFOLIO_HANDOFF_NOTE.md`.
15. Review `ARCHIVE_PORTFOLIO_HANDOFF_RECEIPT.md`.
16. Review `ARCHIVE_PORTFOLIO_RETENTION_POLICY.md`.
17. Keep `ARCHIVE_PORTFOLIO_RUNBOOK.md` as the repeatable workflow reference.

## Expected Portfolio Files

The final archive portfolio workspace can contain these generated files:

- `archive_toolchain_audit.json`
- `ARCHIVE_TOOLCHAIN_AUDIT.md`
- `portfolio_archive_plan.json`
- `PORTFOLIO_ARCHIVE_PLAN.md`
- `archive_status_board.json`
- `ARCHIVE_STATUS_BOARD.md`
- `archive_badge_plan.json`
- `ARCHIVE_BADGE_PLAN.md`
- `archive_badge_board.json`
- `ARCHIVE_BADGE_BOARD.md`
- `archive_completion_plan.json`
- `ARCHIVE_COMPLETION_PLAN.md`
- `archive_completion_board.json`
- `ARCHIVE_COMPLETION_BOARD.md`
- `archive_portfolio_summary.json`
- `ARCHIVE_PORTFOLIO_SUMMARY.md`
- `archive_portfolio_packlist.json`
- `ARCHIVE_PORTFOLIO_PACKLIST.md`
- `archive_portfolio_index.json`
- `ARCHIVE_PORTFOLIO_INDEX.md`
- `archive_portfolio_dashboard.json`
- `ARCHIVE_PORTFOLIO_DASHBOARD.md`
- `archive_portfolio_digest.json`
- `ARCHIVE_PORTFOLIO_DIGEST.md`
- `archive_portfolio_snapshot.json`
- `ARCHIVE_PORTFOLIO_SNAPSHOT.md`
- `archive_portfolio_readiness_review.json`
- `ARCHIVE_PORTFOLIO_READINESS_REVIEW.md`
- `archive_portfolio_release_packet.json`
- `ARCHIVE_PORTFOLIO_RELEASE_PACKET.md`
- `archive_portfolio_handoff_note.json`
- `ARCHIVE_PORTFOLIO_HANDOFF_NOTE.md`
- `archive_portfolio_handoff_receipt.json`
- `ARCHIVE_PORTFOLIO_HANDOFF_RECEIPT.md`
- `archive_portfolio_retention_policy.json`
- `ARCHIVE_PORTFOLIO_RETENTION_POLICY.md`
- `archive_portfolio_runbook.json`
- `ARCHIVE_PORTFOLIO_RUNBOOK.md`

## Status Meaning

- `ready`: all expected portfolio boards are available and no board needs attention.
- `needs-attention`: at least one board, packlist item, indexed file, dashboard source, digest source, snapshot file, release packet file, handoff attachment, receipt attachment, or retention file is missing or reports incomplete work.
- `ready-for-final-review`: the readiness review found no missing source files and all checks passed.
- `ready-to-package`: the release packet found all expected packet files and key source statuses are ready.
- `ready-to-send`: the handoff note found source summaries and handoff attachments available.
- `ready-for-acknowledgement`: the handoff receipt found source summaries and receipt attachments available.
- `ready-for-retention-review`: the retention policy inputs are available and ready for owner review.
- `needs-review`: the readiness review found missing source files or failed checks.
- `archive-ready`: a project or board is ready for archive review.
- `complete`: the packlist, index, or snapshot found every expected portfolio and project file.
- `incomplete`: completion checks found missing source files or unfinished closeout/feedback/archive items.

## Best Practice

Run the individual project tools first, then run the board tools, then run the portfolio summary, then the portfolio packlist, then the portfolio index, then the portfolio dashboard, then the portfolio digest, then the portfolio snapshot, then the readiness review, then the release packet, then the handoff note, then the handoff receipt, and finally the retention policy. This keeps board-level reports accurate, gives leaders one short executive review file, records the final archive package state, checks final readiness, creates one package manifest, prepares the handoff message, records acknowledgement, and ends with retention governance.
