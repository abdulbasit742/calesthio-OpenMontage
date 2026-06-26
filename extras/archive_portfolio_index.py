#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

INDEX_GROUPS = {
    'runbook': [
        'ARCHIVE_PORTFOLIO_RUNBOOK.md',
        'archive_portfolio_runbook.json',
    ],
    'summary': [
        'ARCHIVE_PORTFOLIO_SUMMARY.md',
        'archive_portfolio_summary.json',
        'ARCHIVE_PORTFOLIO_PACKLIST.md',
        'archive_portfolio_packlist.json',
    ],
    'boards': [
        'ARCHIVE_STATUS_BOARD.md',
        'archive_status_board.json',
        'ARCHIVE_BADGE_BOARD.md',
        'archive_badge_board.json',
        'ARCHIVE_COMPLETION_BOARD.md',
        'archive_completion_board.json',
    ],
    'plans': [
        'PORTFOLIO_ARCHIVE_PLAN.md',
        'portfolio_archive_plan.json',
        'ARCHIVE_BADGE_PLAN.md',
        'archive_badge_plan.json',
        'ARCHIVE_COMPLETION_PLAN.md',
        'archive_completion_plan.json',
    ],
    'audit': [
        'ARCHIVE_TOOLCHAIN_AUDIT.md',
        'archive_toolchain_audit.json',
    ],
}

PROJECT_INDEX_FILES = [
    'DELIVERY_MANIFEST.md',
    'DELIVERY_HANDOFF_CHECKLIST.md',
    'CLIENT_FEEDBACK_REPORT.md',
    'PROJECT_CLOSEOUT.md',
    'PROJECT_ARCHIVE_MANIFEST.md',
    'ARCHIVE_READINESS_BADGE.md',
    'ARCHIVE_COMPLETION_REPORT.md',
]


def row_for_file(path):
    return {
        'path': str(path),
        'name': path.name,
        'exists': path.exists(),
        'size_bytes': path.stat().st_size if path.exists() else 0,
    }


def discover_projects(projects_root):
    root = Path(projects_root)
    if not root.exists():
        return []
    return sorted([item for item in root.iterdir() if item.is_dir()], key=lambda item: item.name.lower())


def build_index(projects_root):
    groups = {}
    missing_count = 0
    for group, filenames in INDEX_GROUPS.items():
        rows = [row_for_file(Path(filename)) for filename in filenames]
        missing_count += len([row for row in rows if not row['exists']])
        groups[group] = rows

    project_rows = []
    for project in discover_projects(projects_root):
        files = [row_for_file(project / filename) for filename in PROJECT_INDEX_FILES]
        missing = len([row for row in files if not row['exists']])
        missing_count += missing
        project_rows.append({
            'project': project.name,
            'project_path': str(project),
            'available_count': len(files) - missing,
            'missing_count': missing,
            'files': files,
        })

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'status': 'complete' if missing_count == 0 else 'needs-attention',
        'group_count': len(groups),
        'project_count': len(project_rows),
        'missing_count': missing_count,
        'groups': groups,
        'projects': project_rows,
    }


def render_markdown(index):
    lines = [
        '# Archive Portfolio Index',
        '',
        f"Generated UTC: {index['generated_on_utc']}",
        f"Projects root: `{index['projects_root']}`",
        f"Status: **{index['status']}**",
        f"Portfolio groups: **{index['group_count']}**",
        f"Projects indexed: **{index['project_count']}**",
        f"Missing files: **{index['missing_count']}**",
        '',
        '## Portfolio Documents',
    ]
    for group, rows in index['groups'].items():
        lines.extend(['', f"### {group.title()}", '| File | Exists | Size |', '| --- | --- | ---: |'])
        for row in rows:
            lines.append(f"| `{row['name']}` | {row['exists']} | {row['size_bytes']} |")

    lines.extend(['', '## Project Documents'])
    if index['projects']:
        for project in index['projects']:
            lines.extend([
                '',
                f"### {project['project']}",
                f"Available: **{project['available_count']}**",
                f"Missing: **{project['missing_count']}**",
                '',
                '| File | Exists | Size |',
                '| --- | --- | ---: |',
            ])
            for row in project['files']:
                lines.append(f"| `{row['name']}` | {row['exists']} | {row['size_bytes']} |")
    else:
        lines.append('- No project folders found.')
    lines.append('')
    return '\n'.join(lines)


def write_index(projects_root, out_json, out_md):
    index = build_index(projects_root)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(index, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(index), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': index['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a searchable archive portfolio index for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_portfolio_index.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_INDEX.md')
    args = parser.parse_args()

    result = write_index(args.projects_root, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
