#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_ITEMS = [
    {'key': 'final_packet', 'path': 'archive_governance_final_packet.json', 'required': True},
    {'key': 'final_handoff_note', 'path': 'archive_governance_final_handoff_note.json', 'required': True},
    {'key': 'final_delivery_checklist', 'path': 'archive_governance_final_delivery_checklist.json', 'required': True},
    {'key': 'final_delivery_receipt', 'path': 'archive_governance_final_delivery_receipt.json', 'required': True},
    {'key': 'final_delivery_acknowledgement', 'path': 'archive_governance_final_delivery_acknowledgement.json', 'required': True},
    {'key': 'final_closure_certificate', 'path': 'archive_governance_final_closure_certificate.json', 'required': True},
    {'key': 'final_closeout_certificate_md', 'path': 'ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md', 'required': True},
]


def inspect_item(item):
    path = Path(item['path'])
    result = {
        'key': item['key'],
        'path': item['path'],
        'required': item.get('required', True),
        'exists': path.exists(),
        'size_bytes': path.stat().st_size if path.exists() else 0,
    }
    if path.suffix.lower() == '.json' and path.exists():
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            result['json_status'] = 'loaded' if isinstance(data, dict) else 'non-object-json'
            if isinstance(data, dict):
                for field in ['status', 'receipt_status', 'acknowledgement_status', 'closure_status', 'package_id', 'certificate_id']:
                    if field in data:
                        result[field] = data[field]
        except json.JSONDecodeError:
            result['json_status'] = 'invalid-json'
    return result


def build_index(label, owner, items):
    inspected = [inspect_item(item) for item in items]
    missing_required = [row['path'] for row in inspected if row['required'] and not row['exists']]
    invalid_json = [row['path'] for row in inspected if row.get('json_status') == 'invalid-json']
    closure_rows = [row for row in inspected if row.get('closure_status')]
    closure_closed = any(row.get('closure_status') == 'closed' for row in closure_rows)
    index_status = 'closeout-ready' if not missing_required and not invalid_json and closure_closed else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner': owner,
        'index_status': index_status,
        'missing_required': missing_required,
        'invalid_json': invalid_json,
        'closure_closed': closure_closed,
        'items': inspected,
        'next_steps': next_steps(index_status, missing_required, invalid_json, closure_closed),
    }


def next_steps(status, missing_required, invalid_json, closure_closed):
    if status == 'closeout-ready':
        return [
            'Store this closeout index with the final archive package.',
            'Use it as the package table of contents for reviewer handoff and future audits.',
        ]
    steps = []
    if missing_required:
        steps.append('Add missing required files to the final archive package.')
    if invalid_json:
        steps.append('Regenerate invalid JSON files before closing the package.')
    if not closure_closed:
        steps.append('Generate a final closure certificate with closure_status closed.')
    return steps or ['Review closeout index inputs and rerun the builder.']


def render_markdown(index):
    lines = [
        '# Archive Governance Final Closeout Index',
        '',
        f"Generated UTC: {index['generated_on_utc']}",
        f"Label: **{index['label']}**",
        f"Owner: **{index['owner']}**",
        f"Index status: **{index['index_status']}**",
        f"Closure closed: **{index['closure_closed']}**",
        '',
        '## Files',
        '',
        '| Key | Path | Required | Exists | Size bytes | Status |',
        '| --- | --- | --- | --- | ---: | --- |',
    ]
    for item in index['items']:
        status = item.get('closure_status') or item.get('acknowledgement_status') or item.get('receipt_status') or item.get('status') or item.get('json_status', '-')
        lines.append(f"| {item['key']} | `{item['path']}` | {item['required']} | {item['exists']} | {item['size_bytes']} | {status} |")
    lines.extend(['', '## Missing Required Files'])
    if index['missing_required']:
        for path in index['missing_required']:
            lines.append(f'- `{path}`')
    else:
        lines.append('- None')
    lines.extend(['', '## Invalid JSON Files'])
    if index['invalid_json']:
        for path in index['invalid_json']:
            lines.append(f'- `{path}`')
    else:
        lines.append('- None')
    lines.extend(['', '## Next Steps'])
    for step in index['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_index(label, owner, out_json, out_md):
    index = build_index(label, owner, DEFAULT_ITEMS)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(index, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(index), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': index['index_status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance closeout index')
    parser.add_argument('--label', default='archive-governance-final-closeout')
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--out-json', default='archive_governance_final_closeout_index.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md')
    args = parser.parse_args()

    result = write_index(args.label, args.owner, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
