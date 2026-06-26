#!/usr/bin/env python3
import argparse
import json

FEATURES = [
    {'number': 1, 'name': 'Project overview dashboard foundation', 'area': 'planning', 'status': 'completed'},
    {'number': 2, 'name': 'Workspace manager CLI', 'area': 'projects', 'status': 'completed'},
    {'number': 3, 'name': 'Export presets system', 'area': 'exports', 'status': 'completed'},
    {'number': 4, 'name': 'Budget approval gate', 'area': 'cost-control', 'status': 'completed'},
    {'number': 5, 'name': 'Render history logger', 'area': 'history', 'status': 'completed'},
    {'number': 6, 'name': 'Caption and thumbnail review checklist', 'area': 'quality', 'status': 'completed'},
    {'number': 7, 'name': 'Local zero-cost mode', 'area': 'local', 'status': 'completed'},
    {'number': 8, 'name': 'Unified Plus CLI launcher', 'area': 'cli', 'status': 'completed'},
    {'number': 9, 'name': 'GitHub Actions smoke test', 'area': 'ci', 'status': 'completed'},
    {'number': 10, 'name': 'Feature registry and roadmap tracker', 'area': 'roadmap', 'status': 'completed'},
    {'number': 11, 'name': 'Dashboard data generator', 'area': 'dashboard', 'status': 'completed'},
    {'number': 12, 'name': 'Project health scanner', 'area': 'quality', 'status': 'completed'},
    {'number': 13, 'name': 'Render plan builder', 'area': 'render-pipeline', 'status': 'completed'},
    {'number': 14, 'name': 'Metadata pack builder', 'area': 'publishing', 'status': 'completed'},
    {'number': 15, 'name': 'Caption builder', 'area': 'captions', 'status': 'completed'},
    {'number': 16, 'name': 'Thumbnail brief generator', 'area': 'creative', 'status': 'completed'},
    {'number': 17, 'name': 'Shotlist planner', 'area': 'creative', 'status': 'completed'},
    {'number': 18, 'name': 'Script timing analyzer', 'area': 'script', 'status': 'completed'},
    {'number': 19, 'name': 'Asset auditor', 'area': 'assets', 'status': 'completed'},
    {'number': 20, 'name': 'Publish packager', 'area': 'publishing', 'status': 'completed'},
    {'number': 21, 'name': 'Project bootstrapper', 'area': 'projects', 'status': 'completed'},
    {'number': 22, 'name': 'Quality score calculator', 'area': 'quality', 'status': 'completed'},
    {'number': 23, 'name': 'Batch project creator', 'area': 'projects', 'status': 'completed'},
    {'number': 24, 'name': 'Copy variants builder', 'area': 'publishing', 'status': 'completed'},
    {'number': 25, 'name': 'Content calendar builder', 'area': 'calendar', 'status': 'completed'},
    {'number': 26, 'name': 'Brand kit generator and auditor', 'area': 'brand', 'status': 'completed'},
    {'number': 27, 'name': 'Release notes builder', 'area': 'documentation', 'status': 'completed'},
    {'number': 28, 'name': 'Pipeline runner', 'area': 'automation', 'status': 'completed'},
    {'number': 29, 'name': 'Platform publish validator', 'area': 'platform', 'status': 'completed'},
    {'number': 30, 'name': 'Project status board', 'area': 'dashboard', 'status': 'completed'},
    {'number': 31, 'name': 'Client handoff packet builder', 'area': 'handoff', 'status': 'completed'},
    {'number': 32, 'name': 'Delivery ZIP builder', 'area': 'delivery', 'status': 'completed'},
    {'number': 33, 'name': 'Delivery ZIP audit tool', 'area': 'delivery', 'status': 'completed'},
    {'number': 34, 'name': 'Client review checklist generator', 'area': 'review', 'status': 'completed'},
    {'number': 35, 'name': 'Client revision tracker', 'area': 'review', 'status': 'completed'},
    {'number': 36, 'name': 'Revision report generator', 'area': 'review', 'status': 'completed'},
    {'number': 37, 'name': 'Final approval gate', 'area': 'approval', 'status': 'completed'},
    {'number': 38, 'name': 'Publishing instructions builder', 'area': 'publishing', 'status': 'completed'},
    {'number': 39, 'name': 'SEO keyword planner issue logged', 'area': 'seo', 'status': 'issue-logged', 'issue': 2},
    {'number': 40, 'name': 'Feature registry refresh through feature 40', 'area': 'roadmap', 'status': 'completed'},
    {'number': 41, 'name': 'Roadmap report generator', 'area': 'roadmap', 'status': 'completed'},
    {'number': 42, 'name': 'Plus CLI expanded tool launcher', 'area': 'cli', 'status': 'completed'},
    {'number': 43, 'name': 'Plus toolchain guide', 'area': 'documentation', 'status': 'completed'},
    {'number': 44, 'name': 'Toolchain audit report generator', 'area': 'roadmap', 'status': 'completed'},
    {'number': 45, 'name': 'Toolchain audit CLI integration and registry sync', 'area': 'cli', 'status': 'completed'},
    {'number': 46, 'name': 'Content risk checker', 'area': 'review', 'status': 'completed'},
    {'number': 47, 'name': 'Content review CLI integration and registry sync', 'area': 'cli', 'status': 'completed'},
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


def all_features():
    return [dict(item) for item in FEATURES]


def completed():
    return [dict(item) for item in FEATURES if item.get('status') == 'completed']


def by_status(status):
    return [dict(item) for item in FEATURES if item.get('status') == status]


def next_feature():
    return planned_feature(max(item['number'] for item in FEATURES) + 1)


def summary():
    counts = {}
    for item in FEATURES:
        counts[item['status']] = counts.get(item['status'], 0) + 1
    return {
        'tracked_features': len(FEATURES),
        'latest_tracked_number': max(item['number'] for item in FEATURES),
        'status_counts': counts,
        'next': next_feature(),
    }


def roadmap(start, end):
    rows = []
    feature_map = {item['number']: dict(item) for item in FEATURES}
    for number in range(start, end + 1):
        rows.append(feature_map.get(number, planned_feature(number)))
    return rows


def main():
    parser = argparse.ArgumentParser(description='Track OpenMontage Plus feature passes')
    parser.add_argument('command', choices=['all', 'completed', 'issue-logged', 'next', 'summary', 'roadmap'])
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=50)
    args = parser.parse_args()

    if args.command == 'all':
        result = all_features()
    elif args.command == 'completed':
        result = completed()
    elif args.command == 'issue-logged':
        result = by_status('issue-logged')
    elif args.command == 'next':
        result = next_feature()
    elif args.command == 'summary':
        result = summary()
    else:
        if args.start < 1 or args.end < args.start:
            raise SystemExit('Invalid roadmap range')
        result = roadmap(args.start, args.end)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
