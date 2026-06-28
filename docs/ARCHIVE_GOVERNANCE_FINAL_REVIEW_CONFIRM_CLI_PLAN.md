# Archive Governance Final Review Confirm CLI Plan

This plan documents a small helper for the final review confirmation step.

## Target Builder

```text
extras/archive_governance_final_delivery_acknowledgement.py
```

## Goal

The helper should provide simple discovery and command generation for the final review confirmation builder.

## Planned Helper Commands

```bash
python extras/archive_governance_final_review_confirm_cli.py show
python extras/archive_governance_final_review_confirm_cli.py list
python extras/archive_governance_final_review_confirm_cli.py command --receipt archive_governance_final_delivery_receipt.json --reviewer-name "Archive Reviewer" --reviewer-role "Final Delivery Reviewer" --decision acknowledged --out-json archive_governance_final_delivery_acknowledgement.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_ACKNOWLEDGEMENT.md
```

## Expected Outputs

- `archive_governance_final_delivery_acknowledgement.json`
- `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_ACKNOWLEDGEMENT.md`

## Review Flow

1. Generate the final delivery receipt.
2. Confirm the receipt status is `delivered`.
3. Run the final review confirmation builder.
4. Store the generated confirmation with the archive package.
