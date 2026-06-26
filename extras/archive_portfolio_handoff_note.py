#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_FILES = {
    'release_packet': 'archive_portfolio_release_packet.json',
    'readiness_review': 'archive_portfolio_readiness_review.json',
    'digest': 'archive_portfolio_digest.json',
}

DEFAULT_ATTACHMENTS = [
    'ARCHIVE_PORTFOLIO_RELEASE_PACKET.md',
    'ARCHIVE_PORTFOLIO_READINESS_REVIEW.md',
    'ARCHIVE_PORTFOLIO_DIGEST.md',
    'ARCHIVE_PORTFOLIO_SNAPSHOT.md',
    'ARCHIVE_PORTFOLIO_RUNBOOK.md',
]


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json'}


def source_summary():
    rows = []
    for name, path in SOURCE_FILES.items():
        data = load_json(path)
        status = data.get('status', 'available') if isinstance(data, dict) else 'missing'
        rows.append({'name': name, 'path': path, 'exists': data is not None, 'status': status})
    return rows


def attachment_rows():
    rows = []
    for path in DEFAULT_ATTACHMENTS:
        file_path = Path(path)
        rows.append({
            'path': path,
            'exists': file_path.exists(),
            'size_bytes': file_path.stat().st_size if file_path.exists() else 0,
        })
    return rows


def collect_highlights(sources):
    highlights = []
    packet = sources.get('release_packet')
    review = sources.get('readiness_review')
    digest = sources.get('digest')
    if isinstance(packet, dict):
        highlights.append(f"Release packet status: {packet.get('status', 'unknown')}")
        highlights.append(f"Packet files available: {packet.get('available_file_count', 0)}/{packet.get('expected_file_count', 0)}")
    if isinstance(review, dict):
        highlights.append(f"Readiness review status: {review.get('status', 'unknown')}")
        highlights.append(f"Failed checks: {review.get('failed_check_count', 0)}")
    if isinstance(digest, dict):
        headline = digest.get('headline') or digest.get('status') or 'digest available'
        highlights.append(f"Executive digest: {headline}")
    if not highlights:
        highlights.append('Generate the release packet, readiness review, and digest before handoff.')
    return highlights[:8]


def build_next_actions(source_rows, attachments):
    actions = []
    for row in source_rows:
        if not row['exists']:
            actions.append(f"Generate missing source: {row['path']}")
        elif row['status'] not in {'ready', 'complete', 'ready-for-final-review', 'ready-to-package'}:
            actions.append(f"Review source status for {row['path']}: {row['status']}")
    for row in attachments:
        if not row['exists']:
            actions.append(f"Add missing handoff attachment: {row['path']}")
    if not actions:
        actions.append('Share the handoff note with the release packet and supporting archive portfolio files.')
    return actions[:12]


def build_handoff(projects_root='projects', recipient_name='', sender_name='', handoff_label='archive-portfolio-handoff'):
    sources = {name: load_json(path) for name, path in SOURCE_FILES.items()}
    source_rows = source_summary()
    attachments = attachment_rows()
    status = 'ready-to-send' if all(row['exists'] for row in source_rows) and all(row['exists'] for row in attachments) else 'needs-attention'
    return {
        'handoff_label': handoff_label,
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'recipient_name': recipient_name,
        'sender_name': sender_name,
        'status': status,
        'source_summary': source_rows,
        'attachments': attachments,
        'highlights': collect_highlights(sources),
        'next_actions': build_next_actions(source_rows, attachments),
    }


def render_markdown(handoff):
    recipient = handoff['recipient_name'] or 'Team'
    sender = handoff['sender_name'] or 'OpenMontage Plus'
    lines = [
        '# Archive Portfolio Handoff Note',
        '',
        f"Handoff label: **{handoff['handoff_label']}**",
        f"Generated UTC: {handoff['generated_on_utc']}",
        f"Projects root: `{handoff['projects_root']}`",
        f"Recipient: **{recipient}**",
        f"Sender: **{sender}**",
        f"Status: **{handoff['status']}**",
        '',
        f"Hello {recipient},",
        '',
        'The archive portfolio package is prepared for review. Please use the files below as the handoff set.',
        '',
        '## Highlights',
    ]
    for item in handoff['highlights']:
        lines.append(f'- {item}')
    lines.extend(['', '## Source Summary', '| Source | Path | Exists | Status |', '| --- | --- | --- | --- |'])
    for row in handoff['source_summary']:
        lines.append(f"| {row['name']} | `{row['path']}` | {row['exists']} | {row['status']} |")
    lines.extend(['', '## Handoff Attachments', '| File | Exists | Size bytes |', '| --- | --- | ---: |'])
    for row in handoff['attachments']:
        lines.append(f"| `{row['path']}` | {row['exists']} | {row['size_bytes']} |")
    lines.extend(['', '## Next Actions'])
    for action in handoff['next_actions']:
        lines.append(f'- {action}')
    lines.extend(['', f'Thanks,  ', sender, ''])
    return '\n'.join(lines)


def write_handoff(projects_root, recipient_name, sender_name, handoff_label, out_json, out_md):
    handoff = build_handoff(projects_root, recipient_name, sender_name, handoff_label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(handoff, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(handoff), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': handoff['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio handoff note for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--recipient-name', default='Team')
    parser.add_argument('--sender-name', default='OpenMontage Plus')
    parser.add_argument('--handoff-label', default='archive-portfolio-handoff')
    parser.add_argument('--out-json', default='archive_portfolio_handoff_note.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_HANDOFF_NOTE.md')
    args = parser.parse_args()

    result = write_handoff(args.projects_root, args.recipient_name, args.sender_name, args.handoff_label, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
