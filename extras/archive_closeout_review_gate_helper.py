#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-closeout-review-gate-helper',
    'script': 'extras/archive_closeout_review_gate.py',
    'example': 'python extras/archive_closeout_review_gate.py --rollup archive_closeout_rollup.json --reviewer "Archive Reviewer" --decision approve --out-json archive_closeout_review_gate.json --out-md ARCHIVE_CLOSEOUT_REVIEW_GATE.md',
    'description': 'Build a final archive closeout review gate from the rollup checkpoint and reviewer decision.',
    'area': 'portfolio',
    'outputs': [
        'archive_closeout_review_gate.json',
        'ARCHIVE_CLOSEOUT_REVIEW_GATE.md',
    ],
}


def show_tool():
    row = dict(TOOL)
    row['exists'] = Path(row['script']).exists()
    return row


def list_tool():
    return [show_tool()]


def render_command(extra_args):
    return ['python', TOOL['script']] + extra_args


def main():
    parser = argparse.ArgumentParser(description='Archive closeout review gate command helper for OpenMontage Plus')
    sub = parser.add_subparsers(dest='command', required=True)

    sub.add_parser('list')
    sub.add_parser('show')

    command_parser = sub.add_parser('command')
    command_parser.add_argument('args', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    if args.command == 'list':
        result = list_tool()
    elif args.command == 'show':
        result = show_tool()
    else:
        result = render_command(args.args)

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
