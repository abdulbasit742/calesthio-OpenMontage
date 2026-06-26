# Kiro Prompt: Import OpenMontage and Apply Plus Layer

Use this prompt in Kiro/Devin/Codex if you want the full upstream code moved into this repository.

```text
Project: abdulbasit742/calesthio-OpenMontage

Task:
1. Clone this repository.
2. Run: bash scripts/import_openmontage_plus.sh
3. Confirm upstream OpenMontage files are present: pipeline_defs, skills, tools, docs, remotion-composer, schemas, tests, requirements.txt, setup.py, AGENT_GUIDE.md, PROJECT_CONTEXT.md.
4. Keep README.md, docs/OPENMONTAGE_PLUS_FEATURES.md, scripts/import_openmontage_plus.sh, and extras/*.py from this fork.
5. Run quick checks:
   - python extras/project_starter.py --name "Demo Video" --duration 45 --platform youtube-shorts
   - python extras/cost_guard.py --duration 45 --images 8 --tts-minutes 1 --budget 2.00
   - python extras/export_packager.py projects/demo-video/renders/final.mp4 --out-dir projects/demo-video/exports
6. Do not add API keys or secrets.
7. Commit with message: Import OpenMontage and add Plus features.
8. Push to main.

Extra feature ideas for next pass:
- Web UI dashboard for project briefs and render history.
- One-click preset generator for Shorts/Reels/TikTok style videos.
- Local-only zero-cost mode with Piper TTS, FFmpeg, Remotion, and open footage.
- Budget approval gate before any paid provider call.
- Export checklist with captions, audio loudness, thumbnail, and metadata checks.
```
