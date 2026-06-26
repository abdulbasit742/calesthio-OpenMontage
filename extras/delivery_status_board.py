#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

STATUS_PRIORITY = {
    'ready': 1,
    'review': 2,
    'needs_reports': 3,
    'blocked': 4,
    'unknown': 5,
    'missing': 6,
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def project_row(project_dir):
    badge = load_json(project_dir / 'delivery_readiness_badge.json', {})
    summary = load_json(project_dir / 'project_review_summary.json', {})
    index = load_json(project_dir / 'report_index.json', {})
    return {
        'project': project_dir.name,
        'path': str(project_dir),
        'delivery_status': badge.get('message', 'missing'),
        'badge_color': badge.get('color', 'lightgrey'),
        'human_message': badge.get('human_message', 'Generate delivery readiness badge.'),
        'review_status': summary.get('status', 'missing'),
        'report_index_status': index.get('status', 'missing'),
        'available_reports': index.get('available_count', 0),
        'missing_reports': index.get('missing_count', 0),
    }


def discover_projects(root):
    root_path = Path(root)
    if not root_path.exists():
        return []
    projects = [item for item in root_path.iterdir() if item.is_dir()]
    return sorted(projects, key=lambda item: item.name.lower())


def build_board(projects_root):
    rows = [project_row(project) for project in discover_projects(projects_root)]
    counts = Counter(row['delivery_status'] for row in rows)
    sorted_rows = sorted(rows, key=lambda row: (STATUS_PRIORITY.get(row['delivery_status'], 99), row['project']))
    return {
        'projects_root': str(projects_root),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'project_count': len(rows),
        'status_counts': dict(sorted(counts.items())),
        'projects': sorted_rows,
    }


def render_markdown(board):
    lines = [
        '# Delivery Status Board',
        '',
        f"Generated UTC: {board['generated_on_utc']}",
        f"Projects root: `{board['projects_root']}`",
        f"Project count: **{board['project_count']}**",
        '',
        '## Status Counts',
    ]
    if board['status_counts']:
        for status, count in board['status_counts'].items():
            lines.append(f'- {status}: {count}')
    else:
        lines.append('- None')
    lines.extend([
        '',
        '## Projects',
        '| Project | Delivery | Review | Reports | Message |',
        '| --- | --- | --- | --- | --- |',
    ])
    for row in board['projects']:
        reports = f"{row['available_reports']} available, {row['missing_reports']} missing"
        message = row['human_message'].replace('|', '/')
        lines.append(
            f"| {row['project']} | {row['delivery_status']} | {row['review_status']} | {reports} | {message} |"
        )
    lines.append('')
    return '\n'.join(lines)


def write_board(projects_root, out_json, out_md):
    board = build_board(projects_root)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(board, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(board), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'project_count': board['project_count']}


def main():
    parser = argparse.ArgumentParser(description='Build a delivery status board across OpenMontage Plus projects')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='delivery_status_board.json')
    parser.add_argument('--out-md', default='DELIVERY_STATUS_BOARD.md')
    args = parser.parse_args()

    result = write_board(args.projects_root, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
