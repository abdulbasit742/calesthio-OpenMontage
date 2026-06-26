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


def render_command(command):
    return ' '.join(f'"{part}"' if ' ' in part else part for part in command)


def completion_command(project):
    return [
        'python',
        'extras/archive_completion_report.py',
        '--project',
        str(project),
        '--out-json',
        f'{project}/archive_completion_report.json',
        '--out-md',
        f'{project}/ARCHIVE_COMPLETION_REPORT.md',
    ]


def board_command(projects_root):
    return [
        'python',
        'extras/archive_completion_board.py',
        '--projects-root',
        str(projects_root),
        '--out-json',
        'archive_completion_board.json',
        '--out-md',
        'ARCHIVE_COMPLETION_BOARD.md',
    ]


def build_plan(projects_root):
    projects = discover_projects(projects_root)
    project_commands = [
        {
            'project': project.name,
            'project_path': str(project),
            'command': completion_command(project),
            'completion_json': str(project / 'archive_completion_report.json'),
            'completion_markdown': str(project / 'ARCHIVE_COMPLETION_REPORT.md'),
        }
        for project in projects
    ]
    return {
        'projects_root': str(projects_root),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'ready-to-run' if projects else 'no-projects-found',
        'project_count': len(projects),
        'project_commands': project_commands,
        'board_command': board_command(projects_root),
        'recommended_order': [
            'run closeout and archive manifest workflow first',
            'run archive_readiness_badge.py for each project',
            'run each archive completion report command',
            'run the archive completion board command',
            'review ARCHIVE_COMPLETION_BOARD.md',
        ],
    }


def render_markdown(plan):
    lines = [
        '# Archive Completion Plan',
        '',
        f"Generated UTC: {plan['generated_on_utc']}",
        f"Projects root: `{plan['projects_root']}`",
        f"Status: **{plan['status']}**",
        f"Projects: **{plan['project_count']}**",
        '',
        '## Project Completion Commands',
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
        '## Refresh Archive Completion Board',
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
    parser = argparse.ArgumentParser(description='Build safe archive completion commands for every OpenMontage Plus project')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_completion_plan.json')
    parser.add_argument('--out-md', default='ARCHIVE_COMPLETION_PLAN.md')
    args = parser.parse_args()

    plan = build_plan(args.projects_root)
    result = write_plan(plan, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
