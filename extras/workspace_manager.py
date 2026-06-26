#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PROJECTS_DIR = Path('projects')


def read_manifest(project_dir):
    manifest = project_dir / 'production_manifest.json'
    if not manifest.exists():
        return {'name': project_dir.name, 'status': 'missing-manifest'}
    return json.loads(manifest.read_text())


def list_projects():
    PROJECTS_DIR.mkdir(exist_ok=True)
    rows = []
    for item in sorted(PROJECTS_DIR.iterdir()):
        if item.is_dir():
            data = read_manifest(item)
            rows.append({
                'folder': item.name,
                'name': data.get('name', item.name),
                'platform': data.get('platform', 'unknown'),
                'duration_seconds': data.get('duration_seconds', 0),
                'status': data.get('status', 'unknown'),
            })
    return rows


def main():
    parser = argparse.ArgumentParser(description='Manage OpenMontage Plus project workspaces')
    parser.add_argument('command', choices=['list', 'summary'])
    args = parser.parse_args()

    projects = list_projects()
    if args.command == 'list':
        print(json.dumps(projects, indent=2))
    elif args.command == 'summary':
        print(f'Total projects: {len(projects)}')
        for project in projects:
            print(f"- {project['name']} | {project['platform']} | {project['status']}")


if __name__ == '__main__':
    main()
