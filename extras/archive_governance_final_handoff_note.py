#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_final_packet(path_text):
    path = Path(path_text)
    if not path.exists():
        return {'load_status': 'missing', 'path': path_text, 'data': {}}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'load_status': 'invalid-json', 'path': path_text, 'data': {}}
    return {'load_status': 'loaded', 'path': path_text, 'data': data if isinstance(data, dict) else {}}


def build_handoff(packet_path, sender_name, recipient_name, note):
    packet = load_final_packet(packet_path)
    data = packet['data']
    packet_status = data.get('status')
    blockers = data.get('blockers', []) if isinstance(data.get('blockers'), list) else []
    next_steps = data.get('next_steps', []) if isinstance(data.get('next_steps'), list) else []
    handoff_status = 'ready-to-handoff' if packet_status == 'final-packet-ready' and not blockers else 'needs-attention'

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'handoff_status': handoff_status,
        'sender_name': sender_name,
        'recipient_name': recipient_name,
        'note': note,
        'final_packet_source': packet_path,
        'final_packet_load_status': packet['load_status'],
        'final_packet_status': packet_status,
        'final_packet_label': data.get('packet_label'),
        'file_count': data.get('file_count'),
        'available_count': data.get('available_count'),
        'missing_count': data.get('missing_count'),
        'blockers': blockers,
        'next_steps': next_steps or ['Review the final packet before archive delivery.'],
    }


def render_markdown(handoff):
    lines = [
        '# Archive Governance Final Handoff Note',
        '',
        f"Generated UTC: {handoff['generated_on_utc']}",
        f"Status: **{handoff['handoff_status']}**",
        f"From: **{handoff['sender_name']}**",
        f"To: **{handoff['recipient_name']}**",
        '',
        '## Note',
        handoff['note'] or 'Final archive governance packet is ready for review.',
        '',
        '## Final Packet Summary',
        f"Source: `{handoff['final_packet_source']}`",
        f"Load status: `{handoff['final_packet_load_status']}`",
        f"Packet status: `{handoff['final_packet_status']}`",
        f"Packet label: `{handoff['final_packet_label']}`",
        f"Files: **{handoff['file_count']}**",
        f"Available: **{handoff['available_count']}**",
        f"Missing: **{handoff['missing_count']}**",
        '',
        '## Blockers',
    ]
    if handoff['blockers']:
        for blocker in handoff['blockers']:
            lines.append(f'- {blocker}')
    else:
        lines.append('- None.')

    lines.extend(['', '## Next Steps'])
    for step in handoff['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_handoff(packet_path, sender_name, recipient_name, note, out_json, out_md):
    handoff = build_handoff(packet_path, sender_name, recipient_name, note)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(handoff, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(handoff), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': handoff['handoff_status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance handoff note')
    parser.add_argument('--packet', default='archive_governance_final_packet.json')
    parser.add_argument('--sender-name', default='Archive Owner')
    parser.add_argument('--recipient-name', default='Archive Reviewer')
    parser.add_argument('--note', default='Final archive governance packet is ready for review.')
    parser.add_argument('--out-json', default='archive_governance_final_handoff_note.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_FINAL_HANDOFF_NOTE.md')
    args = parser.parse_args()

    result = write_handoff(args.packet, args.sender_name, args.recipient_name, args.note, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
