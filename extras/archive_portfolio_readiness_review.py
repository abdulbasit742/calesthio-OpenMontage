#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_FILES = {
    'snapshot': 'archive_portfolio_snapshot.json',
    'digest': 'archive_portfolio_digest.json',
    'dashboard': 'archive_portfolio_dashboard.json',
}

READINESS_CHECKS = [
    {
        'name': 'snapshot-complete',
        'source': 'snapshot',
        'ready_statuses': ['complete'],
        'description': 'Final snapshot manifest exists and reports all expected files.',
    },
    {
        'name': 'digest-ready',
        'source': 'digest',
        'ready_statuses': ['ready'],
        'description': 'Executive digest is ready for review.',
    },
    {
        'name': 'dashboard-ready',
        'source': 'dashboard',
        'ready_statuses': ['ready'],
        'description': 'Portfolio dashboard has no reported attention blockers.',
    },
]


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json'}


def get_status(data):
    if not isinstance(data, dict):
        return 'missing'
    return data.get('status') or data.get('overall_status') or data.get('portfolio_status') or 'available'


def build_checks(sources):
    checks = []
    for check in READINESS_CHECKS:
        data = sources.get(check['source'])
        status = get_status(data)
        passed = status in check['ready_statuses']
        checks.append({
            'name': check['name'],
            'source': check['source'],
            'description': check['description'],
            'source_status': status,
            'passed': passed,
        })
    return checks


def collect_notes(sources):
    notes = []
    for source_name, data in sources.items():
        if isinstance(data, dict):
            headline = data.get('headline')
            if headline:
                notes.append(f'{source_name}: {headline}')
            for item in data.get('next_steps', [])[:4]:
                notes.append(f'{source_name}: {item}')
            for item in data.get('executive_next_steps', [])[:4]:
                notes.append(f'{source_name}: {item}')
    if not notes:
        notes.append('No source notes available. Generate snapshot, digest, and dashboard first.')
    return notes[:12]


def build_review(projects_root='projects', reviewer_name='', review_note=''):
    sources = {name: load_json(path) for name, path in SOURCE_FILES.items()}
    checks = build_checks(sources)
    missing_sources = [name for name, data in sources.items() if data is None]
    failed_checks = [check for check in checks if not check['passed']]
    status = 'ready-for-final-review' if not missing_sources and not failed_checks else 'needs-review'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'reviewer_name': reviewer_name,
        'review_note': review_note,
        'status': status,
        'source_files': SOURCE_FILES,
        'missing_source_count': len(missing_sources),
        'failed_check_count': len(failed_checks),
        'checks': checks,
        'source_notes': collect_notes(sources),
        'review_statement': build_statement(status, reviewer_name),
    }


def build_statement(status, reviewer_name):
    reviewer = reviewer_name or 'Reviewer'
    if status == 'ready-for-final-review':
        return f'{reviewer} can continue with final human review of the archive portfolio package.'
    return f'{reviewer} should resolve listed review items before final archive package review.'


def render_markdown(review):
    lines = [
        '# Archive Portfolio Readiness Review',
        '',
        f"Generated UTC: {review['generated_on_utc']}",
        f"Projects root: `{review['projects_root']}`",
        f"Reviewer: **{review['reviewer_name'] or 'Not assigned'}**",
        f"Status: **{review['status']}**",
        f"Missing sources: **{review['missing_source_count']}**",
        f"Failed checks: **{review['failed_check_count']}**",
        '',
        f"**Review statement:** {review['review_statement']}",
        '',
        '## Readiness Checks',
        '| Check | Source | Source Status | Passed | Description |',
        '| --- | --- | --- | --- | --- |',
    ]
    for check in review['checks']:
        lines.append(
            f"| {check['name']} | {check['source']} | {check['source_status']} | {check['passed']} | {check['description']} |"
        )
    lines.extend(['', '## Source Notes'])
    for note in review['source_notes']:
        lines.append(f'- {note}')
    if review['review_note']:
        lines.extend(['', '## Review Note', review['review_note']])
    lines.append('')
    return '\n'.join(lines)


def write_review(projects_root, reviewer_name, review_note, out_json, out_md):
    review = build_review(projects_root=projects_root, reviewer_name=reviewer_name, review_note=review_note)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(review, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(review), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': review['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a final archive portfolio readiness review checklist for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--reviewer-name', default='')
    parser.add_argument('--review-note', default='')
    parser.add_argument('--out-json', default='archive_portfolio_readiness_review.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_READINESS_REVIEW.md')
    args = parser.parse_args()

    result = write_review(args.projects_root, args.reviewer_name, args.review_note, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
