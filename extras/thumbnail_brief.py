#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SAFE_ZONES = {
    '9:16': {
        'primary_text': 'center upper third',
        'face_or_subject': 'center middle',
        'avoid': ['bottom app controls', 'top platform icons'],
    },
    '16:9': {
        'primary_text': 'left or right third',
        'face_or_subject': 'opposite third',
        'avoid': ['extreme edges', 'small text'],
    },
    '1:1': {
        'primary_text': 'top center',
        'face_or_subject': 'center middle',
        'avoid': ['tiny text', 'busy background'],
    },
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def build_brief(project, headline, mood, colors, subject, style):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    preset = load_json(project_dir / 'export_preset.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})

    width = int(preset.get('width', 1080))
    height = int(preset.get('height', 1920))
    aspect_ratio = preset.get('aspect_ratio', '9:16')
    safe_zone = SAFE_ZONES.get(aspect_ratio, SAFE_ZONES['9:16'])
    project_name = manifest.get('name', project_dir.name)
    final_headline = headline or metadata.get('title') or project_name

    return {
        'project': project_name,
        'platform': manifest.get('platform', preset.get('platform', 'youtube-shorts')),
        'canvas': {
            'width': width,
            'height': height,
            'aspect_ratio': aspect_ratio,
        },
        'headline': final_headline,
        'subject': subject,
        'mood': mood,
        'style': style,
        'colors': [item.strip() for item in colors.split(',') if item.strip()],
        'layout': {
            'primary_text': safe_zone['primary_text'],
            'face_or_subject': safe_zone['face_or_subject'],
            'avoid': safe_zone['avoid'],
        },
        'checklist': [
            'Readable at small size',
            'High contrast between text and background',
            'One main subject only',
            'No misleading claims',
            'Matches video topic and metadata',
        ],
    }


def main():
    parser = argparse.ArgumentParser(description='Build a thumbnail design brief JSON')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--headline', default='')
    parser.add_argument('--subject', default='main product or person')
    parser.add_argument('--mood', default='bold, clean, energetic')
    parser.add_argument('--style', default='modern social media thumbnail')
    parser.add_argument('--colors', default='black, white, yellow')
    parser.add_argument('--out', default='projects/demo-video/thumbnail_brief.json')
    args = parser.parse_args()

    brief = build_brief(args.project, args.headline, args.mood, args.colors, args.subject, args.style)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(brief, indent=2), encoding='utf-8')
    print(json.dumps(brief, indent=2))


if __name__ == '__main__':
    main()
