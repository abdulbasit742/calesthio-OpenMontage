#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def read_json(path_text):
    path = Path(path_text)
    if not path.exists():
        return {'load_status': 'missing', 'path': path_text, 'data': {}}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'load_status': 'invalid-json', 'path': path_text, 'data': {}}
    return {'load_status': 'loaded', 'path': path_text, 'data': data if isinstance(data, dict) else {}}


def build_acknowledgement(receipt_path, reviewer_name, reviewer_role, decision, note):
    receipt = read_json(receipt_path)
    receipt_data = receipt['data']
    receipt_status = receipt_data.get('receipt_status')
    can_acknowledge = receipt['load_status'] == 'loaded' and receipt_status == 'delivered'
    normalized_decision = decision.strip().lower()
    accepted = can_acknowledge and normalized_decision in {'accepted', 'acknowledged', 'approved'}
    acknowledgement_status = 'acknowledged' if accepted else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'reviewer_name': reviewer_name,
        'reviewer_role': reviewer_role,
        'decision': normalized_decision,
        'note': note,
        'acknowledgement_status': acknowledgement_status,
        'receipt_path': receipt_path,
        'receipt_load_status': receipt['load_status'],
        'receipt_status': receipt_status,
        'package_id': receipt_data.get('package_id'),
        'sender': receipt_data.get('sender'),
        'recipient': receipt_data.get('recipient'),
        'next_steps': next_steps(acknowledgement_status, receipt['load_status'], receipt_status),
    }


def next_steps(status, load_status, receipt_status):
    if status == 'acknowledged':
        return [
            'Store this acknowledgement with the final delivery receipt and archive package.',
            'Mark the archive governance delivery as reviewer-acknowledged.',
        ]
    if load_status != 'loaded':
        return ['Regenerate or locate the final delivery receipt before acknowledgement.']
    if receipt_status != 'delivered':
        return ['Resolve the delivery receipt status before reviewer acknowledgement.']
    return ['Use decision accepted, acknowledged, or approved to complete acknowledgement.']


def render_markdown(record):
    lines = [
        '# Archive Governance Final Delivery Acknowledgement',
        '',
        f"Generated UTC: {record['generated_on_utc']}",
        f"Acknowledgement status: **{record['acknowledgement_status']}**",
        f"Reviewer: **{record['reviewer_name']}**",
        f"Role: **{record['reviewer_role']}**",
        f"Decision: **{record['decision']}**",
        f"Package ID: **{record['package_id']}**",
        f"Receipt source: `{record['receipt_path']}`",
        f"Receipt status: **{record['receipt_status']}**",
        '',
        '## Note',
        record['note'] or '-',
        '',
        '## Next Steps',
    ]
    for item in record['next_steps']:
        lines.append(f'- {item}')
    lines.append('')
    return '\n'.join(lines)


def write_acknowledgement(receipt, reviewer_name, reviewer_role, decision, note, out_json, out_md):
    record = build_acknowledgement(receipt, reviewer_name, reviewer_role, decision, note)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(record, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(record), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': record['acknowledgement_status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance delivery acknowledgement')
    parser.add_argument('--receipt', default='archive_governance_final_delivery_receipt.json')
    parser.add_argument('--reviewer-name', default='Archive Reviewer')
    parser.add_argument('--reviewer-role', default='Final Delivery Reviewer')
    parser.add_argument('--decision', default='acknowledged')
    parser.add_argument('--note', default='Reviewer acknowledges receipt of the final archive governance package.')
    parser.add_argument('--out-json', default='archive_governance_final_delivery_acknowledgement.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_FINAL_DELIVERY_ACKNOWLEDGEMENT.md')
    args = parser.parse_args()

    result = write_acknowledgement(args.receipt, args.reviewer_name, args.reviewer_role, args.decision, args.note, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
