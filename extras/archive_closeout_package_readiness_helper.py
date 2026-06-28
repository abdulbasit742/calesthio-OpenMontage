#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-closeout-package-readiness-helper',
    'script': 'extras/archive_closeout_package_readiness.py',
    'example': 'python extras/archive_closeout_package_readiness.py --rollup archive_closeout_rollup.json --review-gate archive_closeout_review_gate.json --manifest archive_closeout_milestone_manifest.json --label archive-closeout-package-readiness --out-json archive_closeout_package_readiness.json --out-md ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md',
    'description': 'Build a final package-level readiness report from rollup, review gate, and milestone manifest checkpoints.',
    'area': 'portfolio',
    'outputs': [
        'archive_closeout_package_readiness.json',
        'ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md',
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
    parser = argparse.ArgumentParser(description='Archive closeout package readiness command helper for OpenMontage Plus')
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
