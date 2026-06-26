#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_REPO="https://github.com/calesthio/OpenMontage.git"
TEMP_DIR="/tmp/openmontage-upstream"

printf 'Importing upstream OpenMontage...\n'
rm -rf "$TEMP_DIR"
git clone --depth 1 "$UPSTREAM_REPO" "$TEMP_DIR"

# Preserve this fork's Plus layer before syncing upstream.
mkdir -p /tmp/openmontage-plus-backup
cp -R README.md docs extras scripts /tmp/openmontage-plus-backup/ 2>/dev/null || true

# Copy upstream into current repo working tree.
rsync -a --delete --exclude='.git' "$TEMP_DIR"/ ./

# Restore Plus layer files.
cp -R /tmp/openmontage-plus-backup/* ./ 2>/dev/null || true

printf '\nDone. Review with:\n  git status\n\nThen commit and push with:\n  git add -A\n  git commit -m "Import OpenMontage and add Plus features"\n  git push origin main\n'
