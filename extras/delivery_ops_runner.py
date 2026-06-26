#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_STEPS = [
    {
        'name': 'report-index',
        'script': 'extras/report_index_builder.py',
        'args': ['--project', '{project}', '--out-json', '{project}/report_index.json', '--out-md', '{project}/REPORT_INDEX.md'],
    },
    {
        'name': 'delivery-readiness-badge',
        'script': 'extras/delivery_readiness_badge.py',
        'args': ['--project', '{project}', '--out-json', '{project}/delivery_readiness_badge.json', '--out-md', '{project}/DELIVERY_READINESS_BADGE.md'],
    },
]

GLOBAL_STEP = {
    'name': 'delivery-status-board',
    'script': 'extras/delivery_status_board.py',
    'args': ['--projects-root', '{projects_root}', '--out-json', 'delivery_status_board.json', '--out-md', 'DELIVERY_STATUS_BOARD.md'],
}


def discover_projects(root):
    root_path = Path(root)
    if not root_path.exists():
        return []
    return sorted([item for item in root_path.iterdir() if item.is_dir()], key=lambda item: item.name.lower())


def format_values(values, project='', projects_root='projects'):
    return [item.format(project=project, projects_root=projects_root) for item in values]


def run_command(step, project='', projects_root='projects', dry_run=False):
    script = Path(step['script'])
    command = [sys.executable, str(script)] + format_values(step['args'], project=project, projects_root=projects_root)
    row = {
        'name': step['name'],
        'project': project,
        'script': step['script'],
        'command': command,
        'script_exists': script.exists(),
        'status': 'pending',
        'return_code': None,
    }
    if not script.exists():
        row['status'] = 'missing-script'
        row['return_code'] = 127
        return row
    if dry_run:
        row['status'] = 'dry-run'
        row['return_code'] = 0
        return row
    completed = subprocess.run(command, text=True, capture_output=True)
    row['return_code'] = completed.returncode
    row['stdout'] = completed.stdout[-3000:]
    row['stderr'] = completed.stderr[-3000:]
    row['status'] = 'passed' if completed.returncode == 0 else 'failed'
    return row


def run_delivery_ops(projects_root, dry_run=False, stop_on_failure=False):
    rows = []
    projects = discover_projects(projects_root)
    for project in projects:
        for step in PROJECT_STEPS:
            row = run_command(step, project=str(project), projects_root=projects_root, dry_run=dry_run)
            rows.append(row)
            if stop_on_failure and row['status'] not in {'passed', 'dry-run'}:
                return build_report(projects_root, projects, rows, dry_run)
    board_row = run_command(GLOBAL_STEP, projects_root=projects_root, dry_run=dry_run)
    rows.append(board_row)
    return build_report(projects_root, projects, rows, dry_run)


def build_report(projects_root, projects, rows, dry_run):
    failed = [row for row in rows if row['status'] not in {'passed', 'dry-run'}]
    return {
        'projects_root': str(projects_root),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'dry_run': dry_run,
        'project_count': len(projects),
        'step_count': len(rows),
        'failed_count': len(failed),
        'status': 'passed' if not failed else 'failed',
        'steps': rows,
    }


def render_markdown(report):
    lines = [
        '# Delivery Ops Runner Report',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Projects root: `{report['projects_root']}`",
        f"Status: **{report['status']}**",
        f"Dry run: **{report['dry_run']}**",
        f"Projects: **{report['project_count']}**",
        f"Steps: **{report['step_count']}**",
        f"Failed: **{report['failed_count']}**",
        '',
        '## Steps',
        '| Step | Project | Status | Return Code |',
        '| --- | --- | --- | ---: |',
    ]
    for row in report['steps']:
        project = row.get('project') or '-'
        lines.append(f"| {row['name']} | `{project}` | {row['status']} | {row['return_code']} |")
    lines.append('')
    return '\n'.join(lines)


def write_report(report, out_json, out_md):
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': report['status']}


def main():
    parser = argparse.ArgumentParser(description='Refresh delivery report index, readiness badges, and delivery status board')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--stop-on-failure', action='store_true')
    parser.add_argument('--out-json', default='delivery_ops_report.json')
    parser.add_argument('--out-md', default='DELIVERY_OPS_REPORT.md')
    args = parser.parse_args()

    report = run_delivery_ops(args.projects_root, dry_run=args.dry_run, stop_on_failure=args.stop_on_failure)
    result = write_report(report, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
