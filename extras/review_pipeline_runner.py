#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

STEPS = [
    {
        'name': 'content-review',
        'script': 'extras/content_risk_checker.py',
        'args': ['--project', '{project}', '--out-json', '{project}/content_risk_check.json', '--out-md', '{project}/CONTENT_RISK_CHECK.md'],
    },
    {
        'name': 'quality-score',
        'script': 'extras/quality_score.py',
        'args': ['--project', '{project}', '--out', '{project}/quality_score.json'],
    },
    {
        'name': 'platform-check',
        'script': 'extras/platform_validator.py',
        'args': ['--project', '{project}', '--out', '{project}/platform_validation.json'],
    },
    {
        'name': 'project-review-summary',
        'script': 'extras/project_review_summary.py',
        'args': ['--project', '{project}', '--out-json', '{project}/project_review_summary.json', '--out-md', '{project}/PROJECT_REVIEW_SUMMARY.md'],
    },
    {
        'name': 'approval-gate',
        'script': 'extras/approval_gate.py',
        'args': ['--project', '{project}', '--out-json', '{project}/approval_gate.json', '--out-md', '{project}/APPROVAL_GATE.md'],
    },
]


def format_args(values, project):
    return [item.format(project=project) for item in values]


def run_step(step, project, dry_run=False):
    script = Path(step['script'])
    command = [sys.executable, str(script)] + format_args(step['args'], project)
    result = {
        'name': step['name'],
        'script': step['script'],
        'command': command,
        'script_exists': script.exists(),
        'status': 'pending',
        'return_code': None,
    }
    if not script.exists():
        result['status'] = 'missing-script'
        result['return_code'] = 127
        return result
    if dry_run:
        result['status'] = 'dry-run'
        result['return_code'] = 0
        return result
    completed = subprocess.run(command, text=True, capture_output=True)
    result['return_code'] = completed.returncode
    result['stdout'] = completed.stdout[-4000:]
    result['stderr'] = completed.stderr[-4000:]
    result['status'] = 'passed' if completed.returncode == 0 else 'failed'
    return result


def run_pipeline(project, dry_run=False, stop_on_failure=False):
    results = []
    for step in STEPS:
        result = run_step(step, project, dry_run=dry_run)
        results.append(result)
        if stop_on_failure and result['status'] not in {'passed', 'dry-run'}:
            break
    failed = [item for item in results if item['status'] not in {'passed', 'dry-run'}]
    return {
        'project': project,
        'generated_on': date.today().isoformat(),
        'dry_run': dry_run,
        'status': 'passed' if not failed else 'failed',
        'step_count': len(results),
        'failed_count': len(failed),
        'steps': results,
    }


def render_markdown(report):
    lines = [
        '# Review Pipeline Report',
        '',
        f"Generated: {report['generated_on']}",
        f"Project: `{report['project']}`",
        f"Status: **{report['status']}**",
        f"Dry run: **{report['dry_run']}**",
        '',
        '## Steps',
        '| Step | Status | Return Code | Script |',
        '| --- | --- | --- | --- |',
    ]
    for step in report['steps']:
        lines.append(f"| {step['name']} | {step['status']} | {step['return_code']} | `{step['script']}` |")
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
    parser = argparse.ArgumentParser(description='Run the OpenMontage Plus review pipeline for a project')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--stop-on-failure', action='store_true')
    parser.add_argument('--out-json', default='projects/demo-video/review_pipeline_report.json')
    parser.add_argument('--out-md', default='projects/demo-video/REVIEW_PIPELINE_REPORT.md')
    args = parser.parse_args()

    report = run_pipeline(args.project, dry_run=args.dry_run, stop_on_failure=args.stop_on_failure)
    result = write_report(report, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
