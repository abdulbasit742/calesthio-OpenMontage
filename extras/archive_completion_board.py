#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

COMPLETION_FILE = 'archive_completion_report.json'


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


def completion_row(project_dir):
    report_path = project_dir / COMPLETION_FILE
    report = load_json(report_path, {})
    return {
        'project': project_dir.name,
        'project_path': str(project_dir),
        'report_exists': report_path.exists(),
        'status': report.get('status', 'missing-report'),
        'archive_status': report.get('archive_status', 'missing'),
        'badge_level': report.get('badge_level', 'missing-badge'),
        'closeout_status': report.get('closeout_status', 'missing'),
        'feedback_status': report.get('feedback_status', 'missing'),
        'open_feedback_count': report.get('open_feedback_count', 0),
        'missing_source_count': report.get('missing_source_count', 0),
        'next_step_count': len(report.get('next_steps', [])),
    }


def build_board(projects_root):
    projects = discover_projects(projects_root)
    rows = [completion_row(project) for project in projects]
    status_counts = Counter(row['status'] for row in rows)
    complete_rows = [row for row in rows if row['status'] == 'complete']
    incomplete_rows = [row for row in rows if row['status'] != 'complete']
    return {
        'projects_root': str(projects_root),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'complete' if rows and not incomplete_rows else 'incomplete',
        'project_count': len(rows),
        'complete_count': len(complete_rows),
        'incomplete_count': len(incomplete_rows),
        'status_counts': dict(sorted(status_counts.items())),
        'rows': rows,
    }


def render_markdown(board):
    lines = [
        '# Archive Completion Board',
        '',
        f"Generated UTC: {board['generated_on_utc']}",
        f"Projects root: `{board['projects_root']}`",
        f"Status: **{board['status']}**",
        f"Projects: **{board['project_count']}**",
        f"Complete: **{board['complete_count']}**",
        f"Incomplete: **{board['incomplete_count']}**",
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
        '| Project | Status | Archive | Badge | Closeout | Feedback | Open Feedback | Missing Sources | Next Steps |',
        '| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |',
    ])
    if board['rows']:
        for row in board['rows']:
            lines.append(
                f"| `{row['project']}` | {row['status']} | {row['archive_status']} | {row['badge_level']} | {row['closeout_status']} | {row['feedback_status']} | {row['open_feedback_count']} | {row['missing_source_count']} | {row['next_step_count']} |"
            )
    else:
        lines.append('| - | missing-report | missing | missing-badge | missing | missing | 0 | 0 | 0 |')
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
    parser = argparse.ArgumentParser(description='Build a global archive completion board for OpenMontage Plus projects')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_completion_board.json')
    parser.add_argument('--out-md', default='ARCHIVE_COMPLETION_BOARD.md')
    args = parser.parse_args()

    board = build_board(args.projects_root)
    result = write_board(board, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
