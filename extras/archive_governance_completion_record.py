#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_READINESS = 'archive_governance_readiness_summary.json'


def read_json(path):
    target = Path(path)
    if not target.exists():
        return None, 'missing'
    try:
        return json.loads(target.read_text(encoding='utf-8')), 'loaded'
    except json.JSONDecodeError:
        return None, 'invalid-json'


def build_record(readiness_path=DEFAULT_READINESS, owner_name='', note='', label='archive-governance-completion-record'):
    readiness, load_status = read_json(readiness_path)
    readiness_status = readiness.get('status', load_status) if isinstance(readiness, dict) else load_status
    blockers = readiness.get('blockers', []) if isinstance(readiness, dict) else [f'Readiness summary is {load_status}.']
    metrics = readiness.get('metrics', {}) if isinstance(readiness, dict) else {}
    complete = readiness_status == 'governance-ready' and not blockers

    if complete:
        next_steps = ['Store this completion record with the final archive governance package.']
    else:
        next_steps = [
            'Resolve blockers from ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md.',
            'Regenerate audit, approval record, readiness summary, and this completion record.',
        ]

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'owner_name': owner_name,
        'note': note,
        'status': 'completed' if complete else 'needs-attention',
        'readiness_path': readiness_path,
        'readiness_load_status': load_status,
        'readiness_status': readiness_status,
        'metrics': metrics,
        'blockers': blockers,
        'next_steps': next_steps,
    }


def render_markdown(record):
    lines = [
        '# Archive Governance Completion Record',
        '',
        f"Generated UTC: {record['generated_on_utc']}",
        f"Label: `{record['label']}`",
        f"Status: **{record['status']}**",
        f"Owner: {record['owner_name'] or '-'}",
        f"Note: {record['note'] or '-'}",
        f"Readiness source: `{record['readiness_path']}`",
        f"Readiness load status: `{record['readiness_load_status']}`",
        f"Readiness status: `{record['readiness_status']}`",
        '',
        '## Metrics',
    ]
    if record['metrics']:
        for key, value in record['metrics'].items():
            lines.append(f'- {key}: {value}')
    else:
        lines.append('- None available.')

    lines.extend(['', '## Blockers'])
    if record['blockers']:
        for blocker in record['blockers']:
            lines.append(f'- {blocker}')
    else:
        lines.append('- None.')

    lines.extend(['', '## Next Steps'])
    for step in record['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_record(readiness_path, owner_name, note, label, out_json, out_md):
    record = build_record(readiness_path, owner_name, note, label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(record, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(record), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': record['status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance completion record from readiness summary')
    parser.add_argument('--readiness', default=DEFAULT_READINESS)
    parser.add_argument('--owner-name', default='')
    parser.add_argument('--note', default='')
    parser.add_argument('--label', default='archive-governance-completion-record')
    parser.add_argument('--out-json', default='archive_governance_completion_record.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md')
    args = parser.parse_args()

    result = write_record(args.readiness, args.owner_name, args.note, args.label, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
