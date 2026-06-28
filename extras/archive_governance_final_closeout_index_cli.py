#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-governance-final-closeout-index',
    'script': 'extras/archive_governance_final_closeout_index.py',
    'example': 'python extras/archive_governance_final_closeout_index.py --label archive-governance-final-closeout --owner "Archive Owner" --out-json archive_governance_final_closeout_index.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md',
    'description': 'Build final archive governance closeout index after closure certificate is closed.',
    'area': 'portfolio',
    'outputs': [
        'archive_governance_final_closeout_index.json',
        'ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_INDEX.md',
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
    parser = argparse.ArgumentParser(description='Governance final closeout index CLI companion for OpenMontage Plus')
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
