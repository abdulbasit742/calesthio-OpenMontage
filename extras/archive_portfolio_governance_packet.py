#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_FILES = [
    'ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY.md',
    'archive_portfolio_governance_summary.json',
    'ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER.md',
    'archive_portfolio_governance_action_tracker.json',
    'ARCHIVE_PORTFOLIO_GOVERNANCE_BOARD.md',
    'archive_portfolio_governance_board.json',
    'docs/ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY_GUIDE.md',
    'docs/ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER_GUIDE.md',
    'docs/ARCHIVE_PORTFOLIO_GOVERNANCE_BOARD_GUIDE.md',
]

READY_STATUSES = {
    'governance-ready',
    'actions-ready',
    'governance-board-ready',
    'ready',
    'complete',
}


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json'}


def file_row(path):
    file_path = Path(path)
    return {
        'path': path,
        'exists': file_path.exists(),
        'size_bytes': file_path.stat().st_size if file_path.exists() else 0,
    }


def source_status(path):
    data = load_json(path)
    return {
        'path': path,
        'exists': data is not None,
        'status': data.get('status', 'missing') if isinstance(data, dict) else 'missing',
    }


def build_packet(packet_label='archive-portfolio-governance-packet'):
    file_rows = [file_row(path) for path in EXPECTED_FILES]
    missing_files = [row['path'] for row in file_rows if not row['exists']]
    sources = [
        source_status('archive_portfolio_governance_summary.json'),
        source_status('archive_portfolio_governance_action_tracker.json'),
        source_status('archive_portfolio_governance_board.json'),
    ]
    attention_sources = [row for row in sources if row['status'] not in READY_STATUSES]
    status = 'governance-packet-ready' if not missing_files and not attention_sources else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'packet_label': packet_label,
        'status': status,
        'expected_file_count': len(file_rows),
        'available_file_count': len(file_rows) - len(missing_files),
        'missing_file_count': len(missing_files),
        'missing_files': missing_files,
        'source_statuses': sources,
        'attention_source_count': len(attention_sources),
        'attention_sources': attention_sources,
        'files': file_rows,
    }


def render_markdown(packet):
    lines = [
        '# Archive Portfolio Governance Packet',
        '',
        f"Generated UTC: {packet['generated_on_utc']}",
        f"Packet label: `{packet['packet_label']}`",
        f"Status: **{packet['status']}**",
        '',
        '## Counts',
        f"- Expected files: {packet['expected_file_count']}",
        f"- Available files: {packet['available_file_count']}",
        f"- Missing files: {packet['missing_file_count']}",
        f"- Attention sources: {packet['attention_source_count']}",
        '',
        '## Source Statuses',
        '| Path | Exists | Status |',
        '| --- | --- | --- |',
    ]
    for source in packet['source_statuses']:
        lines.append(f"| {source['path']} | {source['exists']} | {source['status']} |")
    lines.extend(['', '## Files', '| Path | Exists | Size bytes |', '| --- | --- | --- |'])
    for row in packet['files']:
        lines.append(f"| {row['path']} | {row['exists']} | {row['size_bytes']} |")
    lines.extend(['', '## Missing Files'])
    if packet['missing_files']:
        for path in packet['missing_files']:
            lines.append(f'- `{path}`')
    else:
        lines.append('- None')
    lines.append('')
    return '\n'.join(lines)


def write_packet(packet_label, out_json, out_md):
    packet = build_packet(packet_label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(packet, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(packet), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': packet['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio governance packet manifest for OpenMontage Plus')
    parser.add_argument('--packet-label', default='archive-portfolio-governance-packet')
    parser.add_argument('--out-json', default='archive_portfolio_governance_packet.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_GOVERNANCE_PACKET.md')
    args = parser.parse_args()

    result = write_packet(args.packet_label, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
