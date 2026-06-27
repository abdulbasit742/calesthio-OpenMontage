#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

CHECKS = [
    {
        'key': 'final_packet_ready',
        'label': 'Final governance packet is ready',
        'source': 'final_packet',
    },
    {
        'key': 'handoff_note_ready',
        'label': 'Final handoff note is ready',
        'source': 'handoff_note',
    },
    {
        'key': 'no_packet_blockers',
        'label': 'Final packet has no blockers',
        'source': 'final_packet',
    },
    {
        'key': 'no_handoff_blockers',
        'label': 'Handoff note has no blockers',
        'source': 'handoff_note',
    },
]


def read_json(path_text):
    path = Path(path_text)
    if not path.exists():
        return {'load_status': 'missing', 'path': path_text, 'data': {}}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'load_status': 'invalid-json', 'path': path_text, 'data': {}}
    return {'load_status': 'loaded', 'path': path_text, 'data': data if isinstance(data, dict) else {}}


def blockers_from(data):
    blockers = data.get('blockers', [])
    return blockers if isinstance(blockers, list) else []


def build_checklist(packet_path, handoff_path, label):
    packet = read_json(packet_path)
    handoff = read_json(handoff_path)
    packet_data = packet['data']
    handoff_data = handoff['data']
    packet_blockers = blockers_from(packet_data)
    handoff_blockers = blockers_from(handoff_data)

    check_rows = [
        {
            'key': 'final_packet_ready',
            'label': 'Final governance packet is ready',
            'passed': packet['load_status'] == 'loaded' and packet_data.get('status') == 'final-packet-ready',
            'detail': f"packet_status={packet_data.get('status')}",
        },
        {
            'key': 'handoff_note_ready',
            'label': 'Final handoff note is ready',
            'passed': handoff['load_status'] == 'loaded' and handoff_data.get('handoff_status') == 'ready-to-handoff',
            'detail': f"handoff_status={handoff_data.get('handoff_status')}",
        },
        {
            'key': 'no_packet_blockers',
            'label': 'Final packet has no blockers',
            'passed': len(packet_blockers) == 0,
            'detail': f"blockers={len(packet_blockers)}",
        },
        {
            'key': 'no_handoff_blockers',
            'label': 'Handoff note has no blockers',
            'passed': len(handoff_blockers) == 0,
            'detail': f"blockers={len(handoff_blockers)}",
        },
    ]
    failed = [row for row in check_rows if not row['passed']]
    status = 'delivery-ready' if not failed else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'status': status,
        'packet_path': packet_path,
        'handoff_path': handoff_path,
        'packet_load_status': packet['load_status'],
        'handoff_load_status': handoff['load_status'],
        'check_count': len(check_rows),
        'passed_count': len(check_rows) - len(failed),
        'failed_count': len(failed),
        'checks': check_rows,
        'recommendations': recommendations(failed),
    }


def recommendations(failed):
    if not failed:
        return [
            'Attach ARCHIVE_GOVERNANCE_FINAL_PACKET.md and ARCHIVE_GOVERNANCE_FINAL_HANDOFF_NOTE.md to the archive delivery package.',
            'Store the final checklist beside the final governance packet for reviewer sign-off.',
        ]
    return [f"Resolve failed delivery check: {row['label']} ({row['detail']})" for row in failed]


def render_markdown(checklist):
    lines = [
        '# Archive Governance Final Delivery Checklist',
        '',
        f"Generated UTC: {checklist['generated_on_utc']}",
        f"Label: **{checklist['label']}**",
        f"Status: **{checklist['status']}**",
        f"Packet source: `{checklist['packet_path']}`",
        f"Handoff source: `{checklist['handoff_path']}`",
        f"Checks: **{checklist['check_count']}**",
        f"Passed: **{checklist['passed_count']}**",
        f"Failed: **{checklist['failed_count']}**",
        '',
        '## Checks',
        '| Check | Passed | Detail |',
        '| --- | --- | --- |',
    ]
    for row in checklist['checks']:
        lines.append(f"| {row['label']} | {row['passed']} | `{row['detail']}` |")
    lines.extend(['', '## Recommendations'])
    for item in checklist['recommendations']:
        lines.append(f'- {item}')
    lines.append('')
    return '\n'.join(lines)


def write_checklist(packet_path, handoff_path, label, out_json, out_md):
    checklist = build_checklist(packet_path, handoff_path, label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(checklist, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(checklist), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': checklist['status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance delivery checklist')
    parser.add_argument('--packet', default='archive_governance_final_packet.json')
    parser.add_argument('--handoff', default='archive_governance_final_handoff_note.json')
    parser.add_argument('--label', default='archive-governance-final-delivery')
    parser.add_argument('--out-json', default='archive_governance_final_delivery_checklist.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md')
    args = parser.parse_args()

    result = write_checklist(args.packet, args.handoff, args.label, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
