# OpenMontage Plus Review Pipeline Guide

This guide explains how to use the review pipeline runner added in Feature 049.

## Purpose

The review pipeline runner helps you refresh the most important pre-delivery reports in one sequence:

1. Content review
2. Quality score
3. Platform validation
4. Project review summary
5. Approval gate

It is useful before client delivery, publishing, or a final internal review.

## Dry Run First

Use dry run to verify the scripts and commands without changing project report files:

```bash
python extras/review_pipeline_runner.py --project projects/demo-video --dry-run --out-json projects/demo-video/review_pipeline_report.json --out-md projects/demo-video/REVIEW_PIPELINE_REPORT.md
```

## Full Review Run

After dry run passes, run the full review pipeline:

```bash
python extras/review_pipeline_runner.py --project projects/demo-video --out-json projects/demo-video/review_pipeline_report.json --out-md projects/demo-video/REVIEW_PIPELINE_REPORT.md
```

## Stop on First Failure

Use this when you want the pipeline to stop immediately after a failed step:

```bash
python extras/review_pipeline_runner.py --project projects/demo-video --stop-on-failure --out-json projects/demo-video/review_pipeline_report.json --out-md projects/demo-video/REVIEW_PIPELINE_REPORT.md
```

## Output Files

The runner writes:

- `review_pipeline_report.json`
- `REVIEW_PIPELINE_REPORT.md`

Each report includes:

- project path
- dry-run flag
- overall status
- step count
- failed count
- per-step command
- per-step return code
- per-step status

## Recommended Workflow

```bash
python extras/review_pipeline_runner.py --project projects/demo-video --dry-run
python extras/review_pipeline_runner.py --project projects/demo-video --stop-on-failure
python extras/project_review_summary.py --project projects/demo-video
python extras/approval_gate.py --project projects/demo-video
```

## Notes

- Use dry run whenever a project is newly created or files may be missing.
- Use stop-on-failure before final delivery so that errors are easier to locate.
- Refresh project review summary after content review, quality score, platform validation, and approval gate outputs are up to date.
- Feature registry sync may be retried separately when connector write checks allow it.
