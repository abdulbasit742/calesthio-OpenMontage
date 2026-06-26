#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

PORTFOLIO_FILES = [
    'archive_toolchain_audit.json',
    'ARCHIVE_TOOLCHAIN_AUDIT.md',
    'portfolio_archive_plan.json',
    'PORTFOLIO_ARCHIVE_PLAN.md',
    'archive_status_board.json',
    'ARCHIVE_STATUS_BOARD.md',
    'archive_badge_plan.json',
    'ARCHIVE_BADGE_PLAN.md',
    'archive_badge_board.json',
    'ARCHIVE_BADGE_BOARD.md',
    'archive_completion_plan.json',
    'ARCHIVE_COMPLETION_PLAN.md',
    'archive_completion_board.json',
    'ARCHIVE_COMPLETION_BOARD.md',
    'archive_portfolio_summary.json',
    'ARCHIVE_PORTFOLIO_SUMMARY.md',
    'archive_portfolio_runbook.json',
    'ARCHIVE_PORTFOLIO_RUNBOOK.md',
]

PROJECT_FILES = [
    'delivery_manifest.json',
    'DELIVERY_MANIFEST.md',
    'delivery_handoff_checklist.json',
    'DELIVERY_HANDOFF_CHECKLIST.md',
    'client_feedback_tracker.json',
    'client_feedback_report.json',
    'CLIENT_FEEDBACK_REPORT.md',
    'project_closeout.json',
    'PROJECT_CLOSEOUT.md',
    'project_archive_manifest.json',
    'PROJECT_ARCHIVE_MANIFEST.md',
    'archive_readiness_badge.json',
    'ARCHIVE_READINESS_BADGE.md',
    'archive_completion_report.json',
    'ARCHIVE_COMPLETION_REPORT.md',
]


def file_row(base_dir, filename):
    path = Path(base_dir) / filename
    return {
        'path': str(path),
        'filename': filename,
        'exists': path.exists(),
        'size_bytes': path.stat().st_size if path.exists() else 0,
    }


def discover_projects(projects_root):
    root = Path(projects_root)
    if not root.exists():
        return []
    return sorted([item for item in root.iterdir() if item.is_dir()], key=lambda item: item.name.lower())


def project_pack(project):
    rows = [file_row(project, filename) for filename in PROJECT_FILES]
    missing = [row for row in rows if not row['exists']]
    return {
        'project': project.name,
        'project_path': str(project),
        'expected_count': len(rows),
        'available_count': len(rows) - len(missing),
        'missing_count': len(missing),
        'files': rows,
    }


def build_packlist(projects_root):
    portfolio_rows = [file_row('.', filename) for filename in PORTFOLIO_FILES]
    portfolio_missing = [row for row in portfolio_rows if not row['exists']]
    projects = [project_pack(project) for project in discover_projects(projects_root)]
    total_project_expected = sum(project['expected_count'] for project in projects)
    total_project_missing = sum(project['missing_count'] for project in projects)
    status = 'complete' if not portfolio_missing and total_project_missing == 0 else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'status': status,
        'portfolio_expected_count': len(portfolio_rows),
        'portfolio_available_count': len(portfolio_rows) - len(portfolio_missing),
        'portfolio_missing_count': len(portfolio_missing),
        'project_count': len(projects),
        'project_expected_file_count': total_project_expected,
        'project_missing_file_count': total_project_missing,
        'portfolio_files': portfolio_rows,
        'projects': projects,
        'next_steps': next_steps(portfolio_missing, projects),
    }


def next_steps(portfolio_missing, projects):
    steps = []
    for row in portfolio_missing:
        steps.append(f"Generate portfolio file: {row['filename']}")
    for project in projects:
        if project['missing_count']:
            steps.append(f"Review {project['project']} missing files: {project['missing_count']}")
    if not steps:
        steps.append('Portfolio packlist is complete.')
    return steps


def render_markdown(packlist):
    lines = [
        '# Archive Portfolio Packlist',
        '',
        f"Generated UTC: {packlist['generated_on_utc']}",
        f"Projects root: `{packlist['projects_root']}`",
        f"Status: **{packlist['status']}**",
        f"Portfolio files: **{packlist['portfolio_available_count']} / {packlist['portfolio_expected_count']}**",
        f"Projects: **{packlist['project_count']}**",
        f"Project missing files: **{packlist['project_missing_file_count']}**",
        '',
        '## Portfolio Files',
        '| File | Exists | Size |',
        '| --- | --- | ---: |',
    ]
    for row in packlist['portfolio_files']:
        lines.append(f"| `{row['filename']}` | {row['exists']} | {row['size_bytes']} |")
    lines.extend(['', '## Project Packs'])
    if packlist['projects']:
        for project in packlist['projects']:
            lines.extend([
                '',
                f"### {project['project']}",
                f"Available: **{project['available_count']} / {project['expected_count']}**",
                f"Missing: **{project['missing_count']}**",
                '',
                '| File | Exists | Size |',
                '| --- | --- | ---: |',
            ])
            for row in project['files']:
                lines.append(f"| `{row['filename']}` | {row['exists']} | {row['size_bytes']} |")
    else:
        lines.append('- No project folders found.')
    lines.extend(['', '## Next Steps'])
    for step in packlist['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_packlist(projects_root, out_json, out_md):
    packlist = build_packlist(projects_root)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(packlist, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(packlist), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': packlist['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a final archive portfolio packlist for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_portfolio_packlist.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_PACKLIST.md')
    args = parser.parse_args()

    result = write_packlist(args.projects_root, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
