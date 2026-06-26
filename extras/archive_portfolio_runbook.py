#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

RUNBOOK_STEPS = [
    {
        'name': 'toolchain-audit',
        'command': ['python', 'extras/archive_toolchain_audit.py', '--out-json', 'archive_toolchain_audit.json', '--out-md', 'ARCHIVE_TOOLCHAIN_AUDIT.md'],
        'output': 'ARCHIVE_TOOLCHAIN_AUDIT.md',
        'purpose': 'Confirm archive toolchain files and guide are present.',
    },
    {
        'name': 'portfolio-archive-plan',
        'command': ['python', 'extras/portfolio_archive_plan.py', '--projects-root', '{projects_root}', '--client-name', '{client_name}', '--sender-name', '{sender_name}', '--out-json', 'portfolio_archive_plan.json', '--out-md', 'PORTFOLIO_ARCHIVE_PLAN.md'],
        'output': 'PORTFOLIO_ARCHIVE_PLAN.md',
        'purpose': 'Generate safe per-project archive ops commands.',
    },
    {
        'name': 'archive-status-board',
        'command': ['python', 'extras/archive_status_board.py', '--projects-root', '{projects_root}', '--out-json', 'archive_status_board.json', '--out-md', 'ARCHIVE_STATUS_BOARD.md'],
        'output': 'ARCHIVE_STATUS_BOARD.md',
        'purpose': 'Refresh global archive readiness status board.',
    },
    {
        'name': 'archive-badge-plan',
        'command': ['python', 'extras/archive_badge_plan.py', '--projects-root', '{projects_root}', '--out-json', 'archive_badge_plan.json', '--out-md', 'ARCHIVE_BADGE_PLAN.md'],
        'output': 'ARCHIVE_BADGE_PLAN.md',
        'purpose': 'Generate safe per-project archive badge commands.',
    },
    {
        'name': 'archive-badge-board',
        'command': ['python', 'extras/archive_badge_board.py', '--projects-root', '{projects_root}', '--out-json', 'archive_badge_board.json', '--out-md', 'ARCHIVE_BADGE_BOARD.md'],
        'output': 'ARCHIVE_BADGE_BOARD.md',
        'purpose': 'Refresh global archive badge board.',
    },
    {
        'name': 'archive-completion-plan',
        'command': ['python', 'extras/archive_completion_plan.py', '--projects-root', '{projects_root}', '--out-json', 'archive_completion_plan.json', '--out-md', 'ARCHIVE_COMPLETION_PLAN.md'],
        'output': 'ARCHIVE_COMPLETION_PLAN.md',
        'purpose': 'Generate safe per-project archive completion commands.',
    },
    {
        'name': 'archive-completion-board',
        'command': ['python', 'extras/archive_completion_board.py', '--projects-root', '{projects_root}', '--out-json', 'archive_completion_board.json', '--out-md', 'ARCHIVE_COMPLETION_BOARD.md'],
        'output': 'ARCHIVE_COMPLETION_BOARD.md',
        'purpose': 'Refresh global archive completion board.',
    },
    {
        'name': 'portfolio-summary',
        'command': ['python', 'extras/archive_portfolio_summary.py', '--out-json', 'archive_portfolio_summary.json', '--out-md', 'ARCHIVE_PORTFOLIO_SUMMARY.md'],
        'output': 'ARCHIVE_PORTFOLIO_SUMMARY.md',
        'purpose': 'Build final portfolio archive summary from all boards.',
    },
    {
        'name': 'portfolio-packlist',
        'command': ['python', 'extras/archive_portfolio_packlist.py', '--projects-root', '{projects_root}', '--out-json', 'archive_portfolio_packlist.json', '--out-md', 'ARCHIVE_PORTFOLIO_PACKLIST.md'],
        'output': 'ARCHIVE_PORTFOLIO_PACKLIST.md',
        'purpose': 'Build the final portfolio and per-project archive file checklist.',
    },
    {
        'name': 'portfolio-index',
        'command': ['python', 'extras/archive_portfolio_index.py', '--projects-root', '{projects_root}', '--out-json', 'archive_portfolio_index.json', '--out-md', 'ARCHIVE_PORTFOLIO_INDEX.md'],
        'output': 'ARCHIVE_PORTFOLIO_INDEX.md',
        'purpose': 'Build the searchable final archive portfolio document index.',
    },
    {
        'name': 'portfolio-dashboard',
        'command': ['python', 'extras/archive_portfolio_dashboard.py', '--projects-root', '{projects_root}', '--out-json', 'archive_portfolio_dashboard.json', '--out-md', 'ARCHIVE_PORTFOLIO_DASHBOARD.md'],
        'output': 'ARCHIVE_PORTFOLIO_DASHBOARD.md',
        'purpose': 'Build the one-page final archive portfolio status dashboard.',
    },
    {
        'name': 'portfolio-digest',
        'command': ['python', 'extras/archive_portfolio_digest.py', '--projects-root', '{projects_root}', '--out-json', 'archive_portfolio_digest.json', '--out-md', 'ARCHIVE_PORTFOLIO_DIGEST.md'],
        'output': 'ARCHIVE_PORTFOLIO_DIGEST.md',
        'purpose': 'Build the executive archive portfolio digest for final review.',
    },
]


def fill_command(command, projects_root, client_name, sender_name):
    return [part.format(projects_root=projects_root, client_name=client_name, sender_name=sender_name) for part in command]


def render_command(command):
    return ' '.join(f'"{part}"' if ' ' in part else part for part in command)


def build_runbook(projects_root='projects', client_name='', sender_name=''):
    steps = []
    for index, step in enumerate(RUNBOOK_STEPS, start=1):
        command = fill_command(step['command'], projects_root, client_name, sender_name)
        steps.append({
            'order': index,
            'name': step['name'],
            'purpose': step['purpose'],
            'command': command,
            'output': step['output'],
        })
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': projects_root,
        'status': 'ready-to-run',
        'step_count': len(steps),
        'steps': steps,
        'final_outputs': [step['output'] for step in RUNBOOK_STEPS],
    }


def render_markdown(runbook):
    lines = [
        '# Archive Portfolio Runbook',
        '',
        f"Generated UTC: {runbook['generated_on_utc']}",
        f"Projects root: `{runbook['projects_root']}`",
        f"Status: **{runbook['status']}**",
        f"Steps: **{runbook['step_count']}**",
        '',
        '## Command Steps',
    ]
    for step in runbook['steps']:
        lines.extend([
            '',
            f"### {step['order']}. {step['name']}",
            f"Purpose: {step['purpose']}",
            f"Output: `{step['output']}`",
            '',
            '```bash',
            render_command(step['command']),
            '```',
        ])
    lines.extend(['', '## Final Outputs'])
    for output in runbook['final_outputs']:
        lines.append(f'- `{output}`')
    lines.append('')
    return '\n'.join(lines)


def write_runbook(runbook, out_json, out_md):
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(runbook, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(runbook), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': runbook['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a safe archive portfolio runbook for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--client-name', default='')
    parser.add_argument('--sender-name', default='')
    parser.add_argument('--out-json', default='archive_portfolio_runbook.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_RUNBOOK.md')
    args = parser.parse_args()

    runbook = build_runbook(args.projects_root, client_name=args.client_name, sender_name=args.sender_name)
    result = write_runbook(runbook, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
