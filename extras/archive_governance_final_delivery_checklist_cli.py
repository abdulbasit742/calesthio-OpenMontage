#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-governance-final-delivery-checklist',
    'script': 'extras/archive_governance_final_delivery_checklist.py',
    'example': 'python extras/archive_governance_final_delivery_checklist.py --packet archive_governance_final_packet.json --handoff archive_governance_final_handoff_note.json --label archive-governance-final-delivery --out-json archive_governance_final_delivery_checklist.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md',
    'description': 'Build final archive governance delivery checklist from the final packet and handoff note outputs.',
    'area': 'portfolio',
    'outputs': [
        'archive_governance_final_delivery_checklist.json',
        'ARCHIVE_GOVERNANCE_FINAL_DELIVERY_CHECKLIST.md',
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
    parser = argparse.ArgumentParser(description='Governance final delivery checklist CLI companion for OpenMontage Plus')
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
