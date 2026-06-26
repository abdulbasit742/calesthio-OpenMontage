#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_BADGES = {
    'archive-ready': 'ARCHIVE READY',
    'needs-attention': 'NEEDS ATTENTION',
    'missing-manifest': 'MISSING MANIFEST',
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def badge_level(manifest_exists, manifest_status):
    if not manifest_exists:
        return 'missing-manifest'
    if manifest_status == 'archive-ready':
        return 'archive-ready'
    return 'needs-attention'


def build_badge(project):
    project_dir = Path(project)
    manifest_path = project_dir / 'project_archive_manifest.json'
    manifest_exists = manifest_path.exists()
    manifest = load_json(manifest_path, {})
    manifest_status = manifest.get('status', 'missing-manifest')
    level = badge_level(manifest_exists, manifest_status)
    missing_count = manifest.get('missing_count', 0)
    closeout_status = manifest.get('closeout_status', 'missing')
    return {
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'badge': DEFAULT_BADGES[level],
        'level': level,
        'archive_status': manifest_status,
        'closeout_status': closeout_status,
        'missing_count': missing_count,
        'available_count': manifest.get('available_count', 0),
        'message': badge_message(level, missing_count, closeout_status),
    }


def badge_message(level, missing_count, closeout_status):
    if level == 'archive-ready':
        return 'Project archive is ready and closeout files are complete.'
    if level == 'missing-manifest':
        return 'Archive manifest is missing. Run project_archive_manifest.py first.'
    if closeout_status != 'closed':
        return f'Project closeout status is {closeout_status}. Resolve closeout before archiving.'
    return f'Archive needs attention. Missing files: {missing_count}.'


def render_markdown(badge):
    lines = [
        '# Archive Readiness Badge',
        '',
        f"Generated UTC: {badge['generated_on_utc']}",
        f"Project: `{badge['project']}`",
        '',
        f"## {badge['badge']}",
        '',
        f"Level: **{badge['level']}**",
        f"Archive status: **{badge['archive_status']}**",
        f"Closeout status: **{badge['closeout_status']}**",
        f"Available files: **{badge['available_count']}**",
        f"Missing files: **{badge['missing_count']}**",
        '',
        f"Message: {badge['message']}",
        '',
    ]
    return '\n'.join(lines)


def write_badge(project, out_json, out_md):
    badge = build_badge(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(badge, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(badge), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'level': badge['level']}


def main():
    parser = argparse.ArgumentParser(description='Build a simple archive readiness badge from a project archive manifest')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/archive_readiness_badge.json')
    parser.add_argument('--out-md', default='projects/demo-video/ARCHIVE_READINESS_BADGE.md')
    args = parser.parse_args()

    result = write_badge(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
