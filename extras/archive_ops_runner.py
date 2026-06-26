#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STEPS = [
    {
        'name': 'closeout-ops',
        'script': 'extras/closeout_ops_runner.py',
        'args': ['--project', '{project}', '--client-name', '{client_name}', '--sender-name', '{sender_name}', '--out-json', '{project}/closeout_ops_report.json', '--out-md', '{project}/CLOSEOUT_OPS_REPORT.md'],
    },
    {
        'name': 'archive-manifest',
        'script': 'extras/project_archive_manifest.py',
        'args': ['--project', '{project}', '--out-json', '{project}/project_archive_manifest.json', '--out-md', '{project}/PROJECT_ARCHIVE_MANIFEST.md'],
    },
]


def render_arg(value, project, client_name, sender_name):
    return value.format(project=project, client_name=client_name, sender_name=sender_name)


def run_step(step, project, client_name, sender_name, dry_run=False):
    script = Path(step['script'])
    command = [sys.executable, str(script)] + [render_arg(value, project, client_name, sender_name) for value in step['args']]
    row = {
        'name': step['name'],
        'script': step['script'],
        'script_exists': script.exists(),
        'command': command,
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


def run_archive_ops(project, client_name, sender_name, dry_run=False, stop_on_failure=False):
    rows = []
    for step in STEPS:
        row = run_step(step, project, client_name, sender_name, dry_run=dry_run)
        rows.append(row)
        if stop_on_failure and row['status'] not in {'passed', 'dry-run'}:
            break
    failed = [row for row in rows if row['status'] not in {'passed', 'dry-run'}]
    return {
        'project': project,
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'dry_run': dry_run,
        'status': 'passed' if not failed else 'failed',
        'step_count': len(rows),
        'failed_count': len(failed),
        'steps': rows,
    }


def render_markdown(report):
    lines = [
        '# Archive Ops Runner Report',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Project: `{report['project']}`",
        f"Status: **{report['status']}**",
        f"Dry run: **{report['dry_run']}**",
        f"Steps: **{report['step_count']}**",
        f"Failed: **{report['failed_count']}**",
        '',
        '## Steps',
        '| Step | Status | Return Code | Script |',
        '| --- | --- | ---: | --- |',
    ]
    for row in report['steps']:
        lines.append(f"| {row['name']} | {row['status']} | {row['return_code']} | `{row['script']}` |")
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
    parser = argparse.ArgumentParser(description='Run closeout and archive manifest steps for an OpenMontage Plus project')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--client-name', default='')
    parser.add_argument('--sender-name', default='')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--stop-on-failure', action='store_true')
    parser.add_argument('--out-json', default='projects/demo-video/archive_ops_report.json')
    parser.add_argument('--out-md', default='projects/demo-video/ARCHIVE_OPS_REPORT.md')
    args = parser.parse_args()

    report = run_archive_ops(
        args.project,
        client_name=args.client_name,
        sender_name=args.sender_name,
        dry_run=args.dry_run,
        stop_on_failure=args.stop_on_failure,
    )
    result = write_report(report, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
