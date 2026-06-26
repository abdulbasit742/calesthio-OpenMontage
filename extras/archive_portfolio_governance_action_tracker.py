#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SUMMARY_PATH = 'archive_portfolio_governance_summary.json'


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json', 'governance_actions': []}


def infer_priority(action):
    lowered = action.lower()
    if any(word in lowered for word in ('missing', 'failed', 'non-ready', 'attention', 'invalid')):
        return 'high'
    if any(word in lowered for word in ('review', 'approve', 'schedule')):
        return 'medium'
    return 'normal'


def build_action_rows(actions, owner_name):
    rows = []
    for index, action in enumerate(actions, start=1):
        rows.append({
            'id': f'GOV-{index:03d}',
            'action': action,
            'owner': owner_name or 'Archive Owner',
            'priority': infer_priority(action),
            'status': 'open',
            'notes': '',
        })
    if not rows:
        rows.append({
            'id': 'GOV-001',
            'action': 'Review governance summary and store final governance record files together.',
            'owner': owner_name or 'Archive Owner',
            'priority': 'normal',
            'status': 'open',
            'notes': '',
        })
    return rows


def build_tracker(summary_path=DEFAULT_SUMMARY_PATH, owner_name=''):
    summary = load_json(summary_path)
    actions = summary.get('governance_actions', []) if isinstance(summary, dict) else []
    rows = build_action_rows(actions, owner_name or (summary.get('owner_name', '') if isinstance(summary, dict) else ''))
    high_count = sum(1 for row in rows if row['priority'] == 'high')
    medium_count = sum(1 for row in rows if row['priority'] == 'medium')
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'summary_path': summary_path,
        'source_exists': summary is not None,
        'source_status': summary.get('status', 'missing') if isinstance(summary, dict) else 'missing',
        'status': 'actions-ready' if summary is not None else 'needs-attention',
        'action_count': len(rows),
        'high_priority_count': high_count,
        'medium_priority_count': medium_count,
        'actions': rows,
    }


def render_markdown(tracker):
    lines = [
        '# Archive Portfolio Governance Action Tracker',
        '',
        f"Generated UTC: {tracker['generated_on_utc']}",
        f"Summary source: `{tracker['summary_path']}`",
        f"Source exists: **{tracker['source_exists']}**",
        f"Source status: **{tracker['source_status']}**",
        f"Tracker status: **{tracker['status']}**",
        '',
        '## Counts',
        f"- Actions: {tracker['action_count']}",
        f"- High priority: {tracker['high_priority_count']}",
        f"- Medium priority: {tracker['medium_priority_count']}",
        '',
        '## Actions',
        '| ID | Priority | Owner | Status | Action | Notes |',
        '| --- | --- | --- | --- | --- | --- |',
    ]
    for row in tracker['actions']:
        lines.append(f"| {row['id']} | {row['priority']} | {row['owner']} | {row['status']} | {row['action']} | {row['notes']} |")
    lines.extend(['', '## Closeout Use', '', 'Update the status and notes columns as governance actions are completed, then keep this tracker with the final archive governance summary.', ''])
    return '\n'.join(lines)


def write_tracker(summary_path, owner_name, out_json, out_md):
    tracker = build_tracker(summary_path, owner_name)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(tracker, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(tracker), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': tracker['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio governance action tracker for OpenMontage Plus')
    parser.add_argument('--summary', default=DEFAULT_SUMMARY_PATH)
    parser.add_argument('--owner-name', default='')
    parser.add_argument('--out-json', default='archive_portfolio_governance_action_tracker.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_GOVERNANCE_ACTION_TRACKER.md')
    args = parser.parse_args()

    result = write_tracker(args.summary, args.owner_name, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
