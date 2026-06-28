#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_RECORDS = [
    ('rollup', 'archive_closeout_rollup.json', 'ARCHIVE_CLOSEOUT_ROLLUP.md'),
    ('review_gate', 'archive_closeout_review_gate.json', 'ARCHIVE_CLOSEOUT_REVIEW_GATE.md'),
    ('manifest', 'archive_closeout_milestone_manifest.json', 'ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md'),
    ('package_readiness', 'archive_closeout_package_readiness.json', 'ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md'),
    ('handoff_checklist', 'archive_closeout_handoff_checklist.json', 'ARCHIVE_CLOSEOUT_HANDOFF_CHECKLIST.md'),
    ('owner_acknowledgement', 'archive_closeout_owner_acknowledgement.json', 'ARCHIVE_CLOSEOUT_OWNER_ACKNOWLEDGEMENT.md'),
    ('delivery_seal', 'archive_closeout_delivery_seal.json', 'ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md'),
]

STATUS_KEYS = [
    'status',
    'rollup_status',
    'review_gate_status',
    'manifest_status',
    'readiness_status',
    'checklist_status',
    'acknowledgement_status',
    'delivery_seal_status',
]


def load_json_status(path):
    source = Path(path)
    if not source.exists():
        return {'exists': False, 'loaded': False, 'status': 'missing', 'error': 'missing-file'}
    try:
        data = json.loads(source.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        return {'exists': True, 'loaded': False, 'status': 'invalid-json', 'error': str(exc)}
    status = 'present'
    for key in STATUS_KEYS:
        if key in data:
            status = data[key]
            break
    return {'exists': True, 'loaded': True, 'status': status, 'error': None}


def file_state(path):
    source = Path(path)
    return {'path': path, 'exists': source.exists()}


def build_index(label, owner, records):
    entries = []
    for name, json_path, md_path in records:
        json_state = load_json_status(json_path)
        md_state = file_state(md_path)
        entries.append({
            'name': name,
            'json': {'path': json_path, **json_state},
            'markdown': md_state,
            'covered': json_state['exists'] and md_state['exists'],
        })
    missing = [entry['name'] for entry in entries if not entry['covered']]
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'index_status': 'complete' if not missing else 'incomplete',
        'missing_records': missing,
        'records': entries,
    }


def render_markdown(report):
    lines = [
        '# Archive Closeout Delivery Index',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Owner: **{report['owner']}**",
        f"Index status: **{report['index_status']}**",
        '',
        '## Records',
        '',
        '| Record | JSON | JSON status | Markdown | Covered |',
        '|---|---|---|---|---|',
    ]
    for entry in report['records']:
        lines.append(
            f"| {entry['name']} | `{entry['json']['path']}` | `{entry['json']['status']}` | "
            f"`{entry['markdown']['path']}` | `{entry['covered']}` |"
        )
    lines.extend(['', '## Missing Records'])
    if report['missing_records']:
        for item in report['missing_records']:
            lines.append(f'- {item}')
    else:
        lines.append('- None')
    lines.extend([
        '',
        '## Next Steps',
        '',
        '- If status is `complete`, store this index with the final delivery package.',
        '- If status is `incomplete`, regenerate the missing JSON or Markdown records and rerun this builder.',
        '',
    ])
    return '\n'.join(lines)


def parse_record(value):
    parts = value.split(':')
    if len(parts) != 3:
        raise argparse.ArgumentTypeError('record must use name:json_path:markdown_path')
    return tuple(parts)


def write_index(args):
    records = args.record if args.record else DEFAULT_RECORDS
    report = build_index(args.label, args.owner, records)
    Path(args.out_json).write_text(json.dumps(report, indent=2), encoding='utf-8')
    Path(args.out_md).write_text(render_markdown(report), encoding='utf-8')
    return {'json': args.out_json, 'markdown': args.out_md, 'status': report['index_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout delivery index')
    parser.add_argument('--label', default='archive-closeout-delivery-index')
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--record', action='append', type=parse_record, help='name:json_path:markdown_path')
    parser.add_argument('--out-json', default='archive_closeout_delivery_index.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md')
    args = parser.parse_args()
    print(json.dumps(write_index(args), indent=2))


if __name__ == '__main__':
    main()
