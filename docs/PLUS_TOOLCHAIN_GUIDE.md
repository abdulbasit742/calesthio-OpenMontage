# OpenMontage Plus Toolchain Guide

This guide explains how to run the OpenMontage Plus helper tools from one unified CLI.

## 1. Inspect the Toolchain

List every registered helper:

```bash
python extras/plus_cli.py list
```

List available tool areas:

```bash
python extras/plus_cli.py areas
```

Show tools from one area:

```bash
python extras/plus_cli.py list --area review
```

Show one tool definition:

```bash
python extras/plus_cli.py show approval
```

## 2. Recommended Project Flow

### Create or Bootstrap a Project

```bash
python extras/plus_cli.py run bootstrap -- --name "Demo Video" --platform youtube-shorts --duration 45 --topic "AI product launch" --audience "startup founders"
```

### Prepare Production Data

```bash
python extras/plus_cli.py run render-plan -- --project projects/demo-video
python extras/plus_cli.py run metadata -- --project projects/demo-video --topic "AI product launch" --audience "startup founders"
python extras/plus_cli.py run captions -- --text "First line" --duration 30 --out-prefix projects/demo-video/captions/final
```

### Check Quality and Platform Readiness

```bash
python extras/plus_cli.py run assets -- --project projects/demo-video
python extras/plus_cli.py run quality-score -- --project projects/demo-video
python extras/plus_cli.py run platform-check -- --project projects/demo-video
```

### Package and Review Delivery

```bash
python extras/plus_cli.py run handoff -- --project projects/demo-video
python extras/plus_cli.py run delivery -- --project projects/demo-video
python extras/plus_cli.py run delivery-audit -- --zip projects/demo-video/delivery.zip
python extras/plus_cli.py run client-review -- --project projects/demo-video
```

### Track Revisions and Approval

```bash
python extras/plus_cli.py run revisions -- summary --tracker revision_tracker.json
python extras/plus_cli.py run revision-report -- --tracker revision_tracker.json
python extras/plus_cli.py run approval -- --project projects/demo-video
```

### Publish and Report Roadmap

```bash
python extras/plus_cli.py run publishing -- --project projects/demo-video
python extras/plus_cli.py run feature-registry -- summary
python extras/plus_cli.py run roadmap-report -- --start 1 --end 50
```

## 3. Areas

Common areas include:

- projects
- exports
- render-pipeline
- quality
- creative
- publishing
- delivery
- review
- approval
- roadmap

## 4. Notes

- The CLI validates whether each script exists before running it.
- Use `show` before `run` when you need the exact example command.
- Feature 039 is documented as an issue because direct file creation was blocked during that pass.
