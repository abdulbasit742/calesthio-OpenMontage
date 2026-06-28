#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_COMPLETION = 'archive_closeout_package_completion.json'


def load_json(path):
    source = Path(path)
    if not source.exists():
        return {'exists': False, 'loaded': False, 'data': {}, 'error': 'missing-file'}
    try:
        return {'exists': True, 'loaded': True, 'data': json.loads(source.read_text(encoding='utf-8')), 'error': None}
    except json.JSONDecodeError as exc:
        return {'exists': True, 'loaded': False, 'data': {}, 'error': f'invalid-json: {exc}'}


def build_handoff(completion, owner, reviewer, storage_owner, storage_location, label, handoff_note):
    completion_record = load_json(completion)
    completion_status = completion_record['data'].get('package_completion_status', 'missing-or-invalid') if completion_record['loaded'] else 'missing-or-invalid'
    ready = completion_status == 'complete'
    blockers = [] if ready else [f'Package completion status is {completion_status}; expected complete.']

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'reviewer': reviewer,
        'storage_owner': storage_owner,
        'storage_location': storage_location,
        'completion_source': {
            'path': completion,
            'exists': completion_record['exists'],
            'loaded': completion_record['loaded'],
            'status': completion_status,
            'error': completion_record['error'],
        },
        'storage_handoff_status': 'ready-for-storage' if ready else 'blocked',
        'handoff_note': handoff_note,
        'blockers': blockers,
        'next_steps': next_steps(ready),
    }


def next_steps(ready):
    if ready:
        return [
            'Copy the final archive package to the approved storage location.',
            'Keep this storage handoff record with the archived package.',
            'Ask the storage owner to confirm receipt after transfer.',
        ]
    return [
        'Resolve package completion blockers.',
        'Regenerate the package completion report.',
        'Rerun this storage handoff builder after package completion reports complete.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Storage Handoff',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Owner: **{report['owner']}**",
        f"Reviewer: **{report['reviewer']}**",
        f"Storage Owner: **{report['storage_owner']}**",
        f"Storage Location: **{report['storage_location']}**",
        f"Storage handoff status: **{report['storage_handoff_status']}**",
        '',
        '## Package Completion Source',
        '',
        f"- Path: `{report['completion_source']['path']}`",
        f"- Exists: `{report['completion_source']['exists']}`",
        f"- Loaded: `{report['completion_source']['loaded']}`",
        f"- Status: `{report['completion_source']['status']}`",
        f"- Error: `{report['completion_source']['error']}`",
        '',
        '## Handoff Note',
        '',
        report['handoff_note'],
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


def write_handoff(args):
    report = build_handoff(
        args.completion,
        args.owner,
        args.reviewer,
        args.storage_owner,
        args.storage_location,
        args.label,
        args.handoff_note,
    )
    Path(args.out_json).write_text(json.dumps(report, indent=2), encoding='utf-8')
    Path(args.out_md).write_text(render_markdown(report), encoding='utf-8')
    return {'json': args.out_json, 'markdown': args.out_md, 'status': report['storage_handoff_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout storage handoff record')
    parser.add_argument('--completion', default=DEFAULT_COMPLETION)
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--reviewer', default='Archive Reviewer')
    parser.add_argument('--storage-owner', default='Storage Owner')
    parser.add_argument('--storage-location', default='Approved Archive Storage')
    parser.add_argument('--label', default='archive-closeout-storage-handoff')
    parser.add_argument('--handoff-note', default='Storage handoff is based on a complete archive closeout package completion record.')
    parser.add_argument('--out-json', default='archive_closeout_storage_handoff.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_STORAGE_HANDOFF.md')
    args = parser.parse_args()
    print(json.dumps(write_handoff(args), indent=2))


if __name__ == '__main__':
    main()
