#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ACCEPTANCE = 'archive_closeout_delivery_acceptance.json'


def load_json(path):
    source = Path(path)
    if not source.exists():
        return {'exists': False, 'loaded': False, 'data': {}, 'error': 'missing-file'}
    try:
        return {'exists': True, 'loaded': True, 'data': json.loads(source.read_text(encoding='utf-8')), 'error': None}
    except json.JSONDecodeError as exc:
        return {'exists': True, 'loaded': False, 'data': {}, 'error': f'invalid-json: {exc}'}


def build_completion(acceptance, owner, reviewer, label, completion_note):
    acceptance_record = load_json(acceptance)
    acceptance_status = acceptance_record['data'].get('acceptance_status', 'missing-or-invalid') if acceptance_record['loaded'] else 'missing-or-invalid'
    complete = acceptance_status == 'accepted'
    blockers = [] if complete else [f'Delivery acceptance status is {acceptance_status}; expected accepted.']

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'reviewer': reviewer,
        'acceptance_source': {
            'path': acceptance,
            'exists': acceptance_record['exists'],
            'loaded': acceptance_record['loaded'],
            'status': acceptance_status,
            'error': acceptance_record['error'],
        },
        'package_completion_status': 'complete' if complete else 'blocked',
        'completion_note': completion_note,
        'blockers': blockers,
        'next_steps': next_steps(complete),
    }


def next_steps(complete):
    if complete:
        return [
            'Store this package completion record with the final archive package.',
            'Use the complete status as the final closeout package completion checkpoint.',
            'Move the package to archival storage after reviewer signoff.',
        ]
    return [
        'Resolve the delivery acceptance blockers.',
        'Regenerate the delivery acceptance report.',
        'Rerun this package completion builder after acceptance reports accepted.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Package Completion',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Owner: **{report['owner']}**",
        f"Reviewer: **{report['reviewer']}**",
        f"Package completion status: **{report['package_completion_status']}**",
        '',
        '## Delivery Acceptance Source',
        '',
        f"- Path: `{report['acceptance_source']['path']}`",
        f"- Exists: `{report['acceptance_source']['exists']}`",
        f"- Loaded: `{report['acceptance_source']['loaded']}`",
        f"- Status: `{report['acceptance_source']['status']}`",
        f"- Error: `{report['acceptance_source']['error']}`",
        '',
        '## Completion Note',
        '',
        report['completion_note'],
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


def write_completion(args):
    report = build_completion(args.acceptance, args.owner, args.reviewer, args.label, args.completion_note)
    Path(args.out_json).write_text(json.dumps(report, indent=2), encoding='utf-8')
    Path(args.out_md).write_text(render_markdown(report), encoding='utf-8')
    return {'json': args.out_json, 'markdown': args.out_md, 'status': report['package_completion_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout package completion record')
    parser.add_argument('--acceptance', default=DEFAULT_ACCEPTANCE)
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--reviewer', default='Archive Reviewer')
    parser.add_argument('--label', default='archive-closeout-package-completion')
    parser.add_argument('--completion-note', default='Package completion is based on an accepted archive closeout delivery acceptance record.')
    parser.add_argument('--out-json', default='archive_closeout_package_completion.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_PACKAGE_COMPLETION.md')
    args = parser.parse_args()
    print(json.dumps(write_completion(args), indent=2))


if __name__ == '__main__':
    main()
