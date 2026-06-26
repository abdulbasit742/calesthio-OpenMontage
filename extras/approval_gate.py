#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def gate_check(name, passed, blocking, message):
    return {
        'name': name,
        'passed': bool(passed),
        'blocking': bool(blocking),
        'message': message,
        'severity': 'ok' if passed else ('blocker' if blocking else 'warning'),
    }


def client_approved(checklist):
    decision = checklist.get('revision_summary', {}).get('approval_decision', 'pending')
    if decision == 'approved':
        return True
    final_items = [item for item in checklist.get('items', []) if item.get('id') == 'final-approval']
    return any(item.get('status') == 'approved' for item in final_items)


def active_revision_count(report):
    summary = report.get('summary', {})
    if 'open_active' in summary:
        return int(summary.get('open_active') or 0)
    revisions = report.get('revisions', [])
    return len([item for item in revisions if item.get('status') not in {'resolved', 'cancelled'}])


def build_approval_gate(project):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    validation = load_json(project_dir / 'platform_validation.json', {})
    delivery_audit = load_json(project_dir / 'delivery_audit.json', {})
    checklist = load_json(project_dir / 'client_review_checklist.json', {})
    revision_report = load_json(project_dir / 'revision_report.json', {})
    quality = load_json(project_dir / 'quality_score.json', {})

    project_name = manifest.get('name') or project_dir.name
    validation_status = validation.get('status', 'not-checked')
    delivery_status = delivery_audit.get('status', 'not-checked')
    quality_score = float(quality.get('final_score_percent') or 0)
    active_revisions = active_revision_count(revision_report)
    approved = client_approved(checklist)

    checks = [
        gate_check(
            'platform-validation',
            validation_status == 'valid',
            True,
            f'Platform validation status is {validation_status}.',
        ),
        gate_check(
            'delivery-audit',
            delivery_status == 'passed',
            True,
            f'Delivery audit status is {delivery_status}.',
        ),
        gate_check(
            'quality-score',
            quality_score >= 70,
            False,
            f'Quality score is {quality_score}; recommended minimum is 70.',
        ),
        gate_check(
            'active-revisions',
            active_revisions == 0,
            True,
            f'{active_revisions} active revision(s) remain.',
        ),
        gate_check(
            'client-approval',
            approved,
            True,
            'Client final approval is recorded.' if approved else 'Client final approval is still pending.',
        ),
    ]

    blockers = [item for item in checks if not item['passed'] and item['blocking']]
    warnings = [item for item in checks if not item['passed'] and not item['blocking']]
    status = 'approved-for-delivery' if not blockers else 'blocked'

    return {
        'project': project_name,
        'project_folder': str(project_dir),
        'generated_on': date.today().isoformat(),
        'status': status,
        'approved': status == 'approved-for-delivery',
        'checks': checks,
        'blocker_count': len(blockers),
        'warning_count': len(warnings),
        'blockers': blockers,
        'warnings': warnings,
        'decision': 'Deliver/publish now.' if status == 'approved-for-delivery' else 'Do not deliver yet. Fix blockers first.',
    }


def render_markdown(report):
    lines = [
        f"# Final Approval Gate: {report['project']}",
        '',
        f"Generated: {report['generated_on']}",
        f"Status: **{report['status']}**",
        f"Decision: **{report['decision']}**",
        '',
        '## Checks',
        '| Check | Severity | Passed | Message |',
        '| --- | --- | --- | --- |',
    ]
    for item in report['checks']:
        lines.append(f"| {item['name']} | {item['severity']} | {item['passed']} | {item['message'].replace('|', '/')} |")
    lines.extend([
        '',
        f"Blockers: {report['blocker_count']}",
        f"Warnings: {report['warning_count']}",
        '',
    ])
    return '\n'.join(lines)


def write_gate(project, out_json, out_md):
    report = build_approval_gate(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': report['status'], 'approved': report['approved']}


def main():
    parser = argparse.ArgumentParser(description='Run the final OpenMontage Plus approval gate before delivery or publishing')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/approval_gate.json')
    parser.add_argument('--out-md', default='projects/demo-video/APPROVAL_GATE.md')
    args = parser.parse_args()

    result = write_gate(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
