#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_READINESS = 'archive_closeout_package_readiness.json'

CHECKLIST_ITEMS = [
    {
        'id': 'readiness-json',
        'label': 'Package readiness JSON is generated',
        'required_file': 'archive_closeout_package_readiness.json',
    },
    {
        'id': 'readiness-md',
        'label': 'Package readiness Markdown is generated',
        'required_file': 'ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md',
    },
    {
        'id': 'milestone-manifest-json',
        'label': 'Milestone manifest JSON is generated',
        'required_file': 'archive_closeout_milestone_manifest.json',
    },
    {
        'id': 'milestone-manifest-md',
        'label': 'Milestone manifest Markdown is generated',
        'required_file': 'ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md',
    },
    {
        'id': 'rollup-md',
        'label': 'Archive closeout rollup Markdown is generated',
        'required_file': 'ARCHIVE_CLOSEOUT_ROLLUP.md',
    },
    {
        'id': 'review-gate-md',
        'label': 'Archive closeout review gate Markdown is generated',
        'required_file': 'ARCHIVE_CLOSEOUT_REVIEW_GATE.md',
    },
]


def load_readiness(path):
    source = Path(path)
    if not source.exists():
        return {'loaded': False, 'error': 'missing-file', 'data': {}}
    try:
        return {'loaded': True, 'error': None, 'data': json.loads(source.read_text(encoding='utf-8'))}
    except json.JSONDecodeError as exc:
        return {'loaded': False, 'error': f'invalid-json: {exc}', 'data': {}}


def file_state(path):
    target = Path(path)
    return {'path': str(target), 'exists': target.exists(), 'size_bytes': target.stat().st_size if target.exists() else 0}


def build_checklist(readiness_path, label, owner):
    readiness = load_readiness(readiness_path)
    readiness_status = readiness['data'].get('readiness_status', 'missing-or-invalid') if readiness['loaded'] else 'missing-or-invalid'

    items = []
    for item in CHECKLIST_ITEMS:
        state = file_state(item['required_file'])
        items.append({**item, **state, 'status': 'done' if state['exists'] else 'missing'})

    missing = [item for item in items if item['status'] != 'done']
    if readiness_status != 'ready-for-handoff':
        missing.append({
            'id': 'readiness-status',
            'label': f'Readiness status is {readiness_status}; expected ready-for-handoff',
            'required_file': readiness_path,
            'path': readiness_path,
            'exists': readiness['loaded'],
            'size_bytes': 0,
            'status': 'blocked',
        })

    checklist_status = 'ready' if not missing else 'blocked'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'checklist_status': checklist_status,
        'readiness_source': {'path': readiness_path, 'loaded': readiness['loaded'], 'error': readiness['error'], 'status': readiness_status},
        'items': items,
        'missing_or_blocked': missing,
        'next_steps': next_steps(missing),
    }


def next_steps(missing):
    if not missing:
        return [
            'Attach all listed Markdown reports to the final archive package.',
            'Keep JSON outputs as the machine-readable handoff record.',
            'Record final owner acknowledgement after package delivery.',
        ]
    return [
        'Generate or add the missing files listed in this checklist.',
        'Regenerate package readiness until it reports ready-for-handoff.',
        'Rerun this handoff checklist builder before final delivery.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Handoff Checklist',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Owner: **{report['owner']}**",
        f"Checklist status: **{report['checklist_status']}**",
        '',
        '## Readiness Source',
        '',
        f"- Path: `{report['readiness_source']['path']}`",
        f"- Loaded: `{report['readiness_source']['loaded']}`",
        f"- Status: `{report['readiness_source']['status']}`",
        f"- Error: `{report['readiness_source']['error']}`",
        '',
        '## Checklist Items',
        '',
        '| ID | Label | File | Exists | Size | Status |',
        '|---|---|---|---:|---:|---|',
    ]
    for item in report['items']:
        lines.append(f"| {item['id']} | {item['label']} | `{item['path']}` | {item['exists']} | {item['size_bytes']} | {item['status']} |")
    lines.extend(['', '## Missing Or Blocked'])
    if report['missing_or_blocked']:
        for item in report['missing_or_blocked']:
            lines.append(f"- {item['id']}: {item['label']}")
    else:
        lines.append('- None')
    lines.extend(['', '## Next Steps'])
    for step in report['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_checklist(args):
    report = build_checklist(args.readiness, args.label, args.owner)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.write_text(json.dumps(report, indent=2), encoding='utf-8')
    out_md.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(out_json), 'markdown': str(out_md), 'status': report['checklist_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout final handoff checklist')
    parser.add_argument('--readiness', default=DEFAULT_READINESS)
    parser.add_argument('--label', default='archive-closeout-handoff-checklist')
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--out-json', default='archive_closeout_handoff_checklist.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_HANDOFF_CHECKLIST.md')
    args = parser.parse_args()
    print(json.dumps(write_checklist(args), indent=2))


if __name__ == '__main__':
    main()
