#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_NAME = 'project_archive_manifest.json'


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


def project_row(project_dir):
    manifest_path = project_dir / MANIFEST_NAME
    manifest = load_json(manifest_path, {})
    return {
        'project': project_dir.name,
        'project_path': str(project_dir),
        'manifest_exists': manifest_path.exists(),
        'archive_status': manifest.get('status', 'missing'),
        'closeout_status': manifest.get('closeout_status', 'missing'),
        'available_count': manifest.get('available_count', 0),
        'missing_count': manifest.get('missing_count', 0),
        'total_size_bytes': manifest.get('total_size_bytes', 0),
    }


def build_board(projects_root):
    projects = discover_projects(projects_root)
    rows = [project_row(project) for project in projects]
    status_counts = Counter(row['archive_status'] for row in rows)
    closeout_counts = Counter(row['closeout_status'] for row in rows)
    ready_rows = [row for row in rows if row['archive_status'] == 'archive-ready']
    attention_rows = [row for row in rows if row['archive_status'] != 'archive-ready']
    return {
        'projects_root': str(projects_root),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'archive-ready' if rows and not attention_rows else 'needs-attention',
        'project_count': len(rows),
        'archive_ready_count': len(ready_rows),
        'needs_attention_count': len(attention_rows),
        'status_counts': dict(sorted(status_counts.items())),
        'closeout_counts': dict(sorted(closeout_counts.items())),
        'rows': rows,
    }


def render_markdown(board):
    lines = [
        '# Archive Status Board',
        '',
        f"Generated UTC: {board['generated_on_utc']}",
        f"Projects root: `{board['projects_root']}`",
        f"Status: **{board['status']}**",
        f"Projects: **{board['project_count']}**",
        f"Archive ready: **{board['archive_ready_count']}**",
        f"Needs attention: **{board['needs_attention_count']}**",
        '',
        '## Archive Status Counts',
    ]
    if board['status_counts']:
        for status, count in board['status_counts'].items():
            lines.append(f'- {status}: {count}')
    else:
        lines.append('- None')
    lines.extend(['', '## Projects', '| Project | Archive Status | Closeout Status | Available | Missing | Size Bytes |', '| --- | --- | --- | ---: | ---: | ---: |'])
    if board['rows']:
        for row in board['rows']:
            lines.append(
                f"| `{row['project']}` | {row['archive_status']} | {row['closeout_status']} | {row['available_count']} | {row['missing_count']} | {row['total_size_bytes']} |"
            )
    else:
        lines.append('| - | missing | missing | 0 | 0 | 0 |')
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
    parser = argparse.ArgumentParser(description='Build a global archive readiness board for OpenMontage Plus projects')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_status_board.json')
    parser.add_argument('--out-md', default='ARCHIVE_STATUS_BOARD.md')
    args = parser.parse_args()

    board = build_board(args.projects_root)
    result = write_board(board, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
