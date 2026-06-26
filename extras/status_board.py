#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

BOARD_COLUMNS = [
    'Project',
    'Platform',
    'Status',
    'Quality',
    'Validation',
    'Publish Date',
    'Release Notes',
]


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def discover_projects(root):
    root_path = Path(root)
    if not root_path.exists():
        return []
    return [item for item in sorted(root_path.iterdir()) if item.is_dir() and (item / 'production_manifest.json').exists()]


def read_calendar_map(calendar_path):
    calendar = load_json(calendar_path, {})
    rows = calendar.get('calendar', []) if isinstance(calendar, dict) else []
    by_folder = {}
    for row in rows:
        folder = row.get('project_folder')
        if folder:
            by_folder[folder] = row
    return by_folder


def project_row(project_dir, calendar_map):
    manifest = load_json(project_dir / 'production_manifest.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    quality = load_json(project_dir / 'quality_score.json', {})
    validation = load_json(project_dir / 'platform_validation.json', {})
    release = load_json(project_dir / 'release_notes.json', {})
    publish = load_json(project_dir / 'publish' / 'publish_manifest.json', {})

    project_name = manifest.get('name') or project_dir.name
    platform = metadata.get('platform') or manifest.get('platform') or validation.get('platform') or 'unknown'
    status = quality.get('status') or publish.get('status') or manifest.get('status', 'draft')
    quality_score = quality.get('final_score_percent', '')
    validation_status = validation.get('status', 'not-checked')
    calendar_row = calendar_map.get(str(project_dir), {})
    release_file = project_dir / 'RELEASE_NOTES.md'

    return {
        'project': project_name,
        'project_folder': str(project_dir),
        'platform': platform,
        'status': status,
        'quality_score': quality_score,
        'validation_status': validation_status,
        'publish_date': calendar_row.get('publish_date', ''),
        'publish_time': calendar_row.get('publish_time', ''),
        'release_notes': str(release_file) if release_file.exists() or release else '',
        'warnings': validation.get('warnings', []),
        'blocking_errors': validation.get('failed_errors', []),
    }


def board_summary(rows):
    return {
        'total_projects': len(rows),
        'publish_ready': len([row for row in rows if row.get('status') == 'publish-ready' or row.get('validation_status') == 'valid']),
        'blocked': len([row for row in rows if row.get('validation_status') == 'blocked']),
        'needs_work': len([row for row in rows if row.get('status') in {'needs-work', 'not-ready'}]),
    }


def markdown_table(rows):
    header = '| ' + ' | '.join(BOARD_COLUMNS) + ' |'
    separator = '| ' + ' | '.join(['---'] * len(BOARD_COLUMNS)) + ' |'
    lines = [header, separator]
    for row in rows:
        release = row['release_notes'] or 'missing'
        quality = str(row['quality_score']) if row['quality_score'] != '' else 'not scored'
        publish_at = ' '.join([row.get('publish_date', ''), row.get('publish_time', '')]).strip() or 'not scheduled'
        values = [
            row['project'],
            row['platform'],
            row['status'],
            quality,
            row['validation_status'],
            publish_at,
            release,
        ]
        lines.append('| ' + ' | '.join(str(value).replace('|', '/') for value in values) + ' |')
    return '\n'.join(lines)


def render_markdown(board):
    summary = board['summary']
    return '\n'.join([
        '# OpenMontage Plus Project Status Board',
        '',
        f"Generated: {board['generated_on']}",
        '',
        '## Summary',
        f"- Total projects: {summary['total_projects']}",
        f"- Publish ready: {summary['publish_ready']}",
        f"- Blocked: {summary['blocked']}",
        f"- Needs work: {summary['needs_work']}",
        '',
        '## Board',
        markdown_table(board['projects']),
        '',
    ])


def build_status_board(projects_root, calendar_path):
    calendar_map = read_calendar_map(calendar_path)
    rows = [project_row(project, calendar_map) for project in discover_projects(projects_root)]
    return {
        'generated_on': date.today().isoformat(),
        'projects_root': str(projects_root),
        'calendar_source': str(calendar_path),
        'summary': board_summary(rows),
        'projects': rows,
    }


def main():
    parser = argparse.ArgumentParser(description='Build a Markdown and JSON project status board for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--calendar', default='content_calendar.json')
    parser.add_argument('--out-json', default='status_board.json')
    parser.add_argument('--out-md', default='STATUS_BOARD.md')
    args = parser.parse_args()

    board = build_status_board(args.projects_root, args.calendar)
    Path(args.out_json).write_text(json.dumps(board, indent=2), encoding='utf-8')
    Path(args.out_md).write_text(render_markdown(board), encoding='utf-8')
    print(json.dumps(board, indent=2))


if __name__ == '__main__':
    main()
