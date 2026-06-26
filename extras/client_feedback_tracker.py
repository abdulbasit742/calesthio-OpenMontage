#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_TRACKER = {
    'version': 1,
    'created_on_utc': None,
    'updated_on_utc': None,
    'feedback': [],
}

VALID_STATUSES = {'open', 'in-progress', 'resolved', 'closed'}
VALID_PRIORITIES = {'low', 'medium', 'high', 'urgent'}


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def load_tracker(path):
    file_path = Path(path)
    if not file_path.exists():
        tracker = dict(DEFAULT_TRACKER)
        tracker['created_on_utc'] = now_utc()
        tracker['updated_on_utc'] = tracker['created_on_utc']
        return tracker
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        raise SystemExit(f'Invalid JSON tracker: {file_path}')


def save_tracker(path, tracker):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    tracker['updated_on_utc'] = now_utc()
    file_path.write_text(json.dumps(tracker, indent=2), encoding='utf-8')


def next_id(tracker):
    existing = [item.get('id', 0) for item in tracker.get('feedback', [])]
    return (max(existing) if existing else 0) + 1


def add_feedback(tracker, note, source, priority, owner):
    if priority not in VALID_PRIORITIES:
        raise SystemExit(f'Invalid priority. Use one of: {sorted(VALID_PRIORITIES)}')
    item = {
        'id': next_id(tracker),
        'note': note,
        'source': source,
        'priority': priority,
        'owner': owner,
        'status': 'open',
        'created_on_utc': now_utc(),
        'updated_on_utc': now_utc(),
        'resolution_note': '',
    }
    tracker.setdefault('feedback', []).append(item)
    return item


def update_status(tracker, feedback_id, status, resolution_note=''):
    if status not in VALID_STATUSES:
        raise SystemExit(f'Invalid status. Use one of: {sorted(VALID_STATUSES)}')
    for item in tracker.get('feedback', []):
        if item.get('id') == feedback_id:
            item['status'] = status
            item['updated_on_utc'] = now_utc()
            if resolution_note:
                item['resolution_note'] = resolution_note
            return item
    raise SystemExit(f'Feedback item not found: {feedback_id}')


def summarize(tracker):
    feedback = tracker.get('feedback', [])
    by_status = Counter(item.get('status', 'open') for item in feedback)
    by_priority = Counter(item.get('priority', 'medium') for item in feedback)
    open_items = [item for item in feedback if item.get('status') in {'open', 'in-progress'}]
    return {
        'total_feedback': len(feedback),
        'open_feedback': len(open_items),
        'status_counts': dict(sorted(by_status.items())),
        'priority_counts': dict(sorted(by_priority.items())),
        'ready_for_closeout': len(open_items) == 0,
    }


def render_markdown(tracker, summary):
    lines = [
        '# Client Feedback Tracker',
        '',
        f"Updated UTC: {tracker.get('updated_on_utc')}",
        f"Total feedback: **{summary['total_feedback']}**",
        f"Open feedback: **{summary['open_feedback']}**",
        f"Ready for closeout: **{summary['ready_for_closeout']}**",
        '',
        '## Feedback Items',
        '| ID | Status | Priority | Owner | Source | Note |',
        '| ---: | --- | --- | --- | --- | --- |',
    ]
    for item in tracker.get('feedback', []):
        note = item.get('note', '').replace('|', '/')
        lines.append(
            f"| {item.get('id')} | {item.get('status')} | {item.get('priority')} | {item.get('owner') or '-'} | {item.get('source') or '-'} | {note} |"
        )
    lines.append('')
    return '\n'.join(lines)


def write_markdown(tracker_path, tracker):
    summary = summarize(tracker)
    md_path = Path(tracker_path).with_suffix('.md')
    md_path.write_text(render_markdown(tracker, summary), encoding='utf-8')
    return str(md_path)


def main():
    parser = argparse.ArgumentParser(description='Track client feedback after OpenMontage Plus delivery')
    parser.add_argument('command', choices=['add', 'status', 'summary', 'list'])
    parser.add_argument('--tracker', default='projects/demo-video/client_feedback_tracker.json')
    parser.add_argument('--note', default='')
    parser.add_argument('--source', default='client-email')
    parser.add_argument('--priority', default='medium')
    parser.add_argument('--owner', default='editor')
    parser.add_argument('--id', type=int, default=0)
    parser.add_argument('--status-value', default='resolved')
    parser.add_argument('--resolution-note', default='')
    args = parser.parse_args()

    tracker = load_tracker(args.tracker)

    if args.command == 'add':
        if not args.note.strip():
            raise SystemExit('Use --note to add client feedback.')
        result = add_feedback(tracker, args.note.strip(), args.source, args.priority, args.owner)
        save_tracker(args.tracker, tracker)
        write_markdown(args.tracker, tracker)
    elif args.command == 'status':
        if args.id < 1:
            raise SystemExit('Use --id to update a feedback item.')
        result = update_status(tracker, args.id, args.status_value, args.resolution_note)
        save_tracker(args.tracker, tracker)
        write_markdown(args.tracker, tracker)
    elif args.command == 'summary':
        result = summarize(tracker)
        save_tracker(args.tracker, tracker)
        write_markdown(args.tracker, tracker)
    else:
        result = tracker.get('feedback', [])
        save_tracker(args.tracker, tracker)
        write_markdown(args.tracker, tracker)

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
