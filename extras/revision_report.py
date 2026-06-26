#!/usr/bin/env python3
import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

STATUS_ORDER = ['open', 'in-progress', 'blocked', 'resolved', 'cancelled']
PRIORITY_ORDER = ['high', 'medium', 'low']


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def priority_rank(value):
    return PRIORITY_ORDER.index(value) if value in PRIORITY_ORDER else len(PRIORITY_ORDER)


def status_rank(value):
    return STATUS_ORDER.index(value) if value in STATUS_ORDER else len(STATUS_ORDER)


def load_revisions(tracker_path):
    tracker = load_json(tracker_path, {'revisions': []})
    revisions = tracker.get('revisions', [])
    return sorted(
        revisions,
        key=lambda item: (
            status_rank(item.get('status', 'open')),
            priority_rank(item.get('priority', 'medium')),
            item.get('due_date') or '9999-99-99',
            item.get('id', ''),
        ),
    )


def build_report(tracker_path):
    revisions = load_revisions(tracker_path)
    status_counts = Counter(item.get('status', 'open') for item in revisions)
    priority_counts = Counter(item.get('priority', 'medium') for item in revisions)
    owner_counts = Counter(item.get('owner', 'unassigned') for item in revisions)
    by_project = defaultdict(list)
    for revision in revisions:
        by_project[revision.get('project', 'unknown')].append(revision)

    open_items = [item for item in revisions if item.get('status') not in {'resolved', 'cancelled'}]
    blocked_items = [item for item in revisions if item.get('status') == 'blocked']
    high_priority_open = [item for item in open_items if item.get('priority') == 'high']

    return {
        'generated_on': date.today().isoformat(),
        'tracker': str(tracker_path),
        'summary': {
            'total': len(revisions),
            'open_active': len(open_items),
            'resolved': status_counts.get('resolved', 0),
            'blocked': len(blocked_items),
            'high_priority_open': len(high_priority_open),
            'status_counts': dict(status_counts),
            'priority_counts': dict(priority_counts),
            'owner_counts': dict(owner_counts),
            'project_count': len(by_project),
        },
        'projects': {project: items for project, items in sorted(by_project.items())},
        'revisions': revisions,
        'next_actions': next_actions(open_items, blocked_items, high_priority_open),
    }


def next_actions(open_items, blocked_items, high_priority_open):
    actions = []
    if high_priority_open:
        actions.append(f'Resolve {len(high_priority_open)} high-priority open revision(s) first.')
    if blocked_items:
        actions.append(f'Unblock {len(blocked_items)} blocked revision(s) before final delivery.')
    if open_items:
        actions.append(f'Complete or cancel {len(open_items)} active revision(s).')
    if not actions:
        actions.append('All revisions are resolved or cancelled. Project is ready for final approval.')
    return actions


def render_revision_line(item):
    return ' | '.join([
        item.get('id', ''),
        item.get('status', ''),
        item.get('priority', ''),
        item.get('owner', ''),
        item.get('due_date', '') or 'no due date',
        item.get('note', '').replace('|', '/'),
    ])


def render_markdown(report):
    summary = report['summary']
    lines = [
        '# Revision Report',
        '',
        f"Generated: {report['generated_on']}",
        f"Tracker: `{report['tracker']}`",
        '',
        '## Summary',
        f"- Total revisions: {summary['total']}",
        f"- Active open revisions: {summary['open_active']}",
        f"- Resolved: {summary['resolved']}",
        f"- Blocked: {summary['blocked']}",
        f"- High-priority open: {summary['high_priority_open']}",
        f"- Projects with revisions: {summary['project_count']}",
        '',
        '## Next Actions',
    ]
    lines.extend([f'- {action}' for action in report['next_actions']])
    lines.extend(['', '## Revision Table', '| ID | Status | Priority | Owner | Due Date | Note |', '| --- | --- | --- | --- | --- | --- |'])
    if report['revisions']:
        lines.extend([f"| {render_revision_line(item)} |" for item in report['revisions']])
    else:
        lines.append('| none | none | none | none | none | No revisions recorded. |')
    lines.append('')
    return '\n'.join(lines)


def write_report(tracker, out_json, out_md):
    report = build_report(tracker)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'summary': report['summary']}


def main():
    parser = argparse.ArgumentParser(description='Generate a Markdown and JSON report from an OpenMontage Plus revision tracker')
    parser.add_argument('--tracker', default='revision_tracker.json')
    parser.add_argument('--out-json', default='revision_report.json')
    parser.add_argument('--out-md', default='REVISION_REPORT.md')
    args = parser.parse_args()

    result = write_report(args.tracker, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
