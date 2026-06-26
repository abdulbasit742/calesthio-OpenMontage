#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_FILES = {
    'summary': 'archive_portfolio_summary.json',
    'packlist': 'archive_portfolio_packlist.json',
    'index': 'archive_portfolio_index.json',
    'status_board': 'archive_status_board.json',
    'badge_board': 'archive_badge_board.json',
    'completion_board': 'archive_completion_board.json',
    'toolchain_audit': 'archive_toolchain_audit.json',
}


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json', 'path': str(file_path)}


def status_of(data):
    if not data:
        return 'missing'
    return data.get('status') or data.get('overall_status') or data.get('portfolio_status') or 'available'


def count_value(data, keys):
    if not isinstance(data, dict):
        return 0
    for key in keys:
        if isinstance(data.get(key), int):
            return data[key]
    return 0


def build_card(name, path, data):
    return {
        'name': name,
        'path': path,
        'exists': Path(path).exists(),
        'status': status_of(data),
        'missing_count': count_value(data, ['missing_count', 'portfolio_missing_count', 'project_missing_file_count', 'missing_file_count']),
        'project_count': count_value(data, ['project_count', 'projects_count']),
    }


def build_dashboard(projects_root='projects'):
    sources = {name: load_json(path) for name, path in SOURCE_FILES.items()}
    cards = [build_card(name, SOURCE_FILES[name], sources[name]) for name in SOURCE_FILES]
    missing_sources = [card for card in cards if not card['exists']]
    attention_cards = [card for card in cards if card['status'] not in {'ready', 'complete', 'archive-ready', 'available', 'ready-to-run'}]
    total_missing = sum(card['missing_count'] for card in cards)
    status = 'ready' if not missing_sources and not attention_cards and total_missing == 0 else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'status': status,
        'source_count': len(cards),
        'missing_source_count': len(missing_sources),
        'attention_count': len(attention_cards),
        'reported_missing_items': total_missing,
        'cards': cards,
        'next_steps': next_steps(missing_sources, attention_cards, total_missing),
    }


def next_steps(missing_sources, attention_cards, total_missing):
    steps = []
    for card in missing_sources:
        steps.append(f"Generate missing source: {card['path']}")
    for card in attention_cards:
        if card['exists']:
            steps.append(f"Review {card['name']} status: {card['status']}")
    if total_missing:
        steps.append(f"Resolve reported missing items: {total_missing}")
    if not steps:
        steps.append('Archive portfolio dashboard is ready.')
    return steps


def render_markdown(dashboard):
    lines = [
        '# Archive Portfolio Dashboard',
        '',
        f"Generated UTC: {dashboard['generated_on_utc']}",
        f"Projects root: `{dashboard['projects_root']}`",
        f"Status: **{dashboard['status']}**",
        f"Sources: **{dashboard['source_count']}**",
        f"Missing sources: **{dashboard['missing_source_count']}**",
        f"Attention cards: **{dashboard['attention_count']}**",
        f"Reported missing items: **{dashboard['reported_missing_items']}**",
        '',
        '## Status Cards',
        '| Source | Exists | Status | Missing Items | Projects | Path |',
        '| --- | --- | --- | ---: | ---: | --- |',
    ]
    for card in dashboard['cards']:
        lines.append(
            f"| {card['name']} | {card['exists']} | {card['status']} | {card['missing_count']} | {card['project_count']} | `{card['path']}` |"
        )
    lines.extend(['', '## Next Steps'])
    for step in dashboard['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_dashboard(projects_root, out_json, out_md):
    dashboard = build_dashboard(projects_root)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(dashboard, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(dashboard), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': dashboard['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a one-page archive portfolio dashboard for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--out-json', default='archive_portfolio_dashboard.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_DASHBOARD.md')
    args = parser.parse_args()

    result = write_dashboard(args.projects_root, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
