# OpenMontage Plus Fork

This repository is prepared as a custom fork target for `calesthio/OpenMontage`.

## Current purpose

1. Import the upstream OpenMontage source from `https://github.com/calesthio/OpenMontage`.
2. Keep the original AGPL-3.0 license and upstream attribution.
3. Add a safe custom feature layer called **OpenMontage Plus**.

## Added Plus layer

This repo includes helper tools and docs that can be applied after importing upstream OpenMontage:

- Social video packager for TikTok, Reels, YouTube Shorts, and LinkedIn exports.
- Project starter CLI for structured video workspaces.
- Cost guard CLI for preflight budget checks.
- Migration/import guide for Kiro, Devin, or local terminal work.

## Migration command

Run this locally or inside your coding agent workspace:

```bash
bash scripts/import_openmontage_plus.sh
```

After import, review changes and push:

```bash
git status
git add -A
git commit -m "Import OpenMontage and add Plus features"
git push origin main
```

## Upstream

Original project: `calesthio/OpenMontage`

OpenMontage is licensed under GNU AGPLv3. Preserve the upstream license when importing source files.
