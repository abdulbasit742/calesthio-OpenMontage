# OpenMontage Plus Features

This fork adds helper tools on top of upstream OpenMontage.

## Added tools

- `extras/social_packager.py`: creates platform-ready exports from a rendered MP4.
- `extras/project_starter.py`: creates a clean project workspace.
- `extras/cost_guard.py`: estimates a simple production budget before generation.
- `scripts/import_openmontage_plus.sh`: helps import upstream OpenMontage into this repository.

## Example commands

```bash
python extras/project_starter.py --name "AI Product Launch" --duration 45 --platform youtube-shorts
python extras/cost_guard.py --duration 45 --images 8 --tts-minutes 1 --budget 2.00
```

These files are standalone so the upstream package is not broken while the fork is being prepared.
