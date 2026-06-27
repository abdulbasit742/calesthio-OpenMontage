#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_AUDIT = 'archive_toolchain_audit.json'
DEFAULT_APPROVAL = 'archive_portfolio_governance_approval_record.json'


def read_json(path):
    target = Path(path)
    if not target.exists():
        return None, 'missing'
    try:
        return json.loads(target.read_text(encoding='utf-8')), 'loaded'
    except json.JSONDecodeError:
        return None, 'invalid-json'


def source_row(label, path, data, load_status):
    status = data.get('status', load_status) if isinstance(data, dict) else load_status
    return {
        'label': label,
        'path': path,
        'load_status': load_status,
        'status': status,
        'exists': load_status != 'missing',
    }


def build_summary(audit_path=DEFAULT_AUDIT, approval_path=DEFAULT_APPROVAL):
    audit, audit_load_status = read_json(audit_path)
    approval, approval_load_status = read_json(approval_path)
    audit_status = audit.get('status', audit_load_status) if isinstance(audit, dict) else audit_load_status
    approval_status = approval.get('status', approval_load_status) if isinstance(approval, dict) else approval_load_status

    missing_count = audit.get('missing_count', None) if isinstance(audit, dict) else None
    governance_missing_count = audit.get('governance_missing_count', None) if isinstance(audit, dict) else None
    expected_count = audit.get('expected_count', None) if isinstance(audit, dict) else None
    available_count = audit.get('available_count', None) if isinstance(audit, dict) else None
    packet_status = approval.get('packet_status', 'missing') if isinstance(approval, dict) else 'missing'
    approved = bool(approval.get('approved', False)) if isinstance(approval, dict) else False
    attention_source_count = approval.get('attention_source_count', None) if isinstance(approval, dict) else None
    approval_missing_count = approval.get('missing_file_count', None) if isinstance(approval, dict) else None

    blockers = []
    if audit_status != 'passed':
        blockers.append(f'Audit status is {audit_status}, expected passed.')
    if governance_missing_count not in (0, None):
        blockers.append(f'Governance missing count is {governance_missing_count}.')
    if missing_count not in (0, None):
        blockers.append(f'Audit missing file count is {missing_count}.')
    if approval_status != 'approved':
        blockers.append(f'Approval record status is {approval_status}, expected approved.')
    if packet_status != 'governance-packet-ready':
        blockers.append(f'Governance packet status is {packet_status}.')
    if attention_source_count not in (0, None):
        blockers.append(f'Attention source count is {attention_source_count}.')
    if approval_missing_count not in (0, None):
        blockers.append(f'Approval record missing file count is {approval_missing_count}.')

    ready = audit_status == 'passed' and approval_status == 'approved' and not blockers
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'governance-ready' if ready else 'needs-attention',
        'audit_path': audit_path,
        'approval_path': approval_path,
        'sources': [
            source_row('toolchain-audit', audit_path, audit, audit_load_status),
            source_row('governance-approval-record', approval_path, approval, approval_load_status),
        ],
        'metrics': {
            'expected_count': expected_count,
            'available_count': available_count,
            'missing_count': missing_count,
            'governance_missing_count': governance_missing_count,
            'packet_status': packet_status,
            'approved': approved,
            'attention_source_count': attention_source_count,
            'approval_missing_count': approval_missing_count,
        },
        'blockers': blockers,
        'next_steps': [] if ready else [
            'Run archive_toolchain_audit.py and fix any missing files.',
            'Run the governance packet and approval record tools after blockers are fixed.',
            'Regenerate this readiness summary after approval status is approved.',
        ],
    }


def render_markdown(summary):
    lines = [
        '# Archive Governance Readiness Summary',
        '',
        f"Generated UTC: {summary['generated_on_utc']}",
        f"Status: **{summary['status']}**",
        '',
        '## Sources',
        '| Source | Load Status | Status | Exists | Path |',
        '| --- | --- | --- | --- | --- |',
    ]
    for source in summary['sources']:
        lines.append(f"| {source['label']} | {source['load_status']} | {source['status']} | {source['exists']} | `{source['path']}` |")

    lines.extend(['', '## Metrics'])
    for key, value in summary['metrics'].items():
        lines.append(f'- {key}: {value}')

    lines.extend(['', '## Blockers'])
    if summary['blockers']:
        for blocker in summary['blockers']:
            lines.append(f'- {blocker}')
    else:
        lines.append('- None.')

    lines.extend(['', '## Next Steps'])
    if summary['next_steps']:
        for step in summary['next_steps']:
            lines.append(f'- {step}')
    else:
        lines.append('- None. Governance readiness is complete.')
    lines.append('')
    return '\n'.join(lines)


def write_summary(audit_path, approval_path, out_json, out_md):
    summary = build_summary(audit_path, approval_path)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(summary), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': summary['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive governance readiness summary from audit and approval records')
    parser.add_argument('--audit', default=DEFAULT_AUDIT)
    parser.add_argument('--approval', default=DEFAULT_APPROVAL)
    parser.add_argument('--out-json', default='archive_governance_readiness_summary.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md')
    args = parser.parse_args()

    result = write_summary(args.audit, args.approval, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
