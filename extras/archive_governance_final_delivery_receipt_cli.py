#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-governance-final-delivery-receipt',
    'script': 'extras/archive_governance_final_delivery_receipt.py',
    'example': 'python extras/archive_governance_final_delivery_receipt.py --checklist archive_governance_final_delivery_checklist.json --sender "Archive Owner" --recipient "Archive Reviewer" --package-id archive-governance-final-package --note "Final archive governance package delivered for reviewer acknowledgement." --out-json archive_governance_final_delivery_receipt.json --out-md ARCHIVE_GOVERNANCE_FINAL_DELIVERY_RECEIPT.md',
    'description': 'Build final archive governance delivery receipt after the final delivery checklist is delivery-ready.',
    'area': 'portfolio',
    'outputs': [
        'archive_governance_final_delivery_receipt.json',
        'ARCHIVE_GOVERNANCE_FINAL_DELIVERY_RECEIPT.md',
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
    parser = argparse.ArgumentParser(description='Governance final delivery receipt CLI companion for OpenMontage Plus')
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
