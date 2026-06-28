#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_CHECKLIST = 'archive_closeout_handoff_checklist.json'


def load_checklist(path):
    source = Path(path)
    if not source.exists():
        return {'loaded': False, 'error': 'missing-file', 'data': {}}
    try:
        return {'loaded': True, 'error': None, 'data': json.loads(source.read_text(encoding='utf-8'))}
    except json.JSONDecodeError as exc:
        return {'loaded': False, 'error': f'invalid-json: {exc}', 'data': {}}


def build_acknowledgement(checklist_path, owner, reviewer, decision, label, note):
    checklist = load_checklist(checklist_path)
    checklist_status = checklist['data'].get('checklist_status', 'missing-or-invalid') if checklist['loaded'] else 'missing-or-invalid'

    blockers = []
    if checklist_status != 'ready':
        blockers.append(f'Handoff checklist status is {checklist_status}; expected ready.')
    if decision != 'acknowledge':
        blockers.append(f'Owner decision is {decision}; expected acknowledge.')

    acknowledgement_status = 'acknowledged' if not blockers else 'blocked'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'reviewer': reviewer,
        'decision': decision,
        'acknowledgement_status': acknowledgement_status,
        'checklist_source': {
            'path': checklist_path,
            'loaded': checklist['loaded'],
            'error': checklist['error'],
            'status': checklist_status,
        },
        'blockers': blockers,
        'note': note,
        'next_steps': next_steps(blockers),
    }


def next_steps(blockers):
    if not blockers:
        return [
            'Store this acknowledgement with the final archive package.',
            'Keep the handoff checklist and readiness reports with the same delivery bundle.',
            'Mark archive closeout delivery as owner acknowledged.',
        ]
    return [
        'Resolve the blockers listed in this acknowledgement.',
        'Regenerate the handoff checklist until it reports ready.',
        'Rerun this owner acknowledgement builder with decision acknowledge.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Owner Acknowledgement',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Owner: **{report['owner']}**",
        f"Reviewer: **{report['reviewer']}**",
        f"Decision: **{report['decision']}**",
        f"Acknowledgement status: **{report['acknowledgement_status']}**",
        '',
        '## Handoff Checklist Source',
        '',
        f"- Path: `{report['checklist_source']['path']}`",
        f"- Loaded: `{report['checklist_source']['loaded']}`",
        f"- Status: `{report['checklist_source']['status']}`",
        f"- Error: `{report['checklist_source']['error']}`",
        '',
        '## Blockers',
    ]
    if report['blockers']:
        for blocker in report['blockers']:
            lines.append(f'- {blocker}')
    else:
        lines.append('- None')
    lines.extend(['', '## Owner Note', '', report['note'] or 'No additional note recorded.', '', '## Next Steps'])
    for step in report['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_acknowledgement(args):
    report = build_acknowledgement(args.checklist, args.owner, args.reviewer, args.decision, args.label, args.note)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.write_text(json.dumps(report, indent=2), encoding='utf-8')
    out_md.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(out_json), 'markdown': str(out_md), 'status': report['acknowledgement_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout owner acknowledgement')
    parser.add_argument('--checklist', default=DEFAULT_CHECKLIST)
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--reviewer', default='Archive Reviewer')
    parser.add_argument('--decision', choices=['acknowledge', 'hold'], default='acknowledge')
    parser.add_argument('--label', default='archive-closeout-owner-acknowledgement')
    parser.add_argument('--note', default='Final archive closeout package reviewed and acknowledged by the archive owner.')
    parser.add_argument('--out-json', default='archive_closeout_owner_acknowledgement.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_OWNER_ACKNOWLEDGEMENT.md')
    args = parser.parse_args()
    print(json.dumps(write_acknowledgement(args), indent=2))


if __name__ == '__main__':
    main()
