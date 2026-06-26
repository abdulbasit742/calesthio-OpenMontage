#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

REPORT_FILES = {
    'platform_validation': 'platform_validation.json',
    'delivery_audit': 'delivery_audit.json',
    'content_review': 'content_risk_check.json',
    'client_review': 'client_review_checklist.json',
    'revision_report': 'revision_report.json',
    'approval_gate': 'approval_gate.json',
    'quality_score': 'quality_score.json',
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def report_status(name, data):
    if not data:
        return 'missing'
    if name == 'quality_score':
        score = data.get('final_score_percent') or data.get('score') or 0
        return 'passed' if float(score or 0) >= 70 else 'needs-work'
    if name == 'client_review':
        return data.get('revision_summary', {}).get('approval_decision') or data.get('status') or 'pending'
    return data.get('status') or ('available' if data else 'missing')


def build_summary(project):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    reports = {}
    statuses = {}
    for name, filename in REPORT_FILES.items():
        data = load_json(project_dir / filename, {})
        reports[name] = data
        statuses[name] = report_status(name, data)

    blockers = []
    warnings = []
    for name, status in statuses.items():
        if status in {'blocked', 'failed', 'missing', 'not-ready'}:
            blockers.append({'name': name, 'status': status})
        elif status in {'needs-review', 'needs-work', 'pending'}:
            warnings.append({'name': name, 'status': status})

    quality_score = reports['quality_score'].get('final_score_percent') or reports['quality_score'].get('score') or 0
    project_name = manifest.get('name') or project_dir.name
    ready = not blockers

    return {
        'project': project_name,
        'project_folder': str(project_dir),
        'generated_on': date.today().isoformat(),
        'status': 'ready-for-final-review' if ready else 'blocked',
        'quality_score': quality_score,
        'statuses': statuses,
        'blockers': blockers,
        'warnings': warnings,
        'recommended_next_steps': next_steps(blockers, warnings),
    }


def next_steps(blockers, warnings):
    steps = []
    if blockers:
        steps.append('Fix missing or blocked reports before final delivery.')
    if warnings:
        steps.append('Review warning reports and document approvals or edits.')
    if not blockers and not warnings:
        steps.append('Project is ready for final human review and delivery decision.')
    steps.append('Run approval gate after all reports are refreshed.')
    return steps


def render_markdown(summary):
    lines = [
        f"# Project Review Summary: {summary['project']}",
        '',
        f"Generated: {summary['generated_on']}",
        f"Status: **{summary['status']}**",
        f"Quality score: **{summary['quality_score']}**",
        '',
        '## Report Statuses',
        '| Report | Status |',
        '| --- | --- |',
    ]
    for name, status in summary['statuses'].items():
        lines.append(f'| {name} | {status} |')
    lines.extend(['', '## Blockers'])
    if summary['blockers']:
        for item in summary['blockers']:
            lines.append(f"- {item['name']}: {item['status']}")
    else:
        lines.append('- None')
    lines.extend(['', '## Warnings'])
    if summary['warnings']:
        for item in summary['warnings']:
            lines.append(f"- {item['name']}: {item['status']}")
    else:
        lines.append('- None')
    lines.extend(['', '## Recommended Next Steps'])
    for step in summary['recommended_next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_summary(project, out_json, out_md):
    summary = build_summary(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(summary), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': summary['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a combined project review summary from existing OpenMontage Plus reports')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/project_review_summary.json')
    parser.add_argument('--out-md', default='projects/demo-video/PROJECT_REVIEW_SUMMARY.md')
    args = parser.parse_args()

    result = write_summary(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
