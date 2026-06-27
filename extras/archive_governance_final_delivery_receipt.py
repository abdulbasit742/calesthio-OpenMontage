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


def build_receipt(checklist_path, sender, recipient, package_id, note):
    checklist = read_json(checklist_path)
    checklist_data = checklist['data']
    checklist_status = checklist_data.get('status')
    delivered = checklist['load_status'] == 'loaded' and checklist_status == 'delivery-ready'
    receipt_status = 'delivered' if delivered else 'needs-attention'
    failed_checks = [row for row in checklist_data.get('checks', []) if isinstance(row, dict) and not row.get('passed')]
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'package_id': package_id,
        'sender': sender,
        'recipient': recipient,
        'note': note,
        'receipt_status': receipt_status,
        'checklist_path': checklist_path,
        'checklist_load_status': checklist['load_status'],
        'checklist_status': checklist_status,
        'check_count': checklist_data.get('check_count', 0),
        'passed_count': checklist_data.get('passed_count', 0),
        'failed_count': checklist_data.get('failed_count', len(failed_checks)),
        'failed_checks': failed_checks,
        'next_steps': next_steps(receipt_status, failed_checks),
    }


def next_steps(status, failed_checks):
    if status == 'delivered':
        return [
            'Archive reviewer can acknowledge receipt of the final delivery package.',
            'Store this receipt with the final packet, handoff note, and delivery checklist.',
        ]
    if failed_checks:
        return [f"Resolve failed check before delivery: {row.get('label', row.get('key'))}" for row in failed_checks]
    return ['Regenerate the final delivery checklist and rerun this receipt builder.']


def render_markdown(receipt):
    lines = [
        '# Archive Governance Final Delivery Receipt',
        '',
        f"Generated UTC: {receipt['generated_on_utc']}",
        f"Package ID: **{receipt['package_id']}**",
        f"Receipt status: **{receipt['receipt_status']}**",
        f"Sender: **{receipt['sender']}**",
        f"Recipient: **{receipt['recipient']}**",
        f"Checklist source: `{receipt['checklist_path']}`",
        f"Checklist status: **{receipt['checklist_status']}**",
        f"Checks: **{receipt['check_count']}**",
        f"Passed: **{receipt['passed_count']}**",
        f"Failed: **{receipt['failed_count']}**",
        '',
        '## Note',
        receipt['note'] or '-',
        '',
        '## Failed Checks',
    ]
    if receipt['failed_checks']:
        for row in receipt['failed_checks']:
            lines.append(f"- {row.get('label', row.get('key'))}: `{row.get('detail', '-')}`")
    else:
        lines.append('- None')
    lines.extend(['', '## Next Steps'])
    for item in receipt['next_steps']:
        lines.append(f'- {item}')
    lines.append('')
    return '\n'.join(lines)


def write_receipt(checklist, sender, recipient, package_id, note, out_json, out_md):
    receipt = build_receipt(checklist, sender, recipient, package_id, note)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(receipt), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': receipt['receipt_status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance delivery receipt')
    parser.add_argument('--checklist', default='archive_governance_final_delivery_checklist.json')
    parser.add_argument('--sender', default='Archive Owner')
    parser.add_argument('--recipient', default='Archive Reviewer')
    parser.add_argument('--package-id', default='archive-governance-final-package')
    parser.add_argument('--note', default='Final archive governance package delivered for reviewer acknowledgement.')
    parser.add_argument('--out-json', default='archive_governance_final_delivery_receipt.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_FINAL_DELIVERY_RECEIPT.md')
    args = parser.parse_args()

    result = write_receipt(args.checklist, args.sender, args.recipient, args.package_id, args.note, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
