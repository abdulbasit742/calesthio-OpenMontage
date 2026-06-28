#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOL = {
    'name': 'archive-governance-closeout-summary-helper',
    'script': 'extras/archive_governance_final_closeout_summary.py',
    'example': 'python extras/archive_governance_final_closeout_summary.py --index archive_governance_final_closeout_index.json --title "Archive Governance Final Closeout Summary" --owner "Archive Owner" --out-json archive_governance_final_closeout_summary.json --out-md ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_SUMMARY.md',
    'description': 'Build a reviewer closeout summary from the archive governance closeout index.',
    'area': 'portfolio',
    'outputs': [
        'archive_governance_final_closeout_summary.json',
        'ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_SUMMARY.md',
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
    parser = argparse.ArgumentParser(description='Closeout summary command helper for OpenMontage Plus archive governance')
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
