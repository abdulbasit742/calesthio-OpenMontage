#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OPEN_STATUSES = {'open', 'in-progress'}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def build_report(tracker_path):
    tracker_file = Path(tracker_path)
    tracker = load_json(tracker_file, {'feedback': []})
    feedback = tracker.get('feedback', [])
    status_counts = Counter(item.get('status', 'open') for item in feedback)
    priority_counts = Counter(item.get('priority', 'medium') for item in feedback)
    open_items = [item for item in feedback if item.get('status', 'open') in OPEN_STATUSES]
    urgent_open = [item for item in open_items if item.get('priority') == 'urgent']
    high_open = [item for item in open_items if item.get('priority') == 'high']
    return {
        'tracker': str(tracker_file),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'ready-for-closeout' if not open_items else 'feedback-open',
        'total_feedback': len(feedback),
        'open_feedback': len(open_items),
        'urgent_open': len(urgent_open),
        'high_open': len(high_open),
        'status_counts': dict(sorted(status_counts.items())),
        'priority_counts': dict(sorted(priority_counts.items())),
        'open_items': open_items,
        'closeout_recommendation': closeout_recommendation(open_items, urgent_open, high_open),
    }


def closeout_recommendation(open_items, urgent_open, high_open):
    if urgent_open:
        return 'Resolve urgent feedback before closeout.'
    if high_open:
        return 'Resolve high-priority feedback before closeout.'
    if open_items:
        return 'Review remaining open feedback before closeout.'
    return 'All feedback is resolved or closed. Project is ready for closeout.'


def render_markdown(report):
    lines = [
        '# Client Feedback Report',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Tracker: `{report['tracker']}`",
        f"Status: **{report['status']}**",
        f"Total feedback: **{report['total_feedback']}**",
        f"Open feedback: **{report['open_feedback']}**",
        f"Urgent open: **{report['urgent_open']}**",
        f"High open: **{report['high_open']}**",
        '',
        f"Recommendation: {report['closeout_recommendation']}",
        '',
        '## Status Counts',
    ]
    if report['status_counts']:
        for status, count in report['status_counts'].items():
            lines.append(f'- {status}: {count}')
    else:
        lines.append('- None')
    lines.extend(['', '## Priority Counts'])
    if report['priority_counts']:
        for priority, count in report['priority_counts'].items():
            lines.append(f'- {priority}: {count}')
    else:
        lines.append('- None')
    lines.extend(['', '## Open Items', '| ID | Priority | Owner | Source | Note |', '| ---: | --- | --- | --- | --- |'])
    if report['open_items']:
        for item in report['open_items']:
            note = item.get('note', '').replace('|', '/')
            lines.append(f"| {item.get('id')} | {item.get('priority')} | {item.get('owner') or '-'} | {item.get('source') or '-'} | {note} |")
    else:
        lines.append('| - | - | - | - | No open feedback |')
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
    return {'json': str(json_path), 'markdown': str(md_path), 'status': report['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a client feedback closeout report from an OpenMontage Plus feedback tracker')
    parser.add_argument('--tracker', default='projects/demo-video/client_feedback_tracker.json')
    parser.add_argument('--out-json', default='projects/demo-video/client_feedback_report.json')
    parser.add_argument('--out-md', default='projects/demo-video/CLIENT_FEEDBACK_REPORT.md')
    args = parser.parse_args()

    result = write_report(args.tracker, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
