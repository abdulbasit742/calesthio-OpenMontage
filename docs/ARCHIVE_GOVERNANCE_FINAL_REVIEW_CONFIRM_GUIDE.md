# Archive Governance Final Review Confirm Guide

This guide expands the final review confirmation plan into a practical operating checklist for reviewers.

## Purpose

Use this guide when the final delivery receipt has been generated and the reviewer needs to confirm archive governance delivery.

The final review confirmation step helps teams:

- verify that the final delivery receipt exists
- confirm that the receipt status is `delivered`
- run the final review confirmation builder
- store the generated confirmation with the archive package
- mark the archive governance delivery as reviewer-confirmed

## Required Input

```text
archive_governance_final_delivery_receipt.json
```

## Builder Command

```bash
python extras/archive_governance_final_delivery_acknowledgement.py --receipt archive_governance_final_delivery_receipt.json --reviewer-name "Archive Reviewer" --reviewer-role "Final Delivery Reviewer" --decision acknowledged --note "Reviewer confirms the final archive governance delivery." --out-json archive_governance_final_delivery_acknowledgement.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_ACKNOWLEDGEMENT.md
```

## Expected Outputs

- `archive_governance_final_delivery_acknowledgement.json`
- `ARCHIVE_GOVERNANCE_FINAL_DELIVERY_ACKNOWLEDGEMENT.md`

## Confirmation Checklist

1. Confirm the final packet exists.
2. Confirm the final handoff note exists.
3. Confirm the final delivery checklist exists.
4. Confirm the final delivery receipt exists.
5. Confirm the receipt status is `delivered`.
6. Run the final review confirmation builder.
7. Confirm the generated status is `acknowledged`.
8. Store the confirmation with the final archive package.

## Best Practice

Do not close the archive governance delivery until the final review confirmation output is stored with the package.
