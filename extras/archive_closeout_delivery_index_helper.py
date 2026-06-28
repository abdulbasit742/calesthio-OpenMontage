#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-closeout-delivery-index-helper',
    'script': 'extras/archive_closeout_delivery_index.py',
    'example': 'python extras/archive_closeout_delivery_index.py --label archive-closeout-delivery-index --owner "Archive Owner" --out-json archive_closeout_delivery_index.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md',
    'description': 'Build the final archive closeout delivery index across closeout JSON and Markdown records.',
    'area': 'portfolio',
    'outputs': [
        'archive_closeout_delivery_index.json',
        'ARCHIVE_CLOSEOUT_DELIVERY_INDEX.md',
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
    parser = argparse.ArgumentParser(description='Archive closeout delivery index command helper for OpenMontage Plus')
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
