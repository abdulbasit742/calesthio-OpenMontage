#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REVIEW_SOURCES = {
    'retention_policy': 'archive_portfolio_retention_policy.json',
    'handoff_receipt': 'archive_portfolio_handoff_receipt.json',
    'release_packet': 'archive_portfolio_release_packet.json',
    'snapshot': 'archive_portfolio_snapshot.json',
}

REQUIRED_POLICY_SECTIONS = [
    'input_summary',
    'retention_groups',
    'cleanup_rules',
    'next_steps',
]


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
    for name, path in REVIEW_SOURCES.items():
        data = load_json(path)
        rows.append({
            'name': name,
            'path': path,
            'exists': data is not None,
            'status': data.get('status', 'available') if isinstance(data, dict) else 'missing',
        })
    return rows


def policy_checks(policy):
    checks = []
    if not isinstance(policy, dict):
        return [{
            'name': 'retention-policy-json',
            'passed': False,
            'message': 'Retention policy JSON is missing or invalid.',
        }]

    for section in REQUIRED_POLICY_SECTIONS:
        value = policy.get(section)
        checks.append({
            'name': f'policy-section-{section}',
            'passed': bool(value),
            'message': f'Required section `{section}` is present.' if value else f'Required section `{section}` is missing or empty.',
        })

    groups = policy.get('retention_groups', [])
    checks.append({
        'name': 'retention-groups-defined',
        'passed': len(groups) >= 1,
        'message': f'{len(groups)} retention groups defined.',
    })
    checks.append({
        'name': 'cleanup-rules-defined',
        'passed': len(policy.get('cleanup_rules', [])) >= 1,
        'message': f"{len(policy.get('cleanup_rules', []))} cleanup rules defined.",
    })
    checks.append({
        'name': 'owner-assigned',
        'passed': bool(policy.get('owner_name')),
        'message': 'Retention owner assigned.' if policy.get('owner_name') else 'Retention owner is not assigned.',
    })
    missing_files = sum(group.get('missing_count', 0) for group in groups if isinstance(group, dict))
    checks.append({
        'name': 'retention-files-available',
        'passed': missing_files == 0,
        'message': f'{missing_files} retention files missing across policy groups.',
    })
    return checks


def build_decisions(checks):
    decisions = []
    failed = [check for check in checks if not check['passed']]
    if failed:
        decisions.append('Do not approve retention policy until failed checks are resolved.')
        decisions.append('Assign an owner and regenerate any missing handoff, release, snapshot, or policy files.')
    else:
        decisions.append('Approve retention policy for owner review and store it with the handoff receipt.')
        decisions.append('Schedule the first retention review according to the policy review cadence.')
    decisions.append('Keep release packet, handoff note, receipt, and retention review together as the governance record.')
    return decisions


def build_review(projects_root='projects', reviewer_name='', review_note='Retention policy review'):
    sources = source_rows()
    policy = load_json(REVIEW_SOURCES['retention_policy'])
    checks = policy_checks(policy)
    missing_source_count = sum(1 for row in sources if not row['exists'])
    attention_source_count = sum(
        1 for row in sources
        if row['exists'] and row['status'] not in {'ready', 'complete', 'ready-for-final-review', 'ready-to-package', 'ready-to-send', 'ready-for-acknowledgement', 'ready-for-retention-review'}
    )
    failed_check_count = sum(1 for check in checks if not check['passed'])
    status = 'ready-for-retention-approval' if not missing_source_count and not attention_source_count and not failed_check_count else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'reviewer_name': reviewer_name,
        'review_note': review_note,
        'status': status,
        'source_summary': sources,
        'checks': checks,
        'missing_source_count': missing_source_count,
        'attention_source_count': attention_source_count,
        'failed_check_count': failed_check_count,
        'decisions': build_decisions(checks),
    }


def render_markdown(review):
    lines = [
        '# Archive Portfolio Retention Review',
        '',
        f"Generated UTC: {review['generated_on_utc']}",
        f"Projects root: `{review['projects_root']}`",
        f"Reviewer: **{review['reviewer_name'] or 'Unassigned'}**",
        f"Review note: {review['review_note']}",
        f"Status: **{review['status']}**",
        '',
        '## Source Summary',
        '| Source | Path | Exists | Status |',
        '| --- | --- | --- | --- |',
    ]
    for row in review['source_summary']:
        lines.append(f"| {row['name']} | `{row['path']}` | {row['exists']} | {row['status']} |")
    lines.extend(['', '## Review Checks', '| Check | Passed | Message |', '| --- | --- | --- |'])
    for check in review['checks']:
        lines.append(f"| {check['name']} | {check['passed']} | {check['message']} |")
    lines.extend(['', '## Counts'])
    lines.append(f"- Missing sources: {review['missing_source_count']}")
    lines.append(f"- Sources needing attention: {review['attention_source_count']}")
    lines.append(f"- Failed checks: {review['failed_check_count']}")
    lines.extend(['', '## Decisions'])
    for decision in review['decisions']:
        lines.append(f'- {decision}')
    lines.extend(['', '## Approval Fields', '', '- Reviewer signature/date:', '- Owner approval/date:', '- Notes:', ''])
    return '\n'.join(lines)


def write_review(projects_root, reviewer_name, review_note, out_json, out_md):
    review = build_review(projects_root, reviewer_name, review_note)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(review, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(review), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': review['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio retention review for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--reviewer-name', default='')
    parser.add_argument('--review-note', default='Retention policy review')
    parser.add_argument('--out-json', default='archive_portfolio_retention_review.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_RETENTION_REVIEW.md')
    args = parser.parse_args()

    result = write_review(args.projects_root, args.reviewer_name, args.review_note, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
