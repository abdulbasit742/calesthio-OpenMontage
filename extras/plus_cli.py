#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

TOOLS = {
    'new-project': {
        'script': 'extras/project_starter.py',
        'example': 'python extras/project_starter.py --name Demo --duration 45 --platform youtube-shorts',
        'description': 'Create a structured project workspace',
    },
    'workspace': {
        'script': 'extras/workspace_manager.py',
        'example': 'python extras/workspace_manager.py summary',
        'description': 'List and summarize project workspaces',
    },
    'presets': {
        'script': 'extras/export_presets.py',
        'example': 'python extras/export_presets.py list',
        'description': 'Show or write platform export presets',
    },
    'budget': {
        'script': 'extras/budget_gate.py',
        'example': 'python extras/budget_gate.py --budget 2.00',
        'description': 'Approve or block a render plan by budget',
    },
    'history': {
        'script': 'extras/render_history.py',
        'example': 'python extras/render_history.py summary',
        'description': 'Track render events and cost history',
    },
    'review': {
        'script': 'extras/review_checklist.py',
        'example': 'python extras/review_checklist.py template',
        'description': 'Create or check a publish review checklist',
    },
    'local': {
        'script': 'extras/local_zero_cost.py',
        'example': 'python extras/local_zero_cost.py detect',
        'description': 'Prepare local zero-cost mode',
    },
}


def list_tools():
    rows = []
    for name, tool in TOOLS.items():
        rows.append({
            'name': name,
            'script': tool['script'],
            'description': tool['description'],
            'example': tool['example'],
            'exists': Path(tool['script']).exists(),
        })
    return rows


def run_tool(name, extra_args):
    if name not in TOOLS:
        raise SystemExit(f'Unknown tool: {name}')
    script = Path(TOOLS[name]['script'])
    if not script.exists():
        raise SystemExit(f'Tool script not found: {script}')
    command = [sys.executable, str(script)] + extra_args
    return subprocess.call(command)


def main():
    parser = argparse.ArgumentParser(description='OpenMontage Plus unified helper CLI')
    sub = parser.add_subparsers(dest='command', required=True)

    sub.add_parser('list', help='List all Plus helper tools')

    show_parser = sub.add_parser('show', help='Show one helper tool')
    show_parser.add_argument('tool')

    run_parser = sub.add_parser('run', help='Run one helper tool')
    run_parser.add_argument('tool')
    run_parser.add_argument('args', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.command == 'list':
        print(json.dumps(list_tools(), indent=2))
    elif args.command == 'show':
        if args.tool not in TOOLS:
            raise SystemExit(f'Unknown tool: {args.tool}')
        print(json.dumps(TOOLS[args.tool], indent=2))
    elif args.command == 'run':
        raise SystemExit(run_tool(args.tool, args.args))


if __name__ == '__main__':
    main()
