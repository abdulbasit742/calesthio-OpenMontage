#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_ACKNOWLEDGEMENT = 'archive_closeout_owner_acknowledgement.json'


def load_acknowledgement(path):
    source = Path(path)
    if not source.exists():
        return {'loaded': False, 'error': 'missing-file', 'data': {}}
    try:
        return {'loaded': True, 'error': None, 'data': json.loads(source.read_text(encoding='utf-8'))}
    except json.JSONDecodeError as exc:
        return {'loaded': False, 'error': f'invalid-json: {exc}', 'data': {}}


def build_delivery_seal(acknowledgement_path, label, owner, reviewer, release_tag, note):
    acknowledgement = load_acknowledgement(acknowledgement_path)
    acknowledgement_status = acknowledgement['data'].get('acknowledgement_status', 'missing-or-invalid') if acknowledgement['loaded'] else 'missing-or-invalid'

    blockers = []
    if acknowledgement_status != 'acknowledged':
        blockers.append(f'Owner acknowledgement status is {acknowledgement_status}; expected acknowledged.')

    seal_status = 'sealed' if not blockers else 'blocked'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'reviewer': reviewer,
        'release_tag': release_tag,
        'delivery_seal_status': seal_status,
        'acknowledgement_source': {
            'path': acknowledgement_path,
            'loaded': acknowledgement['loaded'],
            'error': acknowledgement['error'],
            'status': acknowledgement_status,
        },
        'blockers': blockers,
        'note': note,
        'next_steps': next_steps(blockers),
    }


def next_steps(blockers):
    if not blockers:
        return [
            'Store the delivery seal with the final archive package.',
            'Keep acknowledgement, checklist, readiness, manifest, review gate, and rollup records together.',
            'Treat the archive closeout workflow as sealed for delivery.',
        ]
    return [
        'Resolve the blockers listed in this delivery seal.',
        'Regenerate owner acknowledgement until it reports acknowledged.',
        'Rerun this delivery seal builder after acknowledgement is complete.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Final Delivery Seal',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Owner: **{report['owner']}**",
        f"Reviewer: **{report['reviewer']}**",
        f"Release tag: **{report['release_tag']}**",
        f"Delivery seal status: **{report['delivery_seal_status']}**",
        '',
        '## Owner Acknowledgement Source',
        '',
        f"- Path: `{report['acknowledgement_source']['path']}`",
        f"- Loaded: `{report['acknowledgement_source']['loaded']}`",
        f"- Status: `{report['acknowledgement_source']['status']}`",
        f"- Error: `{report['acknowledgement_source']['error']}`",
        '',
        '## Blockers',
    ]
    if report['blockers']:
        for blocker in report['blockers']:
            lines.append(f'- {blocker}')
    else:
        lines.append('- None')
    lines.extend(['', '## Seal Note', '', report['note'] or 'No additional note recorded.', '', '## Next Steps'])
    for step in report['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_delivery_seal(args):
    report = build_delivery_seal(args.acknowledgement, args.label, args.owner, args.reviewer, args.release_tag, args.note)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.write_text(json.dumps(report, indent=2), encoding='utf-8')
    out_md.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(out_json), 'markdown': str(out_md), 'status': report['delivery_seal_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout final delivery seal')
    parser.add_argument('--acknowledgement', default=DEFAULT_ACKNOWLEDGEMENT)
    parser.add_argument('--label', default='archive-closeout-final-delivery-seal')
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--reviewer', default='Archive Reviewer')
    parser.add_argument('--release-tag', default='archive-closeout-delivery')
    parser.add_argument('--note', default='Final archive closeout delivery is sealed after owner acknowledgement.')
    parser.add_argument('--out-json', default='archive_closeout_delivery_seal.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md')
    args = parser.parse_args()
    print(json.dumps(write_delivery_seal(args), indent=2))


if __name__ == '__main__':
    main()
