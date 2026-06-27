#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-governance-final-packet',
    'script': 'extras/archive_governance_final_packet.py',
    'example': 'python extras/archive_governance_final_packet.py --label archive-governance-final-packet --out-json archive_governance_final_packet.json --out-md ARCHIVE_GOVERNANCE_FINAL_PACKET.md',
    'description': 'Build final archive governance packet manifest from audit, approval, readiness, and completion outputs.',
    'area': 'portfolio',
    'outputs': [
        'archive_governance_final_packet.json',
        'ARCHIVE_GOVERNANCE_FINAL_PACKET.md',
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
    parser = argparse.ArgumentParser(description='Governance final packet CLI companion for OpenMontage Plus')
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
