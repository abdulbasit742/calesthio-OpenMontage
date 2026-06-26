#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BADGE_FILE = 'archive_readiness_badge.json'


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def discover_projects(projects_root):
    root = Path(projects_root)
    if not root.exists():
        return []
    return sorted([item for item in root.iterdir() if item.is_dir()], key=lambda item: item.name.lower())


def badge_row(project_dir):
    badge_path = project_dir / BADGE_FILE
    badge = load_json(badge_path, {})
    return {
        'project': project_dir.name,
        'project_path': str(project_dir),
        'badge_exists': badge_path.exists(),
        'badge': badge.get('badge', 'MISSING BADGE'),
        'level': badge.get('level', 'missing-badge'),
        'archive_status': badge.get('archive_status', 'missing'),
        'closeout_status': badge.get('closeout_status', 'missing'),
        'available_count': badge.get('available_count', 0),
        'missing_count': badge.get('missing_count', 0),
        'message': badge.get('message', 'Run archive_readiness_badge.py for this project.'),
    }


def build_board(projects_root):
    projects = discover_projects(projects_root)
    rows = [badge_row(project) for project in projects]
    level_counts = Counter(row['level'] for row in rows)
    ready_rows = [row for row in rows if row['level'] == 'archive-ready']
    attention_rows = [row for row in rows if row['level'] != 'archive-ready']
    return {
        'projects_root': str(projects_root),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'archive-ready' if rows and not attention_rows else 'needs-attention',
        'project_count': len(rows),
        'archive_ready_count': len(ready_rows),
        'needs_attention_count': len(attention_rows),
        'level_counts': dict(sorted(level_counts.items())),
        'rows': rows,
    }


def render_markdown(board):
    lines = [
        '# Archive Badge Board',
        '',
        f"Generated UTC: {board['generated_on_utc']}",
        f"Projects root: `{board['projects_root']}`",
        f"Status: **{board['status']}**",
        f"Projects: **{board['project_count']}**",
        f"Archive ready: **{board['archive_ready_count']}**",
        f"Needs attention: **{board['needs_attention_count']}**",
        '',
        '## Badge Level Counts',
    ]
    if board['level_counts']:
        for level, count in board['level_counts'].items():
            lines.append(f'- {level}: {count}')
    else:
        lines.append('- None')
    lines.extend([
        '',
        '## Projects',
        '| Project | Badge | Level | Archive Status | Closeout Status | Missing | Message |',
        '| --- | --- | --- | --- | --- | ---: | --- |',
    ])
    if board['rows']:
        for row in board['rows']:
            safe_message = row['message'].replace('|', '/')
            lines.append(
                f"| `{row['project']}` | {row['badge']} | {row['level']} | {row['archive_status']} | {row['closeout_status']} | {row['missing_count']} | {safe_message} |"
            )
    else:
        lines.append('| - | MISSING BADGE | missing-badge | missing | missing | 0 | No projects found. |')
    lines.append('')
    return '\n'.join(lines)


def write_board(board, out_json, out_md):
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(board, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(board), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': board['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a global archive readiness badge board for OpenMontage Plus projects')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_badge_board.json')
    parser.add_argument('--out-md', default='ARCHIVE_BADGE_BOARD.md')
    args = parser.parse_args()

    board = build_board(args.projects_root)
    result = write_board(board, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
