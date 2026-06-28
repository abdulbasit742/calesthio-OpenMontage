#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-closeout-delivery-seal-helper',
    'script': 'extras/archive_closeout_delivery_seal.py',
    'example': 'python extras/archive_closeout_delivery_seal.py --acknowledgement archive_closeout_owner_acknowledgement.json --label archive-closeout-final-delivery-seal --owner "Archive Owner" --reviewer "Archive Reviewer" --release-tag archive-closeout-delivery --out-json archive_closeout_delivery_seal.json --out-md ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md',
    'description': 'Build the final archive closeout delivery seal from the owner acknowledgement checkpoint.',
    'area': 'portfolio',
    'outputs': [
        'archive_closeout_delivery_seal.json',
        'ARCHIVE_CLOSEOUT_DELIVERY_SEAL.md',
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
    parser = argparse.ArgumentParser(description='Archive closeout delivery seal command helper for OpenMontage Plus')
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
