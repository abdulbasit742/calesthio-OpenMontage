#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

PACKET_FILES = [
    'ARCHIVE_TOOLCHAIN_AUDIT.md',
    'PORTFOLIO_ARCHIVE_PLAN.md',
    'ARCHIVE_STATUS_BOARD.md',
    'ARCHIVE_BADGE_BOARD.md',
    'ARCHIVE_COMPLETION_BOARD.md',
    'ARCHIVE_PORTFOLIO_SUMMARY.md',
    'ARCHIVE_PORTFOLIO_PACKLIST.md',
    'ARCHIVE_PORTFOLIO_INDEX.md',
    'ARCHIVE_PORTFOLIO_DASHBOARD.md',
    'ARCHIVE_PORTFOLIO_DIGEST.md',
    'ARCHIVE_PORTFOLIO_SNAPSHOT.md',
    'ARCHIVE_PORTFOLIO_READINESS_REVIEW.md',
    'ARCHIVE_PORTFOLIO_RUNBOOK.md',
]

SOURCE_JSON_FILES = [
    'archive_portfolio_digest.json',
    'archive_portfolio_snapshot.json',
    'archive_portfolio_readiness_review.json',
]


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
    if not file_path.exists():
        return {'path': str(file_path), 'exists': False, 'size_bytes': 0}
    return {'path': str(file_path), 'exists': True, 'size_bytes': file_path.stat().st_size}


def source_statuses():
    rows = []
    for path in SOURCE_JSON_FILES:
        data = load_json(path)
        rows.append({
            'path': path,
            'exists': data is not None,
            'status': data.get('status', 'available') if isinstance(data, dict) else 'missing',
        })
    return rows


def build_packet(projects_root='projects', packet_label='archive-portfolio-release'):
    files = [file_row(path) for path in PACKET_FILES]
    missing_files = [row for row in files if not row['exists']]
    statuses = source_statuses()
    attention_sources = [row for row in statuses if row['status'] not in {'ready', 'complete', 'ready-for-final-review'}]
    status = 'ready-to-package' if not missing_files and not attention_sources else 'needs-attention'
    return {
        'packet_label': packet_label,
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'status': status,
        'expected_file_count': len(files),
        'available_file_count': len([row for row in files if row['exists']]),
        'missing_file_count': len(missing_files),
        'source_statuses': statuses,
        'packet_files': files,
        'next_steps': build_next_steps(missing_files, attention_sources),
    }


def build_next_steps(missing_files, attention_sources):
    steps = []
    for row in missing_files[:10]:
        steps.append(f"Generate missing release packet file: {row['path']}")
    for row in attention_sources[:10]:
        steps.append(f"Review source status for {row['path']}: {row['status']}")
    if not steps:
        steps.append('Release packet is ready to package with the final archive portfolio files.')
    return steps


def render_markdown(packet):
    lines = [
        '# Archive Portfolio Release Packet',
        '',
        f"Packet label: **{packet['packet_label']}**",
        f"Generated UTC: {packet['generated_on_utc']}",
        f"Projects root: `{packet['projects_root']}`",
        f"Status: **{packet['status']}**",
        f"Expected files: **{packet['expected_file_count']}**",
        f"Available files: **{packet['available_file_count']}**",
        f"Missing files: **{packet['missing_file_count']}**",
        '',
        '## Source Statuses',
        '| Source | Exists | Status |',
        '| --- | --- | --- |',
    ]
    for row in packet['source_statuses']:
        lines.append(f"| `{row['path']}` | {row['exists']} | {row['status']} |")
    lines.extend(['', '## Packet Files', '| File | Exists | Size bytes |', '| --- | --- | ---: |'])
    for row in packet['packet_files']:
        lines.append(f"| `{row['path']}` | {row['exists']} | {row['size_bytes']} |")
    lines.extend(['', '## Next Steps'])
    for step in packet['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_packet(projects_root, packet_label, out_json, out_md):
    packet = build_packet(projects_root=projects_root, packet_label=packet_label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(packet, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(packet), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': packet['status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive portfolio release packet manifest for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--packet-label', default='archive-portfolio-release')
    parser.add_argument('--out-json', default='archive_portfolio_release_packet.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_RELEASE_PACKET.md')
    args = parser.parse_args()

    result = write_packet(args.projects_root, args.packet_label, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
