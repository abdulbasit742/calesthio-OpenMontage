#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_HANDOFF = 'archive_closeout_storage_handoff.json'


def load_json(path):
    source = Path(path)
    if not source.exists():
        return {'exists': False, 'loaded': False, 'data': {}, 'error': 'missing-file'}
    try:
        return {'exists': True, 'loaded': True, 'data': json.loads(source.read_text(encoding='utf-8')), 'error': None}
    except json.JSONDecodeError as exc:
        return {'exists': True, 'loaded': False, 'data': {}, 'error': f'invalid-json: {exc}'}


def build_receipt(handoff, owner, reviewer, storage_owner, receipt_id, label, receipt_note):
    handoff_record = load_json(handoff)
    handoff_status = handoff_record['data'].get('storage_handoff_status', 'missing-or-invalid') if handoff_record['loaded'] else 'missing-or-invalid'
    accepted = handoff_status == 'ready-for-storage'
    blockers = [] if accepted else [f'Storage handoff status is {handoff_status}; expected ready-for-storage.']

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'receipt_id': receipt_id,
        'owner': owner,
        'reviewer': reviewer,
        'storage_owner': storage_owner,
        'handoff_source': {
            'path': handoff,
            'exists': handoff_record['exists'],
            'loaded': handoff_record['loaded'],
            'status': handoff_status,
            'error': handoff_record['error'],
        },
        'storage_receipt_status': 'received' if accepted else 'blocked',
        'receipt_note': receipt_note,
        'blockers': blockers,
        'next_steps': next_steps(accepted),
    }


def next_steps(accepted):
    if accepted:
        return [
            'Record the receipt ID in the final archive package index.',
            'Keep this storage receipt with the archived package.',
            'Notify the reviewer that storage receipt has been recorded.',
        ]
    return [
        'Resolve storage handoff blockers.',
        'Regenerate the storage handoff report.',
        'Rerun this storage receipt builder after handoff reports ready-for-storage.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Storage Receipt',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Receipt ID: **{report['receipt_id']}**",
        f"Owner: **{report['owner']}**",
        f"Reviewer: **{report['reviewer']}**",
        f"Storage Owner: **{report['storage_owner']}**",
        f"Storage receipt status: **{report['storage_receipt_status']}**",
        '',
        '## Storage Handoff Source',
        '',
        f"- Path: `{report['handoff_source']['path']}`",
        f"- Exists: `{report['handoff_source']['exists']}`",
        f"- Loaded: `{report['handoff_source']['loaded']}`",
        f"- Status: `{report['handoff_source']['status']}`",
        f"- Error: `{report['handoff_source']['error']}`",
        '',
        '## Receipt Note',
        '',
        report['receipt_note'],
        '',
        '## Blockers',
    ]
    if report['blockers']:
        for blocker in report['blockers']:
            lines.append(f'- {blocker}')
    else:
        lines.append('- None')
    lines.extend(['', '## Next Steps'])
    for step in report['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_receipt(args):
    report = build_receipt(
        args.handoff,
        args.owner,
        args.reviewer,
        args.storage_owner,
        args.receipt_id,
        args.label,
        args.receipt_note,
    )
    Path(args.out_json).write_text(json.dumps(report, indent=2), encoding='utf-8')
    Path(args.out_md).write_text(render_markdown(report), encoding='utf-8')
    return {'json': args.out_json, 'markdown': args.out_md, 'status': report['storage_receipt_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout storage receipt record')
    parser.add_argument('--handoff', default=DEFAULT_HANDOFF)
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--reviewer', default='Archive Reviewer')
    parser.add_argument('--storage-owner', default='Storage Owner')
    parser.add_argument('--receipt-id', default='ARCHIVE-STORAGE-RECEIPT-001')
    parser.add_argument('--label', default='archive-closeout-storage-receipt')
    parser.add_argument('--receipt-note', default='Storage receipt is based on a ready-for-storage archive closeout handoff record.')
    parser.add_argument('--out-json', default='archive_closeout_storage_receipt.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_STORAGE_RECEIPT.md')
    args = parser.parse_args()
    print(json.dumps(write_receipt(args), indent=2))


if __name__ == '__main__':
    main()
