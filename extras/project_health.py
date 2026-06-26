#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

REQUIRED_FILES = {
    'production_manifest': 'production_manifest.json',
    'export_preset': 'export_preset.json',
    'review_checklist': 'review_checklist.json',
    'local_zero_cost': 'local_zero_cost.json',
}

REQUIRED_DIRS = {
    'assets': 'assets',
    'scripts': 'scripts',
    'renders': 'renders',
    'exports': 'exports',
    'reviews': 'reviews',
}


def exists(base, relative):
    return (Path(base) / relative).exists()


def audit_project(project):
    project_path = Path(project)
    file_checks = {
        name: exists(project_path, relative)
        for name, relative in REQUIRED_FILES.items()
    }
    dir_checks = {
        name: exists(project_path, relative)
        for name, relative in REQUIRED_DIRS.items()
    }

    checks = {**file_checks, **dir_checks}
    passed = len([value for value in checks.values() if value])
    total = len(checks)
    score = 0 if total == 0 else round((passed / total) * 100, 2)

    missing = [name for name, ok in checks.items() if not ok]
    return {
        'project': str(project_path),
        'exists': project_path.exists(),
        'score_percent': score,
        'passed_checks': passed,
        'total_checks': total,
        'status': 'healthy' if score == 100 else 'needs-attention',
        'files': file_checks,
        'directories': dir_checks,
        'missing': missing,
    }


def audit_all(projects_root):
    root = Path(projects_root)
    root.mkdir(exist_ok=True)
    projects = [audit_project(item) for item in sorted(root.iterdir()) if item.is_dir()]
    average = 0 if not projects else round(sum(item['score_percent'] for item in projects) / len(projects), 2)
    return {
        'projects_root': str(root),
        'project_count': len(projects),
        'average_score_percent': average,
        'projects': projects,
    }


def main():
    parser = argparse.ArgumentParser(description='Audit OpenMontage Plus project health')
    parser.add_argument('command', choices=['project', 'all'])
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out')
    args = parser.parse_args()

    data = audit_project(args.project) if args.command == 'project' else audit_all(args.projects_root)
    if args.out:
        Path(args.out).write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
