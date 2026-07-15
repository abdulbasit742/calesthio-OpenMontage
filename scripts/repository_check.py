#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
findings: list[str] = []

lock_path = ROOT / "upstream/openmontage.lock.json"
try:
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
except Exception as error:
    findings.append(f"invalid upstream lock: {error}")
else:
    for key in ("commit", "license_blob_sha"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(lock.get(key, ""))):
            findings.append(f"{key} must be a full lowercase SHA")
    if lock.get("repository") != "https://github.com/calesthio/OpenMontage.git":
        findings.append("upstream repository URL is not the reviewed OpenMontage source")

shell = (ROOT / "scripts/import_openmontage_plus.sh").read_text(encoding="utf-8")
python_importer = (ROOT / "scripts/openmontage_import.py").read_text(encoding="utf-8")
for forbidden in ("rsync -a --delete", 'rm -rf "$TEMP_DIR"', "/tmp/openmontage-upstream"):
    if forbidden in shell or forbidden in python_importer:
        findings.append(f"destructive legacy importer pattern found: {forbidden}")
if "review-only" not in python_importer or "import-plan.json" not in python_importer:
    findings.append("importer must retain review-only provenance and conflict plan")
if "ALLOWED_STAGE_ROOT = \".openmontage-import\"" not in python_importer:
    findings.append("importer must restrict stage deletion to the ignored staging root")
if "--replace-stage" not in python_importer:
    findings.append("stage replacement must require an explicit operator flag")

if findings:
    print(f"Repository check failed with {len(findings)} finding(s):", file=sys.stderr)
    for finding in findings:
        print(f"- {finding}", file=sys.stderr)
    raise SystemExit(1)
print("Repository import safety check passed.")
