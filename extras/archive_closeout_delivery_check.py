#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DELIVERY_SEAL = 'archive_closeout_delivery_seal.json'
DEFAULT_DELIVERY_INDEX = 'archive_closeout_delivery_index.json'


def load_json(path):
    source = Path(path)
    if not source.exists():
        return {'path': path, 'exists': False, 'loaded': False, 'data': {}, 'error': 'missing-file'}
    try:
        return {'path': path, 'exists': True, 'loaded': True, 'data': json.loads(source.read_text(encoding='utf-8')), 'error': None}
    except json.JSONDecodeError as exc:
        return {'path': path, 'exists': True, 'loaded': False, 'data': {}, 'error': f'invalid-json: {exc}'}


def build_check(delivery_seal, delivery_index, label, owner):
    seal = load_json(delivery_seal)
    index = load_json(delivery_index)

    seal_status = seal['data'].get('delivery_seal_status', 'missing-or-invalid') if seal['loaded'] else 'missing-or-invalid'
    index_status = index['data'].get('index_status', 'missing-or-invalid') if index['loaded'] else 'missing-or-invalid'

    blockers = []
    if seal_status != 'sealed':
        blockers.append(f'Delivery seal status is {seal_status}; expected sealed.')
    if index_status != 'complete':
        blockers.append(f'Delivery index status is {index_status}; expected complete.')

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'delivery_check_status': 'passed' if not blockers else 'blocked',
        'sources': {
            'delivery_seal': {
                'path': seal['path'],
                'exists': seal['exists'],
                'loaded': seal['loaded'],
                'status': seal_status,
                'error': seal['error'],
            },
            'delivery_index': {
                'path': index['path'],
                'exists': index['exists'],
                'loaded': index['loaded'],
                'status': index_status,
                'error': index['error'],
            },
        },
        'blockers': blockers,
        'next_steps': next_steps(blockers),
    }


def next_steps(blockers):
    if not blockers:
        return [
            'Store the delivery check with the final archive package.',
            'Use this report as the final quick pass/fail record for closeout delivery.',
        ]
    return [
        'Resolve the blockers listed in this report.',
        'Regenerate the delivery seal and delivery index if needed.',
        'Rerun this check after the source records are corrected.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Delivery Check',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Owner: **{report['owner']}**",
        f"Delivery check status: **{report['delivery_check_status']}**",
        '',
        '## Source Status',
        '',
        '| Source | Path | Exists | Loaded | Status | Error |',
        '|---|---|---|---|---|---|',
    ]
    for name, source in report['sources'].items():
        lines.append(
            f"| {name} | `{source['path']}` | `{source['exists']}` | `{source['loaded']}` | `{source['status']}` | `{source['error']}` |"
        )
    lines.extend(['', '## Blockers'])
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


def write_check(args):
    report = build_check(args.delivery_seal, args.delivery_index, args.label, args.owner)
    Path(args.out_json).write_text(json.dumps(report, indent=2), encoding='utf-8')
    Path(args.out_md).write_text(render_markdown(report), encoding='utf-8')
    return {'json': args.out_json, 'markdown': args.out_md, 'status': report['delivery_check_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout delivery check')
    parser.add_argument('--delivery-seal', default=DEFAULT_DELIVERY_SEAL)
    parser.add_argument('--delivery-index', default=DEFAULT_DELIVERY_INDEX)
    parser.add_argument('--label', default='archive-closeout-delivery-check')
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--out-json', default='archive_closeout_delivery_check.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_DELIVERY_CHECK.md')
    args = parser.parse_args()
    print(json.dumps(write_check(args), indent=2))


if __name__ == '__main__':
    main()
