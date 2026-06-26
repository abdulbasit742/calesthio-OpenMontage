#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

GOVERNANCE_SOURCES = {
    'retention_review': 'archive_portfolio_retention_review.json',
    'retention_policy': 'archive_portfolio_retention_policy.json',
    'handoff_receipt': 'archive_portfolio_handoff_receipt.json',
    'release_packet': 'archive_portfolio_release_packet.json',
    'readiness_review': 'archive_portfolio_readiness_review.json',
}

READY_STATUSES = {
    'ready',
    'complete',
    'ready-for-final-review',
    'ready-to-package',
    'ready-to-send',
    'ready-for-acknowledgement',
    'ready-for-retention-review',
    'ready-for-retention-approval',
}


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json'}


def source_rows():
    rows = []
    for name, path in GOVERNANCE_SOURCES.items():
        data = load_json(path)
        rows.append({
            'name': name,
            'path': path,
            'exists': data is not None,
            'status': data.get('status', 'missing') if isinstance(data, dict) else 'missing',
            'missing_source_count': data.get('missing_source_count', 0) if isinstance(data, dict) else 0,
            'failed_check_count': data.get('failed_check_count', 0) if isinstance(data, dict) else 0,
            'attention_source_count': data.get('attention_source_count', 0) if isinstance(data, dict) else 0,
        })
    return rows


def collect_actions():
    actions = []
    for name, path in GOVERNANCE_SOURCES.items():
        data = load_json(path)
        if not isinstance(data, dict):
            actions.append(f'Generate missing governance source: {path}')
            continue
        status = data.get('status', 'missing')
        if status not in READY_STATUSES:
            actions.append(f'Review non-ready governance source `{path}` with status `{status}`.')
        for key in ('next_steps', 'decisions'):
            for item in data.get(key, [])[:3]:
                if isinstance(item, str) and item not in actions:
                    actions.append(item)
    if not actions:
        actions.append('Store governance summary with retention review, retention policy, handoff receipt, and release packet.')
    return actions[:12]


def build_summary(projects_root='projects', summary_label='archive-portfolio-governance-summary', owner_name=''):
    sources = source_rows()
    missing_source_count = sum(1 for row in sources if not row['exists'])
    attention_source_count = sum(1 for row in sources if row['exists'] and row['status'] not in READY_STATUSES)
    failed_check_count = sum(row['failed_check_count'] for row in sources)
    status = 'governance-ready' if not missing_source_count and not attention_source_count and not failed_check_count else 'needs-attention'
    return {
        'summary_label': summary_label,
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'owner_name': owner_name,
        'status': status,
        'source_summary': sources,
        'source_count': len(sources),
        'missing_source_count': missing_source_count,
        'attention_source_count': attention_source_count,
        'failed_check_count': failed_check_count,
        'governance_actions': collect_actions(),
        'governance_record_files': [
            'ARCHIVE_PORTFOLIO_RETENTION_REVIEW.md',
            'ARCHIVE_PORTFOLIO_RETENTION_POLICY.md',
            'ARCHIVE_PORTFOLIO_HANDOFF_RECEIPT.md',
            'ARCHIVE_PORTFOLIO_RELEASE_PACKET.md',
            'ARCHIVE_PORTFOLIO_READINESS_REVIEW.md',
        ],
    }


def render_markdown(summary):
    lines = [
        '# Archive Portfolio Governance Summary',
        '',
        f"Summary label: **{summary['summary_label']}**",
        f"Generated UTC: {summary['generated_on_utc']}",
        f"Projects root: `{summary['projects_root']}`",
        f"Owner: **{summary['owner_name'] or 'Unassigned'}**",
        f"Status: **{summary['status']}**",
        '',
        '## Governance Metrics',
        f"- Governance sources: {summary['source_count']}",
        f"- Missing sources: {summary['missing_source_count']}",
        f"- Sources needing attention: {summary['attention_source_count']}",
        f"- Failed checks: {summary['failed_check_count']}",
        '',
        '## Source Summary',
        '| Source | Path | Exists | Status | Missing | Attention | Failed checks |',
        '| --- | --- | --- | --- | ---: | ---: | ---: |',
    ]
    for row in summary['source_summary']:
        lines.append(
            f"| {row['name']} | `{row['path']}` | {row['exists']} | {row['status']} | {row['missing_source_count']} | {row['attention_source_count']} | {row['failed_check_count']} |"
        )
    lines.extend(['', '## Governance Record Files'])
    for path in summary['governance_record_files']:
        lines.append(f'- `{path}`')
    lines.extend(['', '## Governance Actions'])
    for action in summary['governance_actions']:
        lines.append(f'- {action}')
    lines.append('')
    return '\n'.join(lines)


def write_summary(projects_root, summary_label, owner_name, out_json, out_md):
    summary = build_summary(projects_root, summary_label, owner_name)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(summary), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': summary['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio governance summary for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--summary-label', default='archive-portfolio-governance-summary')
    parser.add_argument('--owner-name', default='')
    parser.add_argument('--out-json', default='archive_portfolio_governance_summary.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_GOVERNANCE_SUMMARY.md')
    args = parser.parse_args()

    result = write_summary(args.projects_root, args.summary_label, args.owner_name, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
