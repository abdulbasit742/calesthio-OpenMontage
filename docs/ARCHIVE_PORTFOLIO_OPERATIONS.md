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
7. create a repeatable runbook
8. use the CLI registry to inspect and call tools

## Recommended Full Workflow

Run the portfolio runbook generator first when you want a single Markdown command file.

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

## CLI Registry Usage

The archive CLI can list, inspect, and generate command arrays for the archive tools.

```bash
python extras/archive_toolchain_cli.py areas
python extras/archive_toolchain_cli.py list
python extras/archive_toolchain_cli.py list --area badge
python extras/archive_toolchain_cli.py list --area completion
python extras/archive_toolchain_cli.py list --area portfolio
python extras/archive_toolchain_cli.py show portfolio-runbook
python extras/archive_toolchain_cli.py command archive-completion-board --projects-root projects
```

## Suggested Review Order

1. Review `ARCHIVE_TOOLCHAIN_AUDIT.md`.
2. Review `PORTFOLIO_ARCHIVE_PLAN.md`.
3. Review `ARCHIVE_STATUS_BOARD.md`.
4. Review `ARCHIVE_BADGE_BOARD.md`.
5. Review `ARCHIVE_COMPLETION_BOARD.md`.
6. Review `ARCHIVE_PORTFOLIO_SUMMARY.md`.
7. Keep `ARCHIVE_PORTFOLIO_RUNBOOK.md` as the repeatable workflow reference.

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
- `archive_portfolio_runbook.json`
- `ARCHIVE_PORTFOLIO_RUNBOOK.md`

## Status Meaning

- `ready`: all expected portfolio boards are available and no board needs attention.
- `needs-attention`: at least one board is missing or reports incomplete work.
- `archive-ready`: a project or board is ready for archive review.
- `incomplete`: completion checks found missing source files or unfinished closeout/feedback/archive items.

## Best Practice

Run the individual project tools first, then run the board tools, then run the portfolio summary. This keeps board-level reports accurate and avoids stale status files.
