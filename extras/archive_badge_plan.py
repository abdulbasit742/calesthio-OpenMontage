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


def badge_command(project):
    return [
        'python',
        'extras/archive_readiness_badge.py',
        '--project',
        str(project),
        '--out-json',
        f'{project}/archive_readiness_badge.json',
        '--out-md',
        f'{project}/ARCHIVE_READINESS_BADGE.md',
    ]


def board_command(projects_root):
    return [
        'python',
        'extras/archive_badge_board.py',
        '--projects-root',
        str(projects_root),
        '--out-json',
        'archive_badge_board.json',
        '--out-md',
        'ARCHIVE_BADGE_BOARD.md',
    ]


def build_plan(projects_root):
    projects = discover_projects(projects_root)
    project_commands = [
        {
            'project': project.name,
            'project_path': str(project),
            'command': badge_command(project),
            'badge_json': str(project / 'archive_readiness_badge.json'),
            'badge_markdown': str(project / 'ARCHIVE_READINESS_BADGE.md'),
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
            'run project_archive_manifest.py for each project if manifest is missing',
            'run each badge command',
            'run the badge board command',
            'review ARCHIVE_BADGE_BOARD.md',
        ],
    }


def render_markdown(plan):
    lines = [
        '# Archive Badge Plan',
        '',
        f"Generated UTC: {plan['generated_on_utc']}",
        f"Projects root: `{plan['projects_root']}`",
        f"Status: **{plan['status']}**",
        f"Projects: **{plan['project_count']}**",
        '',
        '## Project Badge Commands',
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
        '## Refresh Archive Badge Board',
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
    parser = argparse.ArgumentParser(description='Build safe archive readiness badge commands for every OpenMontage Plus project')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_badge_plan.json')
    parser.add_argument('--out-md', default='ARCHIVE_BADGE_PLAN.md')
    args = parser.parse_args()

    plan = build_plan(args.projects_root)
    result = write_plan(plan, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
