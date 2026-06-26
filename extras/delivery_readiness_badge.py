#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def score_status(report_index, review_summary, approval_gate, content_review):
    index_status = report_index.get('status', 'missing')
    review_status = review_summary.get('status', 'missing')
    approval_status = approval_gate.get('status', 'missing')
    content_status = content_review.get('status', 'missing')

    if approval_status == 'approved-for-delivery':
        return 'ready', 'brightgreen', 'Approved for delivery'
    if any(status in {'blocked', 'failed'} for status in [review_status, approval_status, content_status]):
        return 'blocked', 'red', 'Fix blocking review items'
    if index_status in {'missing', 'needs-attention'}:
        return 'needs_reports', 'orange', 'Refresh or generate missing reports'
    if any(status in {'needs-review', 'pending', 'needs-work'} for status in [review_status, approval_status, content_status]):
        return 'review', 'yellow', 'Needs final review'
    return 'unknown', 'lightgrey', 'Run review pipeline'


def build_badge(project):
    project_dir = Path(project)
    report_index = load_json(project_dir / 'report_index.json', {})
    review_summary = load_json(project_dir / 'project_review_summary.json', {})
    approval_gate = load_json(project_dir / 'approval_gate.json', {})
    content_review = load_json(project_dir / 'content_risk_check.json', {})
    state, color, message = score_status(report_index, review_summary, approval_gate, content_review)
    return {
        'schemaVersion': 1,
        'label': 'delivery',
        'message': state,
        'color': color,
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'human_message': message,
        'source_statuses': {
            'report_index': report_index.get('status', 'missing'),
            'project_review_summary': review_summary.get('status', 'missing'),
            'approval_gate': approval_gate.get('status', 'missing'),
            'content_review': content_review.get('status', 'missing'),
        },
    }


def render_markdown(badge):
    lines = [
        '# Delivery Readiness Badge',
        '',
        f"Project: `{badge['project']}`",
        f"Generated UTC: {badge['generated_on_utc']}",
        f"Badge: **{badge['label']}: {badge['message']}**",
        f"Color: `{badge['color']}`",
        f"Meaning: {badge['human_message']}",
        '',
        '## Source Statuses',
        '| Source | Status |',
        '| --- | --- |',
    ]
    for name, status in badge['source_statuses'].items():
        lines.append(f'| {name} | {status} |')
    lines.extend([
        '',
        '## Suggested Badge JSON',
        '',
        '```json',
        json.dumps({
            'schemaVersion': badge['schemaVersion'],
            'label': badge['label'],
            'message': badge['message'],
            'color': badge['color'],
        }, indent=2),
        '```',
        '',
    ])
    return '\n'.join(lines)


def write_badge(project, out_json, out_md):
    badge = build_badge(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(badge, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(badge), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'message': badge['message'], 'color': badge['color']}


def main():
    parser = argparse.ArgumentParser(description='Generate a delivery readiness badge from OpenMontage Plus project reports')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/delivery_readiness_badge.json')
    parser.add_argument('--out-md', default='projects/demo-video/DELIVERY_READINESS_BADGE.md')
    args = parser.parse_args()

    result = write_badge(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
