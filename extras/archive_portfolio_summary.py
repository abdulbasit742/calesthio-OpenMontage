#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BOARD_FILES = [
    ('status_board', 'archive_status_board.json'),
    ('badge_board', 'archive_badge_board.json'),
    ('completion_board', 'archive_completion_board.json'),
    ('toolchain_audit', 'archive_toolchain_audit.json'),
]


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return {}
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def board_row(name, filename):
    path = Path(filename)
    data = load_json(path)
    return {
        'name': name,
        'path': filename,
        'exists': path.exists(),
        'status': data.get('status', 'missing'),
        'project_count': data.get('project_count', 0),
        'ready_count': data.get('archive_ready_count', data.get('complete_count', 0)),
        'attention_count': data.get('needs_attention_count', data.get('incomplete_count', data.get('missing_count', 0))),
    }


def build_summary():
    rows = [board_row(name, filename) for name, filename in BOARD_FILES]
    missing = [row for row in rows if not row['exists']]
    attention = [row for row in rows if row['status'] in {'missing', 'needs-attention', 'incomplete'}]
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'ready' if not missing and not attention else 'needs-attention',
        'board_count': len(rows),
        'available_board_count': len(rows) - len(missing),
        'missing_board_count': len(missing),
        'attention_board_count': len(attention),
        'rows': rows,
        'next_steps': build_next_steps(missing, attention),
    }


def build_next_steps(missing, attention):
    steps = []
    for row in missing:
        steps.append(f"Generate {row['path']}.")
    for row in attention:
        if row not in missing:
            steps.append(f"Review {row['path']} because status is {row['status']}.")
    if not steps:
        steps.append('All archive boards are ready.')
    return steps


def render_markdown(summary):
    lines = [
        '# Archive Portfolio Summary',
        '',
        f"Generated UTC: {summary['generated_on_utc']}",
        f"Status: **{summary['status']}**",
        f"Boards: **{summary['board_count']}**",
        f"Available boards: **{summary['available_board_count']}**",
        f"Missing boards: **{summary['missing_board_count']}**",
        f"Attention boards: **{summary['attention_board_count']}**",
        '',
        '## Boards',
        '| Board | Exists | Status | Projects | Ready | Attention | Path |',
        '| --- | --- | --- | ---: | ---: | ---: | --- |',
    ]
    for row in summary['rows']:
        lines.append(f"| {row['name']} | {row['exists']} | {row['status']} | {row['project_count']} | {row['ready_count']} | {row['attention_count']} | `{row['path']}` |")
    lines.extend(['', '## Next Steps'])
    for step in summary['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_summary(out_json, out_md):
    summary = build_summary()
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(summary), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': summary['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a summary from OpenMontage Plus archive boards')
    parser.add_argument('--out-json', default='archive_portfolio_summary.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_SUMMARY.md')
    args = parser.parse_args()

    result = write_summary(args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
