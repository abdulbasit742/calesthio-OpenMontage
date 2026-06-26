#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def build_email(project, client_name, sender_name):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'delivery_manifest.json', {})
    badge = load_json(project_dir / 'delivery_readiness_badge.json', {})
    checklist = load_json(project_dir / 'delivery_handoff_checklist.json', {})
    project_name = project_dir.name.replace('-', ' ').title()
    readiness = badge.get('message', 'not-ready')
    handoff_status = checklist.get('status', 'needs-attention')
    available = manifest.get('available_count', 0)
    missing = manifest.get('missing_count', 0)
    subject = f'Final delivery package: {project_name}'
    greeting = f'Hi {client_name},' if client_name else 'Hi,'
    body_lines = [
        greeting,
        '',
        f'The final delivery package for {project_name} is prepared for review.',
        '',
        'Delivery status:',
        f'- Readiness badge: {readiness}',
        f'- Handoff checklist: {handoff_status}',
        f'- Manifest files available: {available}',
        f'- Manifest files missing: {missing}',
        '',
        'Included review files:',
        '- Delivery manifest',
        '- Delivery readiness badge',
        '- Delivery handoff checklist',
        '- Publishing metadata and instructions, when available',
        '',
        'Please review the package and let me know if any revision is required.',
        '',
        f'Best,\n{sender_name}' if sender_name else 'Best,',
    ]
    return {
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'subject': subject,
        'body': '\n'.join(body_lines),
        'source_statuses': {
            'readiness_badge': readiness,
            'handoff_checklist': handoff_status,
            'manifest_available_count': available,
            'manifest_missing_count': missing,
        },
    }


def render_markdown(email):
    return '\n'.join([
        '# Client Delivery Email Draft',
        '',
        f"Generated UTC: {email['generated_on_utc']}",
        f"Project: `{email['project']}`",
        '',
        f"**Subject:** {email['subject']}",
        '',
        '## Body',
        '',
        '```text',
        email['body'],
        '```',
        '',
    ])


def write_email(project, client_name, sender_name, out_json, out_md):
    email = build_email(project, client_name, sender_name)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(email, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(email), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'subject': email['subject']}


def main():
    parser = argparse.ArgumentParser(description='Build a client delivery email draft from OpenMontage Plus handoff reports')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--client-name', default='')
    parser.add_argument('--sender-name', default='')
    parser.add_argument('--out-json', default='projects/demo-video/client_delivery_email.json')
    parser.add_argument('--out-md', default='projects/demo-video/CLIENT_DELIVERY_EMAIL.md')
    args = parser.parse_args()

    result = write_email(args.project, args.client_name, args.sender_name, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
