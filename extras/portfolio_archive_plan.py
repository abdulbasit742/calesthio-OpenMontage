#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def discover_projects(projects_root):
    root = Path(projects_root)
    if not root.exists():
        return []
    return sorted([item for item in root.iterdir() if item.is_dir()], key=lambda item: item.name.lower())


def build_project_command(project, client_name, sender_name):
    command = [
        'python',
        'extras/archive_ops_runner.py',
        '--project',
        str(project),
        '--out-json',
        f'{project}/archive_ops_report.json',
        '--out-md',
        f'{project}/ARCHIVE_OPS_REPORT.md',
    ]
    if client_name:
        command.extend(['--client-name', client_name])
    if sender_name:
        command.extend(['--sender-name', sender_name])
    return command


def build_plan(projects_root, client_name='', sender_name=''):
    projects = discover_projects(projects_root)
    project_commands = [
        {
            'project': project.name,
            'project_path': str(project),
            'command': build_project_command(project, client_name, sender_name),
            'archive_manifest': str(project / 'project_archive_manifest.json'),
            'archive_ops_report': str(project / 'archive_ops_report.json'),
        }
        for project in projects
    ]
    board_command = [
        'python',
        'extras/archive_status_board.py',
        '--projects-root',
        str(projects_root),
        '--out-json',
        'archive_status_board.json',
        '--out-md',
        'ARCHIVE_STATUS_BOARD.md',
    ]
    return {
        'projects_root': str(projects_root),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'ready-to-run' if projects else 'no-projects-found',
        'project_count': len(projects),
        'project_commands': project_commands,
        'board_command': board_command,
        'recommended_order': ['run each project command', 'run board command', 'review ARCHIVE_STATUS_BOARD.md'],
    }


def render_command(command):
    return ' '.join(f'"{part}"' if ' ' in part else part for part in command)


def render_markdown(plan):
    lines = [
        '# Portfolio Archive Plan',
        '',
        f"Generated UTC: {plan['generated_on_utc']}",
        f"Projects root: `{plan['projects_root']}`",
        f"Status: **{plan['status']}**",
        f"Projects: **{plan['project_count']}**",
        '',
        '## Project Archive Commands',
    ]
    if plan['project_commands']:
        for item in plan['project_commands']:
            lines.extend([
                '',
                f"### {item['project']}",
                '```bash',
                render_command(item['command']),
                '```',
            ])
    else:
        lines.append('- No project folders found.')
    lines.extend([
        '',
        '## Refresh Archive Status Board',
        '```bash',
        render_command(plan['board_command']),
        '```',
        '',
        '## Recommended Order',
    ])
    for step in plan['recommended_order']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_plan(plan, out_json, out_md):
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(plan, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(plan), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': plan['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a safe portfolio archive command plan for OpenMontage Plus projects')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--client-name', default='')
    parser.add_argument('--sender-name', default='')
    parser.add_argument('--out-json', default='portfolio_archive_plan.json')
    parser.add_argument('--out-md', default='PORTFOLIO_ARCHIVE_PLAN.md')
    args = parser.parse_args()

    plan = build_plan(args.projects_root, client_name=args.client_name, sender_name=args.sender_name)
    result = write_plan(plan, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
