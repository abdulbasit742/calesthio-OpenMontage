#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_FILES = [
    {'key': 'delivery_manifest', 'path': 'extras/delivery_manifest_builder.py', 'category': 'script'},
    {'key': 'handoff_checklist', 'path': 'extras/delivery_handoff_checklist.py', 'category': 'script'},
    {'key': 'client_email', 'path': 'extras/client_delivery_email_builder.py', 'category': 'script'},
    {'key': 'client_feedback_tracker', 'path': 'extras/client_feedback_tracker.py', 'category': 'script'},
    {'key': 'client_feedback_report', 'path': 'extras/client_feedback_report.py', 'category': 'script'},
    {'key': 'project_closeout', 'path': 'extras/project_closeout_builder.py', 'category': 'script'},
    {'key': 'closeout_ops', 'path': 'extras/closeout_ops_runner.py', 'category': 'script'},
    {'key': 'archive_manifest', 'path': 'extras/project_archive_manifest.py', 'category': 'script'},
    {'key': 'archive_ops', 'path': 'extras/archive_ops_runner.py', 'category': 'script'},
    {'key': 'archive_status_board', 'path': 'extras/archive_status_board.py', 'category': 'script'},
    {'key': 'portfolio_archive_plan', 'path': 'extras/portfolio_archive_plan.py', 'category': 'script'},
    {'key': 'archive_toolchain_cli', 'path': 'extras/archive_toolchain_cli.py', 'category': 'script'},
    {'key': 'archive_toolchain_guide', 'path': 'docs/ARCHIVE_TOOLCHAIN_GUIDE.md', 'category': 'docs'},
    {'key': 'portfolio_runbook', 'path': 'extras/archive_portfolio_runbook.py', 'category': 'script'},
    {'key': 'portfolio_operations_guide', 'path': 'docs/ARCHIVE_PORTFOLIO_OPERATIONS.md', 'category': 'docs'},
    {'key': 'governance_summary', 'path': 'extras/archive_portfolio_governance_summary.py', 'category': 'script'},
    {'key': 'governance_summary_guide', 'path': 'docs/ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY_GUIDE.md', 'category': 'docs'},
    {'key': 'governance_action_tracker', 'path': 'extras/archive_portfolio_governance_action_tracker.py', 'category': 'script'},
    {'key': 'governance_action_tracker_guide', 'path': 'docs/ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER_GUIDE.md', 'category': 'docs'},
    {'key': 'governance_board', 'path': 'extras/archive_portfolio_governance_board.py', 'category': 'script'},
    {'key': 'governance_board_guide', 'path': 'docs/ARCHIVE_PORTFOLIO_GOVERNANCE_BOARD_GUIDE.md', 'category': 'docs'},
    {'key': 'governance_packet', 'path': 'extras/archive_portfolio_governance_packet.py', 'category': 'script'},
    {'key': 'governance_packet_guide', 'path': 'docs/ARCHIVE_PORTFOLIO_GOVERNANCE_PACKET_GUIDE.md', 'category': 'docs'},
    {'key': 'governance_approval_record', 'path': 'extras/archive_portfolio_governance_approval_record.py', 'category': 'script'},
    {'key': 'governance_approval_record_guide', 'path': 'docs/ARCHIVE_PORTFOLIO_GOVERNANCE_APPROVAL_RECORD_GUIDE.md', 'category': 'docs'},
    {'key': 'governance_audit_guide', 'path': 'docs/ARCHIVE_TOOLCHAIN_GOVERNANCE_AUDIT_GUIDE.md', 'category': 'docs'},
    {'key': 'governance_readiness_summary', 'path': 'extras/archive_governance_readiness_summary.py', 'category': 'script'},
    {'key': 'governance_readiness_summary_guide', 'path': 'docs/ARCHIVE_GOVERNANCE_READINESS_SUMMARY_GUIDE.md', 'category': 'docs'},
    {'key': 'governance_readiness_cli', 'path': 'extras/archive_governance_readiness_cli.py', 'category': 'script'},
    {'key': 'governance_readiness_runbook_appendix', 'path': 'extras/archive_governance_readiness_runbook_appendix.py', 'category': 'script'},
    {'key': 'governance_readiness_runbook_appendix_guide', 'path': 'docs/ARCHIVE_GOVERNANCE_READINESS_RUNBOOK_APPENDIX_GUIDE.md', 'category': 'docs'},
]

KEYWORDS = [
    'delivery',
    'handoff',
    'feedback',
    'closeout',
    'archive',
    'portfolio',
    'governance',
    'packet',
    'approval',
    'readiness',
    'appendix',
]


def read_text(path):
    if not path.exists():
        return ''
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return ''


def file_row(item):
    path = Path(item['path'])
    text = read_text(path)
    lower_text = text.lower()
    keyword_hits = [keyword for keyword in KEYWORDS if keyword in lower_text]
    return {
        'key': item['key'],
        'category': item['category'],
        'path': item['path'],
        'exists': path.exists(),
        'size_bytes': path.stat().st_size if path.exists() else 0,
        'keyword_hits': keyword_hits,
        'missing_keywords': [keyword for keyword in KEYWORDS if keyword not in lower_text],
    }


def build_audit():
    rows = [file_row(item) for item in EXPECTED_FILES]
    missing = [row for row in rows if not row['exists']]
    docs = [row for row in rows if row['category'] == 'docs']
    scripts = [row for row in rows if row['category'] == 'script']
    governance_rows = [row for row in rows if 'governance' in row['key']]
    governance_missing = [row for row in governance_rows if not row['exists']]
    status = 'passed' if not missing else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': status,
        'expected_count': len(rows),
        'script_count': len(scripts),
        'docs_count': len(docs),
        'governance_count': len(governance_rows),
        'governance_missing_count': len(governance_missing),
        'missing_count': len(missing),
        'available_count': len(rows) - len(missing),
        'rows': rows,
        'recommendations': recommendations(missing, governance_missing),
    }


def recommendations(missing, governance_missing):
    if missing:
        return [f"Create or restore missing file: {row['path']}" for row in missing]
    notes = [
        'Archive toolchain files are present.',
        'Governance scripts, guides, packet, approval record, readiness summary, CLI, and appendix coverage are present.',
        'Run archive_governance_readiness_cli.py show to inspect the readiness summary companion command.',
        'Run archive_governance_readiness_runbook_appendix.py after the governance approval record.',
        'Run archive_portfolio_runbook.py to generate the full archive governance workflow.',
    ]
    if governance_missing:
        notes.append('Regenerate the governance coverage files before final archive delivery.')
    return notes


def render_markdown(audit):
    lines = [
        '# Archive Toolchain Audit',
        '',
        f"Generated UTC: {audit['generated_on_utc']}",
        f"Status: **{audit['status']}**",
        f"Expected files: **{audit['expected_count']}**",
        f"Available files: **{audit['available_count']}**",
        f"Missing files: **{audit['missing_count']}**",
        f"Scripts: **{audit['script_count']}**",
        f"Docs: **{audit['docs_count']}**",
        f"Governance files: **{audit['governance_count']}**",
        f"Governance missing: **{audit['governance_missing_count']}**",
        '',
        '## Files',
        '| Key | Category | Exists | Size | Keyword Hits | Path |',
        '| --- | --- | --- | ---: | --- | --- |',
    ]
    for row in audit['rows']:
        hits = ', '.join(row['keyword_hits']) or '-'
        lines.append(f"| {row['key']} | {row['category']} | {row['exists']} | {row['size_bytes']} | {hits} | `{row['path']}` |")
    lines.extend(['', '## Recommendations'])
    for item in audit['recommendations']:
        lines.append(f'- {item}')
    lines.append('')
    return '\n'.join(lines)


def write_audit(out_json, out_md):
    audit = build_audit()
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(audit, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(audit), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': audit['status']}


def main():
    parser = argparse.ArgumentParser(description='Audit the OpenMontage Plus archive toolchain files and governance coverage')
    parser.add_argument('--out-json', default='archive_toolchain_audit.json')
    parser.add_argument('--out-md', default='ARCHIVE_TOOLCHAIN_AUDIT.md')
    args = parser.parse_args()

    result = write_audit(args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
