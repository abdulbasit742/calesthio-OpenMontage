#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SNAPSHOT_FILES = [
    'ARCHIVE_TOOLCHAIN_AUDIT.md',
    'PORTFOLIO_ARCHIVE_PLAN.md',
    'ARCHIVE_STATUS_BOARD.md',
    'ARCHIVE_BADGE_BOARD.md',
    'ARCHIVE_COMPLETION_BOARD.md',
    'ARCHIVE_PORTFOLIO_SUMMARY.md',
    'ARCHIVE_PORTFOLIO_PACKLIST.md',
    'ARCHIVE_PORTFOLIO_INDEX.md',
    'ARCHIVE_PORTFOLIO_DASHBOARD.md',
    'ARCHIVE_PORTFOLIO_DIGEST.md',
    'ARCHIVE_PORTFOLIO_RUNBOOK.md',
]

SNAPSHOT_JSON_FILES = [
    'archive_toolchain_audit.json',
    'portfolio_archive_plan.json',
    'archive_status_board.json',
    'archive_badge_board.json',
    'archive_completion_board.json',
    'archive_portfolio_summary.json',
    'archive_portfolio_packlist.json',
    'archive_portfolio_index.json',
    'archive_portfolio_dashboard.json',
    'archive_portfolio_digest.json',
    'archive_portfolio_runbook.json',
]


def file_info(path):
    file_path = Path(path)
    if not file_path.exists():
        return {
            'path': str(file_path),
            'exists': False,
            'size_bytes': 0,
            'modified_utc': '',
        }
    stat = file_path.stat()
    return {
        'path': str(file_path),
        'exists': True,
        'size_bytes': stat.st_size,
        'modified_utc': datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
    }


def build_snapshot(projects_root='projects', label='archive-portfolio-final'):
    markdown_files = [file_info(path) for path in SNAPSHOT_FILES]
    json_files = [file_info(path) for path in SNAPSHOT_JSON_FILES]
    all_files = markdown_files + json_files
    missing = [item for item in all_files if not item['exists']]
    available = [item for item in all_files if item['exists']]
    total_size = sum(item['size_bytes'] for item in available)
    return {
        'label': label,
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'status': 'complete' if not missing else 'needs-attention',
        'expected_file_count': len(all_files),
        'available_file_count': len(available),
        'missing_file_count': len(missing),
        'total_size_bytes': total_size,
        'markdown_files': markdown_files,
        'json_files': json_files,
        'next_steps': build_next_steps(missing),
    }


def build_next_steps(missing):
    if not missing:
        return ['Snapshot manifest is complete. Keep this file with the final archive portfolio package.']
    return [f"Generate missing snapshot source: {item['path']}" for item in missing[:20]]


def render_table(rows):
    lines = [
        '| File | Exists | Size bytes | Modified UTC |',
        '| --- | --- | ---: | --- |',
    ]
    for row in rows:
        lines.append(f"| `{row['path']}` | {row['exists']} | {row['size_bytes']} | {row['modified_utc']} |")
    return lines


def render_markdown(snapshot):
    lines = [
        '# Archive Portfolio Snapshot',
        '',
        f"Label: **{snapshot['label']}**",
        f"Generated UTC: {snapshot['generated_on_utc']}",
        f"Projects root: `{snapshot['projects_root']}`",
        f"Status: **{snapshot['status']}**",
        f"Expected files: **{snapshot['expected_file_count']}**",
        f"Available files: **{snapshot['available_file_count']}**",
        f"Missing files: **{snapshot['missing_file_count']}**",
        f"Total available size: **{snapshot['total_size_bytes']} bytes**",
        '',
        '## Markdown Snapshot Files',
    ]
    lines.extend(render_table(snapshot['markdown_files']))
    lines.extend(['', '## JSON Snapshot Files'])
    lines.extend(render_table(snapshot['json_files']))
    lines.extend(['', '## Next Steps'])
    for step in snapshot['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_snapshot(projects_root, label, out_json, out_md):
    snapshot = build_snapshot(projects_root=projects_root, label=label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(snapshot), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': snapshot['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a timestamped archive portfolio snapshot manifest for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--label', default='archive-portfolio-final')
    parser.add_argument('--out-json', default='archive_portfolio_snapshot.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_SNAPSHOT.md')
    args = parser.parse_args()

    result = write_snapshot(args.projects_root, args.label, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
