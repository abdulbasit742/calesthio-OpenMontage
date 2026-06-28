#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path_text):
    path = Path(path_text)
    if not path.exists():
        return {'state': 'missing', 'data': {}}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'state': 'invalid-json', 'data': {}}
    return {'state': 'loaded', 'data': data if isinstance(data, dict) else {}}


def make_rollup(index_path, summary_path, label):
    index = load_json(index_path)
    summary = load_json(summary_path)
    index_data = index['data']
    summary_data = summary['data']
    ok = index_data.get('index_status') == 'closeout-ready' and summary_data.get('summary_status') == 'complete'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'rollup_status': 'ready' if ok else 'needs-attention',
        'index_path': index_path,
        'summary_path': summary_path,
        'index_load_state': index['state'],
        'summary_load_state': summary['state'],
        'index_status': index_data.get('index_status'),
        'summary_status': summary_data.get('summary_status'),
        'closure_closed': index_data.get('closure_closed'),
        'total_items': len(index_data.get('items', [])) if isinstance(index_data.get('items'), list) else summary_data.get('total_items', 0),
        'missing_required': index_data.get('missing_required', []),
        'invalid_json': index_data.get('invalid_json', []),
        'note': summary_data.get('executive_note', 'Closeout summary note is not available.'),
        'next_steps': steps(ok),
    }


def steps(ok):
    if ok:
        return ['Store the rollup with the archive package.', 'Use it as a quick review checkpoint.']
    return ['Repair the closeout index or summary, then rerun this rollup.']


def render_md(rollup):
    lines = [
        '# Archive Closeout Rollup',
        '',
        f"Generated UTC: {rollup['generated_on_utc']}",
        f"Label: **{rollup['label']}**",
        f"Rollup status: **{rollup['rollup_status']}**",
        f"Index path: `{rollup['index_path']}`",
        f"Summary path: `{rollup['summary_path']}`",
        '',
        '## Status',
        f"- Index load state: {rollup['index_load_state']}",
        f"- Summary load state: {rollup['summary_load_state']}",
        f"- Index status: {rollup['index_status']}",
        f"- Summary status: {rollup['summary_status']}",
        f"- Closure closed: {rollup['closure_closed']}",
        f"- Total items: {rollup['total_items']}",
        '',
        '## Note',
        rollup['note'],
        '',
        '## Missing Required Files',
    ]
    for item in rollup['missing_required'] or ['None']:
        lines.append(f'- `{item}`' if item != 'None' else '- None')
    lines.extend(['', '## Invalid JSON Files'])
    for item in rollup['invalid_json'] or ['None']:
        lines.append(f'- `{item}`' if item != 'None' else '- None')
    lines.extend(['', '## Next Steps'])
    for step in rollup['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_rollup(index, summary, label, out_json, out_md):
    rollup = make_rollup(index, summary, label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.write_text(json.dumps(rollup, indent=2), encoding='utf-8')
    md_path.write_text(render_md(rollup), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': rollup['rollup_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout rollup')
    parser.add_argument('--index', default='archive_governance_final_closeout_index.json')
    parser.add_argument('--summary', default='archive_governance_final_closeout_summary.json')
    parser.add_argument('--label', default='archive-closeout-rollup')
    parser.add_argument('--out-json', default='archive_closeout_rollup.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_ROLLUP.md')
    args = parser.parse_args()
    print(json.dumps(write_rollup(args.index, args.summary, args.label, args.out_json, args.out_md), indent=2))


if __name__ == '__main__':
    main()
