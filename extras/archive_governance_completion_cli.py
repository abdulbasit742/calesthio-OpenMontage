#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-governance-completion-record',
    'script': 'extras/archive_governance_completion_record.py',
    'example': 'python extras/archive_governance_completion_record.py --readiness archive_governance_readiness_summary.json --owner-name ArchiveOwner --note "Final governance readiness reviewed" --out-json archive_governance_completion_record.json --out-md ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md',
    'description': 'Build final archive governance completion record from readiness summary.',
    'area': 'portfolio',
    'outputs': [
        'archive_governance_completion_record.json',
        'ARCHIVE_GOVERNANCE_COMPLETION_RECORD.md',
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
    parser = argparse.ArgumentParser(description='Governance completion CLI companion for OpenMontage Plus')
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
