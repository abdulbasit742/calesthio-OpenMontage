#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_FILES = {
    'handoff_checklist': 'delivery_handoff_checklist.json',
    'delivery_manifest': 'delivery_manifest.json',
    'readiness_badge': 'delivery_readiness_badge.json',
    'feedback_report': 'client_feedback_report.json',
    'client_email': 'client_delivery_email.json',
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def source_status(project_dir):
    statuses = {}
    for key, filename in SOURCE_FILES.items():
        path = project_dir / filename
        data = load_json(path, {})
        statuses[key] = {
            'file': filename,
            'exists': path.exists(),
            'status': data.get('status') or data.get('message') or ('available' if path.exists() else 'missing'),
        }
    return statuses


def closeout_status(statuses):
    handoff = statuses['handoff_checklist']['status']
    readiness = statuses['readiness_badge']['status']
    feedback = statuses['feedback_report']['status']
    missing = [name for name, item in statuses.items() if not item['exists']]
    if missing:
        return 'needs-files', f'Missing closeout files: {", ".join(missing)}'
    if handoff != 'ready-for-handoff':
        return 'needs-handoff-review', 'Delivery handoff checklist is not ready.'
    if readiness != 'ready':
        return 'needs-readiness-review', 'Delivery readiness badge is not ready.'
    if feedback != 'ready-for-closeout':
        return 'feedback-open', 'Client feedback still needs review or resolution.'
    return 'closed', 'Project is ready to close out.'


def build_closeout(project):
    project_dir = Path(project)
    statuses = source_status(project_dir)
    status, message = closeout_status(statuses)
    return {
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': status,
        'message': message,
        'sources': statuses,
        'closeout_steps': closeout_steps(status),
    }


def closeout_steps(status):
    if status == 'closed':
        return [
            'Archive final delivery package.',
            'Save client approval and feedback report.',
            'Mark project as closed in the project tracker.',
        ]
    return [
        'Run delivery ops runner to refresh reports.',
        'Resolve any open client feedback.',
        'Refresh client feedback report and closeout builder.',
    ]


def render_markdown(closeout):
    lines = [
        '# Project Closeout Report',
        '',
        f"Generated UTC: {closeout['generated_on_utc']}",
        f"Project: `{closeout['project']}`",
        f"Status: **{closeout['status']}**",
        f"Message: {closeout['message']}",
        '',
        '## Source Files',
        '| Source | Exists | Status | File |',
        '| --- | --- | --- | --- |',
    ]
    for key, item in closeout['sources'].items():
        lines.append(f"| {key} | {item['exists']} | {item['status']} | `{item['file']}` |")
    lines.extend(['', '## Closeout Steps'])
    for step in closeout['closeout_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_closeout(project, out_json, out_md):
    closeout = build_closeout(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(closeout, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(closeout), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': closeout['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a final project closeout report for OpenMontage Plus delivery work')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/project_closeout.json')
    parser.add_argument('--out-md', default='projects/demo-video/PROJECT_CLOSEOUT.md')
    args = parser.parse_args()

    result = write_closeout(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
