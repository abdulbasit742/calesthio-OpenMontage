#!/usr/bin/env python3
import argparse
import csv
import json
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_TIME_BY_PLATFORM = {
    'youtube-shorts': '18:00',
    'instagram-reels': '19:00',
    'tiktok': '20:00',
    'youtube': '17:00',
    'linkedin': '10:00',
    'square-feed': '18:30',
}

CALENDAR_FIELDS = [
    'publish_date',
    'publish_time',
    'project',
    'project_folder',
    'platform',
    'title',
    'status',
    'quality_score',
    'caption_file',
    'metadata_file',
    'publish_package',
    'notes',
]


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def parse_start_date(value):
    if value:
        return datetime.strptime(value, '%Y-%m-%d').date()
    return date.today()


def discover_projects(root):
    root_path = Path(root)
    if not root_path.exists():
        return []
    projects = []
    for item in sorted(root_path.iterdir()):
        if item.is_dir() and (item / 'production_manifest.json').exists():
            projects.append(item)
    return projects


def project_calendar_row(project_dir, publish_day):
    manifest = load_json(project_dir / 'production_manifest.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    quality = load_json(project_dir / 'quality_score.json', {})
    publish_manifest = load_json(project_dir / 'publish' / 'publish_manifest.json', {})

    platform = metadata.get('platform') or manifest.get('platform') or 'youtube-shorts'
    title = metadata.get('title') or manifest.get('name') or project_dir.name
    quality_score = quality.get('final_score_percent', '')
    status = quality.get('status') or publish_manifest.get('status') or manifest.get('status', 'draft')

    caption_file = ''
    for candidate in ['captions/final.srt', 'captions/final.vtt', 'exports/final.srt', 'exports/final.vtt']:
        if (project_dir / candidate).exists():
            caption_file = str(project_dir / candidate)
            break

    return {
        'publish_date': publish_day.isoformat(),
        'publish_time': DEFAULT_TIME_BY_PLATFORM.get(platform, '18:00'),
        'project': manifest.get('name', project_dir.name),
        'project_folder': str(project_dir),
        'platform': platform,
        'title': title,
        'status': status,
        'quality_score': quality_score,
        'caption_file': caption_file,
        'metadata_file': str(project_dir / 'metadata_pack.json') if (project_dir / 'metadata_pack.json').exists() else '',
        'publish_package': str(project_dir / 'publish') if (project_dir / 'publish').exists() else '',
        'notes': 'Review status and assets before publishing.',
    }


def build_calendar(projects_root, start_date, every_days):
    projects = discover_projects(projects_root)
    first_day = parse_start_date(start_date)
    rows = []
    for index, project_dir in enumerate(projects):
        publish_day = first_day + timedelta(days=index * every_days)
        rows.append(project_calendar_row(project_dir, publish_day))
    return {
        'projects_root': str(projects_root),
        'start_date': first_day.isoformat(),
        'cadence_days': every_days,
        'item_count': len(rows),
        'calendar': rows,
    }


def write_csv(path, rows):
    with Path(path).open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=CALENDAR_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description='Build a publish content calendar from OpenMontage Plus projects')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--start-date', help='YYYY-MM-DD. Defaults to today.')
    parser.add_argument('--every-days', type=int, default=1)
    parser.add_argument('--out-json', default='content_calendar.json')
    parser.add_argument('--out-csv', default='content_calendar.csv')
    args = parser.parse_args()

    calendar = build_calendar(args.projects_root, args.start_date, max(1, args.every_days))
    Path(args.out_json).write_text(json.dumps(calendar, indent=2), encoding='utf-8')
    write_csv(args.out_csv, calendar['calendar'])
    print(json.dumps(calendar, indent=2))


if __name__ == '__main__':
    main()
