#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DEFAULT_PLAN = {
    'images': 0,
    'generated_video_seconds': 0,
    'tts_minutes': 0,
    'music_tracks': 0,
    'render_mode': 'local',
    'needs_budget_gate': True,
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def infer_scene_count(duration_seconds):
    duration = max(1, int(float(duration_seconds or 1)))
    return max(1, round(duration / 6))


def build_plan(project):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    preset = load_json(project_dir / 'export_preset.json', {})
    local_config = load_json(project_dir / 'local_zero_cost.json', {})

    duration = int(float(manifest.get('duration_seconds', 30) or 30))
    scene_count = infer_scene_count(duration)
    local_only = local_config.get('allow_paid_api_calls') is False

    plan = dict(DEFAULT_PLAN)
    plan.update({
        'project': manifest.get('name', project_dir.name),
        'project_folder': str(project_dir),
        'platform': manifest.get('platform', preset.get('platform', 'unknown')),
        'duration_seconds': duration,
        'scene_count': scene_count,
        'width': preset.get('width', 1080),
        'height': preset.get('height', 1920),
        'fps': preset.get('fps', 30),
        'aspect_ratio': preset.get('aspect_ratio', '9:16'),
        'caption_safe_zone': preset.get('caption_safe_zone', 'center 80 percent'),
        'render_mode': 'local' if local_only else 'mixed',
        'images': 0 if local_only else scene_count,
        'generated_video_seconds': 0 if local_only else duration,
        'tts_minutes': 0 if local_only else round(duration / 60, 2),
        'music_tracks': 0 if local_only else 1,
        'needs_budget_gate': not local_only,
    })
    return plan


def main():
    parser = argparse.ArgumentParser(description='Build an OpenMontage Plus render plan JSON')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out', default='render_plan.json')
    args = parser.parse_args()

    plan = build_plan(args.project)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, indent=2), encoding='utf-8')
    print(json.dumps(plan, indent=2))


if __name__ == '__main__':
    main()
