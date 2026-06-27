#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SUMMARY = 'archive_portfolio_governance_summary.json'
DEFAULT_TRACKER = 'archive_portfolio_governance_action_tracker.json'


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json'}


def build_board(summary_path=DEFAULT_SUMMARY, tracker_path=DEFAULT_TRACKER):
    summary = load_json(summary_path)
    tracker = load_json(tracker_path)
    summary_status = summary.get('status', 'missing') if isinstance(summary, dict) else 'missing'
    tracker_status = tracker.get('status', 'missing') if isinstance(tracker, dict) else 'missing'
    actions = tracker.get('actions', []) if isinstance(tracker, dict) else []
    open_actions = [action for action in actions if action.get('status') != 'done']
    high_actions = [action for action in open_actions if action.get('priority') == 'high']
    status = 'governance-board-ready' if summary and tracker and not high_actions else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': status,
        'summary_path': summary_path,
        'tracker_path': tracker_path,
        'summary_exists': summary is not None,
        'tracker_exists': tracker is not None,
        'summary_status': summary_status,
        'tracker_status': tracker_status,
        'source_metrics': {
            'missing_source_count': summary.get('missing_source_count', 0) if isinstance(summary, dict) else 1,
            'attention_source_count': summary.get('attention_source_count', 0) if isinstance(summary, dict) else 0,
            'failed_check_count': summary.get('failed_check_count', 0) if isinstance(summary, dict) else 0,
        },
        'action_metrics': {
            'action_count': len(actions),
            'open_action_count': len(open_actions),
            'high_priority_open_count': len(high_actions),
        },
        'top_open_actions': open_actions[:10],
    }


def render_markdown(board):
    lines = [
        '# Archive Portfolio Governance Board',
        '',
        f"Generated UTC: {board['generated_on_utc']}",
        f"Status: **{board['status']}**",
        f"Summary: `{board['summary_path']}`",
        f"Tracker: `{board['tracker_path']}`",
        '',
        '## Source Status',
        f"- Summary exists: {board['summary_exists']}",
        f"- Tracker exists: {board['tracker_exists']}",
        f"- Summary status: {board['summary_status']}",
        f"- Tracker status: {board['tracker_status']}",
        '',
        '## Source Metrics',
    ]
    for key, value in board['source_metrics'].items():
        lines.append(f'- {key}: {value}')
    lines.extend(['', '## Action Metrics'])
    for key, value in board['action_metrics'].items():
        lines.append(f'- {key}: {value}')
    lines.extend(['', '## Top Open Actions'])
    if not board['top_open_actions']:
        lines.append('- No open actions found.')
    else:
        lines.extend(['| ID | Priority | Owner | Status | Action |', '| --- | --- | --- | --- | --- |'])
        for action in board['top_open_actions']:
            lines.append(f"| {action.get('id', '')} | {action.get('priority', '')} | {action.get('owner', '')} | {action.get('status', '')} | {action.get('action', '')} |")
    lines.append('')
    return '\n'.join(lines)


def write_board(summary_path, tracker_path, out_json, out_md):
    board = build_board(summary_path, tracker_path)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(board, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(board), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': board['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio governance board for OpenMontage Plus')
    parser.add_argument('--summary', default=DEFAULT_SUMMARY)
    parser.add_argument('--tracker', default=DEFAULT_TRACKER)
    parser.add_argument('--out-json', default='archive_portfolio_governance_board.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_GOVERNANCE_BOARD.md')
    args = parser.parse_args()

    result = write_board(args.summary, args.tracker, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
