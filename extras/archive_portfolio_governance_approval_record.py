#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_PACKET = 'archive_portfolio_governance_packet.json'
READY_STATUS = 'governance-packet-ready'


def read_json(path):
    target = Path(path)
    if not target.exists():
        return None
    try:
        return json.loads(target.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json'}


def build_record(packet_path=DEFAULT_PACKET, reviewer_name='Archive Owner', reviewer_role='Owner', review_note='Governance package reviewed'):
    packet = read_json(packet_path)
    packet_status = packet.get('status', 'missing') if isinstance(packet, dict) else 'missing'
    missing_files = packet.get('missing_files', []) if isinstance(packet, dict) else []
    attention_sources = packet.get('attention_sources', []) if isinstance(packet, dict) else []
    approved = packet_status == READY_STATUS and not missing_files and not attention_sources
    checklist = [
        {'item': 'Packet JSON exists', 'status': 'pass' if packet is not None else 'fail'},
        {'item': 'Packet status is governance-packet-ready', 'status': 'pass' if packet_status == READY_STATUS else 'fail'},
        {'item': 'No missing governance files', 'status': 'pass' if not missing_files else 'fail'},
        {'item': 'No attention sources remain', 'status': 'pass' if not attention_sources else 'fail'},
    ]
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'approved' if approved else 'needs-attention',
        'packet_path': packet_path,
        'packet_status': packet_status,
        'reviewer_name': reviewer_name,
        'reviewer_role': reviewer_role,
        'review_note': review_note,
        'approved': approved,
        'missing_file_count': len(missing_files),
        'attention_source_count': len(attention_sources),
        'checklist': checklist,
        'next_steps': [] if approved else [
            'Fix missing governance files or attention sources.',
            'Regenerate the governance packet, then rerun this approval record.',
        ],
    }


def render_markdown(record):
    lines = [
        '# Archive Portfolio Governance Approval Record',
        '',
        f"Generated UTC: {record['generated_on_utc']}",
        f"Status: **{record['status']}**",
        f"Packet: `{record['packet_path']}`",
        f"Packet status: `{record['packet_status']}`",
        f"Reviewer: **{record['reviewer_name']}**",
        f"Role: {record['reviewer_role']}",
        f"Review note: {record['review_note']}",
        '',
        '## Counts',
        f"- Missing files: {record['missing_file_count']}",
        f"- Attention sources: {record['attention_source_count']}",
        f"- Approved: {record['approved']}",
        '',
        '## Checklist',
        '| Item | Status |',
        '| --- | --- |',
    ]
    for item in record['checklist']:
        lines.append(f"| {item['item']} | {item['status']} |")
    lines.extend(['', '## Next Steps'])
    if record['next_steps']:
        for step in record['next_steps']:
            lines.append(f'- {step}')
    else:
        lines.append('- None. Governance package is approved.')
    lines.append('')
    return '\n'.join(lines)


def write_record(packet_path, reviewer_name, reviewer_role, review_note, out_json, out_md):
    record = build_record(packet_path, reviewer_name, reviewer_role, review_note)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(record, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(record), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': record['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio governance approval record for OpenMontage Plus')
    parser.add_argument('--packet', default=DEFAULT_PACKET)
    parser.add_argument('--reviewer-name', default='Archive Owner')
    parser.add_argument('--reviewer-role', default='Owner')
    parser.add_argument('--review-note', default='Governance package reviewed')
    parser.add_argument('--out-json', default='archive_portfolio_governance_approval_record.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_GOVERNANCE_APPROVAL_RECORD.md')
    args = parser.parse_args()

    result = write_record(args.packet, args.reviewer_name, args.reviewer_role, args.review_note, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
