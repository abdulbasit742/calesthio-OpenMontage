#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from datetime import date
from pathlib import Path


def load_registry():
    from feature_registry import roadmap, summary
    return roadmap, summary


def build_report(start, end):
    roadmap_func, summary_func = load_registry()
    rows = roadmap_func(start, end)
    counts = Counter(item.get('status', 'unknown') for item in rows)
    areas = Counter(item.get('area', 'unknown') for item in rows)
    return {
        'generated_on': date.today().isoformat(),
        'range': {'start': start, 'end': end},
        'registry_summary': summary_func(),
        'range_summary': {
            'total': len(rows),
            'status_counts': dict(counts),
            'area_counts': dict(areas),
        },
        'features': rows,
    }


def render_markdown(report):
    lines = [
        '# OpenMontage Plus Roadmap Report',
        '',
        f"Generated: {report['generated_on']}",
        f"Range: {report['range']['start']} to {report['range']['end']}",
        '',
        '## Registry Summary',
        f"- Tracked features: {report['registry_summary']['tracked_features']}",
        f"- Latest tracked number: {report['registry_summary']['latest_tracked_number']}",
        f"- Next planned feature: {report['registry_summary']['next']['number']} — {report['registry_summary']['next']['name']}",
        '',
        '## Range Summary',
    ]
    for status, count in sorted(report['range_summary']['status_counts'].items()):
        lines.append(f'- {status}: {count}')
    lines.extend([
        '',
        '## Features',
        '| Number | Name | Area | Status |',
        '| --- | --- | --- | --- |',
    ])
    for item in report['features']:
        lines.append(f"| {item['number']} | {item['name']} | {item['area']} | {item['status']} |")
    lines.append('')
    return '\n'.join(lines)


def write_report(start, end, out_json, out_md):
    report = build_report(start, end)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'range_summary': report['range_summary']}


def main():
    parser = argparse.ArgumentParser(description='Generate a roadmap report from the OpenMontage Plus feature registry')
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=50)
    parser.add_argument('--out-json', default='roadmap_report.json')
    parser.add_argument('--out-md', default='ROADMAP_REPORT.md')
    args = parser.parse_args()

    if args.start < 1 or args.end < args.start:
        raise SystemExit('Invalid roadmap range')
    result = write_report(args.start, args.end, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
