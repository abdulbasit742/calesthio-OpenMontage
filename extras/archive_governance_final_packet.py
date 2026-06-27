#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_FILES = [
    'archive_toolchain_audit.json',
    'ARCHIVE_TOOLCHAIN_AUDIT.md',
    'archive_portfolio_governance_packet.json',
    'ARCHIVE_PORTFOLIO_GOVERNANCE_PACKET.md',
    'archive_portfolio_governance_approval_record.json',
    'ARCHIVE_PORTFOLIO_GOVERNANCE_APPROVAL_RECORD.md',
    'archive_governance_readiness_summary.json',
    'ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md',
    'archive_governance_completion_record.json',
    'ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md',
    'ARCHIVE_GOVERNANCE_COMPLETION_CLI_GUIDE.md',
]


def file_row(path_text):
    path = Path(path_text)
    return {
        'path': path_text,
        'exists': path.exists(),
        'size_bytes': path.stat().st_size if path.exists() else 0,
        'kind': 'json' if path.suffix.lower() == '.json' else 'markdown' if path.suffix.lower() == '.md' else 'other',
    }


def read_status(path_text):
    path = Path(path_text)
    if not path.exists() or path.suffix.lower() != '.json':
        return None
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return 'invalid-json'
    if isinstance(data, dict):
        return data.get('status') or data.get('readiness_status') or data.get('approval_status')
    return None


def build_packet(packet_label='archive-governance-final-packet', files=None):
    files = files or DEFAULT_FILES
    rows = [file_row(path) for path in files]
    missing = [row for row in rows if not row['exists']]
    statuses = {path: read_status(path) for path in files if read_status(path) is not None}
    completion_status = statuses.get('archive_governance_completion_record.json')
    readiness_status = statuses.get('archive_governance_readiness_summary.json')
    packet_ready = not missing and completion_status == 'completed'

    blockers = []
    if missing:
        blockers.extend([f"Missing final packet file: {row['path']}" for row in missing])
    if readiness_status and readiness_status != 'governance-ready':
        blockers.append(f'Readiness summary status is {readiness_status}.')
    if completion_status and completion_status != 'completed':
        blockers.append(f'Completion record status is {completion_status}.')
    if completion_status is None:
        blockers.append('Completion record status is not available.')

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'packet_label': packet_label,
        'status': 'final-packet-ready' if packet_ready else 'needs-attention',
        'file_count': len(rows),
        'available_count': len(rows) - len(missing),
        'missing_count': len(missing),
        'statuses': statuses,
        'files': rows,
        'blockers': blockers,
        'next_steps': next_steps(packet_ready),
    }


def next_steps(packet_ready):
    if packet_ready:
        return ['Store the final governance packet with the archive delivery package.']
    return [
        'Resolve missing or blocked governance files.',
        'Regenerate audit, governance packet, approval record, readiness summary, completion record, and final packet.',
    ]


def render_markdown(packet):
    lines = [
        '# Archive Governance Final Packet',
        '',
        f"Generated UTC: {packet['generated_on_utc']}",
        f"Packet label: `{packet['packet_label']}`",
        f"Status: **{packet['status']}**",
        f"Files: **{packet['file_count']}**",
        f"Available: **{packet['available_count']}**",
        f"Missing: **{packet['missing_count']}**",
        '',
        '## Source Statuses',
    ]
    if packet['statuses']:
        for path, status in packet['statuses'].items():
            lines.append(f'- `{path}`: `{status}`')
    else:
        lines.append('- None available.')

    lines.extend([
        '',
        '## Files',
        '| Exists | Kind | Size | Path |',
        '| --- | --- | ---: | --- |',
    ])
    for row in packet['files']:
        lines.append(f"| {row['exists']} | {row['kind']} | {row['size_bytes']} | `{row['path']}` |")

    lines.extend(['', '## Blockers'])
    if packet['blockers']:
        for blocker in packet['blockers']:
            lines.append(f'- {blocker}')
    else:
        lines.append('- None.')

    lines.extend(['', '## Next Steps'])
    for step in packet['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_packet(label, files, out_json, out_md):
    packet = build_packet(label, files)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(packet, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(packet), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': packet['status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance packet manifest')
    parser.add_argument('--label', default='archive-governance-final-packet')
    parser.add_argument('--include', nargs='*', default=DEFAULT_FILES)
    parser.add_argument('--out-json', default='archive_governance_final_packet.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_FINAL_PACKET.md')
    args = parser.parse_args()

    result = write_packet(args.label, args.include, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
