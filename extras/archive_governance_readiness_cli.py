#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-governance-readiness-summary',
    'script': 'extras/archive_governance_readiness_summary.py',
    'example': 'python extras/archive_governance_readiness_summary.py --audit archive_toolchain_audit.json --approval archive_portfolio_governance_approval_record.json --out-json archive_governance_readiness_summary.json --out-md ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md',
    'description': 'Build final archive governance readiness summary from audit and approval records.',
    'area': 'portfolio',
    'outputs': [
        'archive_governance_readiness_summary.json',
        'ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md',
    ],
}


def show_tool():
    row = dict(TOOL)
    row['exists'] = Path(row['script']).exists()
    return row


def render_command(extra_args):
    return ['python', TOOL['script']] + extra_args


def list_tool():
    return [show_tool()]


def main():
    parser = argparse.ArgumentParser(description='Governance readiness CLI companion for OpenMontage Plus')
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
