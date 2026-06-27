# Archive Governance Readiness Runbook Appendix Guide

This guide documents the `archive_governance_readiness_runbook_appendix.py` helper for OpenMontage Plus archive governance.

Use it when the main archive portfolio runbook already exists and you need to append the final governance readiness checkpoint without editing the main runbook file.

## Purpose

The runbook appendix builder creates a small add-on document that tells reviewers exactly where and how to run the final governance readiness summary step.

It is useful when:

- the main runbook has already been generated
- the final readiness summary step needs to be shared separately
- direct main runbook editing is not desired
- reviewers need a clear final command after the approval record

## Command

```bash
python extras/archive_governance_readiness_runbook_appendix.py --label archive-governance-final-checkpoint --out-json archive_governance_readiness_runbook_appendix.json --out-md ARCHIVE_GOVERNANCE_READINESS_RUNBOOK_APPENDIX.md
```

## Output Files

- `archive_governance_readiness_runbook_appendix.json`
- `ARCHIVE_GOVERNANCE_READINESS_RUNBOOK_APPENDIX.md`

## What The Appendix Contains

The appendix includes:

- final checkpoint label
- generated UTC time
- readiness summary command
- recommended position in the workflow
- final JSON and Markdown outputs

## Recommended Position

Run this appendix step after:

```text
ARCHIVE_PORTFOLIO_GOVERNANCE_APPROVAL_RECORD.md
```

Then run the generated command for:

```text
ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md
```

## Suggested Review Order

1. Generate the archive portfolio runbook.
2. Generate the governance packet.
3. Generate the governance approval record.
4. Generate this runbook appendix.
5. Run the readiness summary command from the appendix.
6. Review `ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md`.

## Best Practice

Keep this appendix with the final archive package. It works like a small addendum that makes the final governance readiness checkpoint easy to find, run, and review.
