#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PRESETS = {
    'youtube-shorts': {
        'platform': 'youtube-shorts',
        'aspect_ratio': '9:16',
        'width': 1080,
        'height': 1920,
        'fps': 30,
        'max_duration_seconds': 60,
        'caption_safe_zone': 'center 80 percent',
    },
    'instagram-reels': {
        'platform': 'instagram-reels',
        'aspect_ratio': '9:16',
        'width': 1080,
        'height': 1920,
        'fps': 30,
        'max_duration_seconds': 90,
        'caption_safe_zone': 'center 75 percent',
    },
    'tiktok': {
        'platform': 'tiktok',
        'aspect_ratio': '9:16',
        'width': 1080,
        'height': 1920,
        'fps': 30,
        'max_duration_seconds': 180,
        'caption_safe_zone': 'center 75 percent',
    },
    'youtube': {
        'platform': 'youtube',
        'aspect_ratio': '16:9',
        'width': 1920,
        'height': 1080,
        'fps': 30,
        'max_duration_seconds': 600,
        'caption_safe_zone': 'lower third',
    },
    'linkedin': {
        'platform': 'linkedin',
        'aspect_ratio': '16:9',
        'width': 1920,
        'height': 1080,
        'fps': 30,
        'max_duration_seconds': 300,
        'caption_safe_zone': 'lower third',
    },
    'square-feed': {
        'platform': 'square-feed',
        'aspect_ratio': '1:1',
        'width': 1080,
        'height': 1080,
        'fps': 30,
        'max_duration_seconds': 90,
        'caption_safe_zone': 'center 80 percent',
    },
}


def write_project_preset(project_folder, preset_name):
    if preset_name not in PRESETS:
        raise SystemExit(f'Unknown preset: {preset_name}')
    project_dir = Path(project_folder)
    project_dir.mkdir(parents=True, exist_ok=True)
    out_file = project_dir / 'export_preset.json'
    out_file.write_text(json.dumps(PRESETS[preset_name], indent=2))
    return out_file


def main():
    parser = argparse.ArgumentParser(description='OpenMontage Plus export presets')
    parser.add_argument('command', choices=['list', 'show', 'write'])
    parser.add_argument('--preset', default='youtube-shorts')
    parser.add_argument('--project', default='projects/demo-video')
    args = parser.parse_args()

    if args.command == 'list':
        print(json.dumps(sorted(PRESETS.keys()), indent=2))
    elif args.command == 'show':
        if args.preset not in PRESETS:
            raise SystemExit(f'Unknown preset: {args.preset}')
        print(json.dumps(PRESETS[args.preset], indent=2))
    elif args.command == 'write':
        out_file = write_project_preset(args.project, args.preset)
        print(f'Wrote {out_file}')


if __name__ == '__main__':
    main()
