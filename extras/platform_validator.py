#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PLATFORM_RULES = {
    'youtube-shorts': {
        'max_duration_seconds': 60,
        'preferred_aspect_ratio': '9:16',
        'max_title_length': 100,
        'max_hashtags': 8,
        'captions_recommended': True,
    },
    'instagram-reels': {
        'max_duration_seconds': 90,
        'preferred_aspect_ratio': '9:16',
        'max_title_length': 125,
        'max_hashtags': 12,
        'captions_recommended': True,
    },
    'tiktok': {
        'max_duration_seconds': 180,
        'preferred_aspect_ratio': '9:16',
        'max_title_length': 150,
        'max_hashtags': 10,
        'captions_recommended': True,
    },
    'youtube': {
        'max_duration_seconds': 43200,
        'preferred_aspect_ratio': '16:9',
        'max_title_length': 100,
        'max_hashtags': 8,
        'captions_recommended': True,
    },
    'linkedin': {
        'max_duration_seconds': 600,
        'preferred_aspect_ratio': '1:1',
        'max_title_length': 150,
        'max_hashtags': 5,
        'captions_recommended': True,
    },
    'square-feed': {
        'max_duration_seconds': 60,
        'preferred_aspect_ratio': '1:1',
        'max_title_length': 125,
        'max_hashtags': 10,
        'captions_recommended': True,
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


def normalize_hashtags(value):
    if isinstance(value, str):
        return [item for item in value.split() if item.strip().startswith('#')]
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []


def check(condition, passed_message, failed_message, severity='error'):
    return {
        'passed': bool(condition),
        'severity': 'ok' if condition else severity,
        'message': passed_message if condition else failed_message,
    }


def caption_exists(project_dir):
    candidates = [
        project_dir / 'captions' / 'final.srt',
        project_dir / 'captions' / 'final.vtt',
        project_dir / 'exports' / 'final.srt',
        project_dir / 'exports' / 'final.vtt',
    ]
    return any(path.exists() for path in candidates)


def build_validation(project):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    preset = load_json(project_dir / 'export_preset.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    quality = load_json(project_dir / 'quality_score.json', {})
    script_timing = load_json(project_dir / 'script_timing.json', {})

    platform = metadata.get('platform') or manifest.get('platform') or preset.get('platform') or 'youtube-shorts'
    rules = PLATFORM_RULES.get(platform, PLATFORM_RULES['youtube-shorts'])
    duration = float(script_timing.get('estimated_seconds') or manifest.get('duration_seconds') or 0)
    title = metadata.get('title') or manifest.get('name') or project_dir.name
    hashtags = normalize_hashtags(metadata.get('hashtags', []))
    aspect_ratio = preset.get('aspect_ratio', '')
    quality_score = float(quality.get('final_score_percent') or 0)

    checks = {
        'duration': check(
            duration <= rules['max_duration_seconds'] if duration else False,
            f'Duration {duration}s fits {platform}.',
            f'Duration {duration}s exceeds or is missing for {platform} max {rules["max_duration_seconds"]}s.',
        ),
        'aspect_ratio': check(
            aspect_ratio == rules['preferred_aspect_ratio'],
            f'Aspect ratio {aspect_ratio} matches {platform}.',
            f'Aspect ratio should be {rules["preferred_aspect_ratio"]} for {platform}, found {aspect_ratio or "missing"}.',
        ),
        'title_length': check(
            len(title) <= rules['max_title_length'],
            f'Title length {len(title)} is valid.',
            f'Title length {len(title)} exceeds max {rules["max_title_length"]}.',
        ),
        'hashtags': check(
            len(hashtags) <= rules['max_hashtags'],
            f'{len(hashtags)} hashtag(s) fit the platform limit.',
            f'{len(hashtags)} hashtag(s) exceed platform limit {rules["max_hashtags"]}.',
            severity='warning',
        ),
        'captions': check(
            caption_exists(project_dir) if rules['captions_recommended'] else True,
            'Captions file found.',
            'Captions are recommended but final SRT/VTT file is missing.',
            severity='warning',
        ),
        'quality_score': check(
            quality_score >= 70,
            f'Quality score {quality_score} is acceptable.',
            f'Quality score {quality_score} is below recommended 70.',
            severity='warning',
        ),
    }

    failed = [name for name, item in checks.items() if not item['passed'] and item['severity'] == 'error']
    warnings = [name for name, item in checks.items() if not item['passed'] and item['severity'] == 'warning']

    return {
        'project': str(project_dir),
        'platform': platform,
        'rules': rules,
        'checks': checks,
        'failed_errors': failed,
        'warnings': warnings,
        'status': 'valid' if not failed else 'blocked',
        'publish_advice': 'Ready for platform review.' if not failed else 'Fix blocking errors before publishing.',
    }


def main():
    parser = argparse.ArgumentParser(description='Validate an OpenMontage Plus project against platform publish rules')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out', default='projects/demo-video/platform_validation.json')
    args = parser.parse_args()

    report = build_validation(args.project)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
