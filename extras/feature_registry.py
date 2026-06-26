#!/usr/bin/env python3
import argparse
import json

COMPLETED_FEATURES = [
    {'number': 1, 'name': 'Project overview dashboard foundation', 'area': 'planning'},
    {'number': 2, 'name': 'Workspace manager CLI', 'area': 'projects'},
    {'number': 3, 'name': 'Export presets system', 'area': 'exports'},
    {'number': 4, 'name': 'Budget approval gate', 'area': 'cost-control'},
    {'number': 5, 'name': 'Render history logger', 'area': 'history'},
    {'number': 6, 'name': 'Caption and thumbnail review checklist', 'area': 'quality'},
    {'number': 7, 'name': 'Local zero-cost mode', 'area': 'local'},
    {'number': 8, 'name': 'Unified Plus CLI launcher', 'area': 'cli'},
    {'number': 9, 'name': 'GitHub Actions smoke test', 'area': 'ci'},
    {'number': 10, 'name': 'Feature registry and roadmap tracker', 'area': 'roadmap'},
]

ROADMAP_THEMES = [
    'dashboard',
    'project-management',
    'render-pipeline',
    'quality-control',
    'export-automation',
    'budget-safety',
    'local-mode',
    'documentation',
    'ci-testing',
    'upstream-integration',
]


def planned_feature(number):
    theme = ROADMAP_THEMES[(number - 1) % len(ROADMAP_THEMES)]
    return {
        'number': number,
        'name': f'Planned {theme} improvement pass',
        'area': theme,
        'status': 'planned',
    }


def completed():
    return [dict(item, status='completed') for item in COMPLETED_FEATURES]


def roadmap(start, end):
    rows = []
    completed_map = {item['number']: dict(item, status='completed') for item in COMPLETED_FEATURES}
    for number in range(start, end + 1):
        rows.append(completed_map.get(number, planned_feature(number)))
    return rows


def main():
    parser = argparse.ArgumentParser(description='Track OpenMontage Plus feature passes')
    parser.add_argument('command', choices=['completed', 'next', 'roadmap'])
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=25)
    args = parser.parse_args()

    if args.command == 'completed':
        print(json.dumps(completed(), indent=2))
    elif args.command == 'next':
        next_number = max(item['number'] for item in COMPLETED_FEATURES) + 1
        print(json.dumps(planned_feature(next_number), indent=2))
    elif args.command == 'roadmap':
        if args.start < 1 or args.end < args.start:
            raise SystemExit('Invalid roadmap range')
        print(json.dumps(roadmap(args.start, args.end), indent=2))


if __name__ == '__main__':
    main()
