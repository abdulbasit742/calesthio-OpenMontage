#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

from project_bootstrapper import bootstrap_project

SAMPLE_PROJECTS = [
    {
        'name': 'AI Launch Demo',
        'platform': 'youtube-shorts',
        'duration': 45,
        'topic': 'AI product launch',
        'audience': 'startup founders',
    },
    {
        'name': 'Founder Story Reel',
        'platform': 'instagram-reels',
        'duration': 60,
        'topic': 'founder story',
        'audience': 'early customers',
    },
]


def read_csv(path):
    with Path(path).open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def read_json(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data, dict):
        data = data.get('projects', [])
    if not isinstance(data, list):
        raise SystemExit('JSON input must be a list or an object with a projects list')
    return data


def normalize_project(row):
    name = str(row.get('name') or row.get('project') or '').strip()
    if not name:
        raise SystemExit('Each project needs a name field')
    return {
        'name': name,
        'platform': str(row.get('platform') or 'youtube-shorts').strip(),
        'duration': int(float(row.get('duration') or row.get('duration_seconds') or 45)),
        'topic': str(row.get('topic') or name).strip(),
        'audience': str(row.get('audience') or 'social media audience').strip(),
    }


def create_sample(path, file_format):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    if file_format == 'csv':
        with output.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=['name', 'platform', 'duration', 'topic', 'audience'])
            writer.writeheader()
            writer.writerows(SAMPLE_PROJECTS)
    else:
        output.write_text(json.dumps({'projects': SAMPLE_PROJECTS}, indent=2), encoding='utf-8')
    return str(output)


def load_projects(input_path):
    path = Path(input_path)
    if not path.exists():
        raise SystemExit(f'Input file not found: {path}')
    if path.suffix.lower() == '.csv':
        rows = read_csv(path)
    elif path.suffix.lower() == '.json':
        rows = read_json(path)
    else:
        raise SystemExit('Input file must be .csv or .json')
    return [normalize_project(row) for row in rows]


def batch_create(input_path, root, overwrite):
    projects = load_projects(input_path)
    results = []
    for project in projects:
        result = bootstrap_project(
            name=project['name'],
            platform=project['platform'],
            duration=project['duration'],
            topic=project['topic'],
            audience=project['audience'],
            root=root,
            overwrite=overwrite,
        )
        results.append({'input': project, 'result': result})
    return {
        'input': str(input_path),
        'root': root,
        'created_count': len(results),
        'projects': results,
    }


def main():
    parser = argparse.ArgumentParser(description='Batch-create OpenMontage Plus project workspaces from CSV or JSON')
    subparsers = parser.add_subparsers(dest='command', required=True)

    sample_parser = subparsers.add_parser('sample')
    sample_parser.add_argument('--format', choices=['csv', 'json'], default='csv')
    sample_parser.add_argument('--out', default='batch_projects.csv')

    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('--input', required=True)
    create_parser.add_argument('--root', default='projects')
    create_parser.add_argument('--overwrite', action='store_true')
    create_parser.add_argument('--out', default='batch_create_report.json')

    args = parser.parse_args()
    if args.command == 'sample':
        path = create_sample(args.out, args.format)
        print(json.dumps({'sample_file': path}, indent=2))
        return

    report = batch_create(args.input, args.root, args.overwrite)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
