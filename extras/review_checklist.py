#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DEFAULT_CHECKS = [
    {'id': 'captions_present', 'title': 'Captions file is present', 'required': True},
    {'id': 'captions_readable', 'title': 'Captions are readable and synced', 'required': True},
    {'id': 'thumbnail_present', 'title': 'Thumbnail image is present', 'required': True},
    {'id': 'thumbnail_clear', 'title': 'Thumbnail is clear and not blurry', 'required': True},
    {'id': 'audio_loudness_ok', 'title': 'Audio loudness is acceptable', 'required': True},
    {'id': 'metadata_ready', 'title': 'Title, description, and hashtags are ready', 'required': True},
    {'id': 'export_preset_selected', 'title': 'Correct export preset is selected', 'required': True},
    {'id': 'final_video_reviewed', 'title': 'Final video was manually reviewed', 'required': True},
]


def create_template(path):
    data = {
        'project': 'demo-video',
        'checks': [dict(item, done=False, note='') for item in DEFAULT_CHECKS],
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, indent=2))
    return data


def load_checklist(path):
    file_path = Path(path)
    if not file_path.exists():
        raise SystemExit(f'Checklist not found: {file_path}')
    return json.loads(file_path.read_text())


def evaluate(data):
    checks = data.get('checks', [])
    required = [item for item in checks if item.get('required', True)]
    passed = [item for item in required if item.get('done') is True]
    missing = [item for item in required if item.get('done') is not True]
    score = 100 if not required else round((len(passed) / len(required)) * 100, 2)
    return {
        'project': data.get('project', 'unknown'),
        'approved': len(missing) == 0,
        'score_percent': score,
        'passed_required': len(passed),
        'total_required': len(required),
        'missing': [{'id': item.get('id'), 'title': item.get('title')} for item in missing],
    }


def main():
    parser = argparse.ArgumentParser(description='Review captions, thumbnail, audio, metadata, and exports')
    parser.add_argument('command', choices=['template', 'check'])
    parser.add_argument('--file', default='projects/demo-video/review_checklist.json')
    args = parser.parse_args()

    if args.command == 'template':
        print(json.dumps(create_template(args.file), indent=2))
    elif args.command == 'check':
        print(json.dumps(evaluate(load_checklist(args.file)), indent=2))


if __name__ == '__main__':
    main()
