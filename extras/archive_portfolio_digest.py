#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_PATHS = {
    'dashboard': 'archive_portfolio_dashboard.json',
    'summary': 'archive_portfolio_summary.json',
    'packlist': 'archive_portfolio_packlist.json',
    'index': 'archive_portfolio_index.json',
}

OK_STATUSES = {'ready', 'complete', 'archive-ready', 'available', 'ready-to-run'}


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json', 'path': str(file_path)}


def get_status(data):
    if not isinstance(data, dict):
        return 'missing'
    return data.get('status') or data.get('overall_status') or data.get('portfolio_status') or 'available'


def count_from(data, keys):
    if not isinstance(data, dict):
        return 0
    for key in keys:
        value = data.get(key)
        if isinstance(value, int):
            return value
    return 0


def collect_next_steps(*sources):
    steps = []
    for source in sources:
        if isinstance(source, dict):
            for item in source.get('next_steps', [])[:5]:
                if item not in steps:
                    steps.append(item)
    if not steps:
        steps.append('No blocking next steps reported by portfolio sources.')
    return steps[:10]


def build_digest(projects_root='projects'):
    data = {name: load_json(path) for name, path in SOURCE_PATHS.items()}
    source_rows = []
    for name, path in SOURCE_PATHS.items():
        source = data[name]
        source_rows.append({
            'name': name,
            'path': path,
            'exists': Path(path).exists(),
            'status': get_status(source),
            'missing_count': count_from(source, ['missing_count', 'missing_source_count', 'reported_missing_items']),
            'project_count': count_from(source, ['project_count', 'projects_count']),
        })

    missing_sources = [row for row in source_rows if not row['exists']]
    needs_attention = [row for row in source_rows if row['status'] not in OK_STATUSES]
    reported_missing = sum(row['missing_count'] for row in source_rows)
    project_count = max([row['project_count'] for row in source_rows] + [0])

    if missing_sources:
        headline = 'Archive portfolio digest needs source generation.'
    elif needs_attention or reported_missing:
        headline = 'Archive portfolio digest needs review.'
    else:
        headline = 'Archive portfolio digest is ready for executive review.'

    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'status': 'ready' if not missing_sources and not needs_attention and reported_missing == 0 else 'needs-attention',
        'headline': headline,
        'project_count': project_count,
        'source_count': len(source_rows),
        'missing_source_count': len(missing_sources),
        'attention_source_count': len(needs_attention),
        'reported_missing_items': reported_missing,
        'sources': source_rows,
        'executive_next_steps': collect_next_steps(data.get('dashboard'), data.get('summary'), data.get('packlist'), data.get('index')),
    }


def render_markdown(digest):
    lines = [
        '# Archive Portfolio Executive Digest',
        '',
        f"Generated UTC: {digest['generated_on_utc']}",
        f"Projects root: `{digest['projects_root']}`",
        f"Status: **{digest['status']}**",
        '',
        f"**Headline:** {digest['headline']}",
        '',
        '## Executive Metrics',
        f"- Projects: **{digest['project_count']}**",
        f"- Sources checked: **{digest['source_count']}**",
        f"- Missing sources: **{digest['missing_source_count']}**",
        f"- Attention sources: **{digest['attention_source_count']}**",
        f"- Reported missing items: **{digest['reported_missing_items']}**",
        '',
        '## Source Snapshot',
        '| Source | Exists | Status | Missing Items | Projects | Path |',
        '| --- | --- | --- | ---: | ---: | --- |',
    ]
    for row in digest['sources']:
        lines.append(
            f"| {row['name']} | {row['exists']} | {row['status']} | {row['missing_count']} | {row['project_count']} | `{row['path']}` |"
        )

    lines.extend(['', '## Executive Next Steps'])
    for step in digest['executive_next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_digest(projects_root, out_json, out_md):
    digest = build_digest(projects_root)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(digest, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(digest), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': digest['status']}


def main():
    parser = argparse.ArgumentParser(description='Build an executive archive portfolio digest for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_portfolio_digest.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_DIGEST.md')
    args = parser.parse_args()

    result = write_digest(args.projects_root, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
