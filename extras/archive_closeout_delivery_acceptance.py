#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DELIVERY_CHECK = 'archive_closeout_delivery_check.json'


def load_json(path):
    source = Path(path)
    if not source.exists():
        return {'exists': False, 'loaded': False, 'data': {}, 'error': 'missing-file'}
    try:
        return {'exists': True, 'loaded': True, 'data': json.loads(source.read_text(encoding='utf-8')), 'error': None}
    except json.JSONDecodeError as exc:
        return {'exists': True, 'loaded': False, 'data': {}, 'error': f'invalid-json: {exc}'}


def build_acceptance(delivery_check, owner, reviewer, label, acceptance_note):
    check = load_json(delivery_check)
    check_status = check['data'].get('delivery_check_status', 'missing-or-invalid') if check['loaded'] else 'missing-or-invalid'
    accepted = check_status == 'passed'
    blockers = [] if accepted else [f'Delivery check status is {check_status}; expected passed.']

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'reviewer': reviewer,
        'delivery_check': {
            'path': delivery_check,
            'exists': check['exists'],
            'loaded': check['loaded'],
            'status': check_status,
            'error': check['error'],
        },
        'acceptance_status': 'accepted' if accepted else 'blocked',
        'acceptance_note': acceptance_note,
        'blockers': blockers,
        'next_steps': next_steps(accepted),
    }


def next_steps(accepted):
    if accepted:
        return [
            'Store this acceptance record with the final archive package.',
            'Use the accepted status as the final owner/reviewer delivery acknowledgement checkpoint.',
        ]
    return [
        'Resolve the delivery check blockers.',
        'Regenerate the delivery check report.',
        'Rerun this acceptance builder after the delivery check reports passed.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Delivery Acceptance',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Owner: **{report['owner']}**",
        f"Reviewer: **{report['reviewer']}**",
        f"Acceptance status: **{report['acceptance_status']}**",
        '',
        '## Delivery Check Source',
        '',
        f"- Path: `{report['delivery_check']['path']}`",
        f"- Exists: `{report['delivery_check']['exists']}`",
        f"- Loaded: `{report['delivery_check']['loaded']}`",
        f"- Status: `{report['delivery_check']['status']}`",
        f"- Error: `{report['delivery_check']['error']}`",
        '',
        '## Acceptance Note',
        '',
        report['acceptance_note'],
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


def write_acceptance(args):
    report = build_acceptance(args.delivery_check, args.owner, args.reviewer, args.label, args.acceptance_note)
    Path(args.out_json).write_text(json.dumps(report, indent=2), encoding='utf-8')
    Path(args.out_md).write_text(render_markdown(report), encoding='utf-8')
    return {'json': args.out_json, 'markdown': args.out_md, 'status': report['acceptance_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout delivery acceptance record')
    parser.add_argument('--delivery-check', default=DEFAULT_DELIVERY_CHECK)
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--reviewer', default='Archive Reviewer')
    parser.add_argument('--label', default='archive-closeout-delivery-acceptance')
    parser.add_argument('--acceptance-note', default='Delivery acceptance is based on a passed archive closeout delivery check.')
    parser.add_argument('--out-json', default='archive_closeout_delivery_acceptance.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_DELIVERY_ACCEPTANCE.md')
    args = parser.parse_args()
    print(json.dumps(write_acceptance(args), indent=2))


if __name__ == '__main__':
    main()
