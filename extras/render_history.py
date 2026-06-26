#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_HISTORY = Path('render_history.jsonl')


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def append_event(history_path, event):
    history_path.parent.mkdir(parents=True, exist_ok=True)
    event['created_at'] = now_iso()
    with history_path.open('a', encoding='utf-8') as file:
        file.write(json.dumps(event, sort_keys=True) + '\n')
    return event


def read_events(history_path):
    if not history_path.exists():
        return []
    events = []
    for line in history_path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def summarize(events):
    counts = {}
    total_cost = 0.0
    for event in events:
        status = event.get('status', 'unknown')
        counts[status] = counts.get(status, 0) + 1
        total_cost += float(event.get('cost_usd', 0) or 0)
    return {
        'total_events': len(events),
        'status_counts': counts,
        'total_cost_usd': round(total_cost, 4),
    }


def main():
    parser = argparse.ArgumentParser(description='Track OpenMontage Plus render history')
    parser.add_argument('command', choices=['add', 'list', 'summary'])
    parser.add_argument('--history', default=str(DEFAULT_HISTORY))
    parser.add_argument('--project', default='demo-video')
    parser.add_argument('--status', default='completed')
    parser.add_argument('--output', default='')
    parser.add_argument('--duration-seconds', type=float, default=0)
    parser.add_argument('--cost-usd', type=float, default=0)
    parser.add_argument('--note', default='')
    args = parser.parse_args()

    history_path = Path(args.history)
    if args.command == 'add':
        event = {
            'project': args.project,
            'status': args.status,
            'output': args.output,
            'duration_seconds': args.duration_seconds,
            'cost_usd': args.cost_usd,
            'note': args.note,
        }
        print(json.dumps(append_event(history_path, event), indent=2))
    elif args.command == 'list':
        print(json.dumps(read_events(history_path), indent=2))
    elif args.command == 'summary':
        print(json.dumps(summarize(read_events(history_path)), indent=2))


if __name__ == '__main__':
    main()
