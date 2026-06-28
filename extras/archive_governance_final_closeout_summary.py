#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def read_index(path_text):
    path = Path(path_text)
    if not path.exists():
        return {'load_status': 'missing', 'path': path_text, 'data': {}}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'load_status': 'invalid-json', 'path': path_text, 'data': {}}
    return {'load_status': 'loaded', 'path': path_text, 'data': data if isinstance(data, dict) else {}}


def build_summary(index_path, title, owner):
    loaded = read_index(index_path)
    data = loaded['data']
    items = data.get('items', []) if isinstance(data.get('items', []), list) else []
    existing_items = [item for item in items if item.get('exists')]
    required_items = [item for item in items if item.get('required')]
    missing_required = data.get('missing_required', []) if isinstance(data.get('missing_required', []), list) else []
    invalid_json = data.get('invalid_json', []) if isinstance(data.get('invalid_json', []), list) else []
    ready = loaded['load_status'] == 'loaded' and data.get('index_status') == 'closeout-ready'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'title': title,
        'owner': owner,
        'summary_status': 'complete' if ready else 'needs-attention',
        'index_path': index_path,
        'index_load_status': loaded['load_status'],
        'index_status': data.get('index_status'),
        'closure_closed': data.get('closure_closed'),
        'total_items': len(items),
        'required_items': len(required_items),
        'existing_items': len(existing_items),
        'missing_required_count': len(missing_required),
        'invalid_json_count': len(invalid_json),
        'missing_required': missing_required,
        'invalid_json': invalid_json,
        'executive_note': executive_note(ready, data.get('index_status'), missing_required, invalid_json),
        'next_steps': next_steps(ready, loaded['load_status'], data.get('index_status'), missing_required, invalid_json),
    }


def executive_note(ready, index_status, missing_required, invalid_json):
    if ready:
        return 'Final archive governance package is indexed and ready for closeout review.'
    if missing_required:
        return 'Final archive governance package is not complete because required files are missing.'
    if invalid_json:
        return 'Final archive governance package needs JSON repair before closeout review.'
    return f'Final archive governance package requires attention; index status is {index_status!r}.'


def next_steps(ready, load_status, index_status, missing_required, invalid_json):
    if ready:
        return [
            'Attach this summary to the final archive package.',
            'Use it as the executive-level closeout note for reviewers.',
        ]
    if load_status != 'loaded':
        return ['Generate the final closeout index before building this summary.']
    steps = []
    if missing_required:
        steps.append('Add all missing required files listed in the closeout index.')
    if invalid_json:
        steps.append('Regenerate invalid JSON files listed in the closeout index.')
    if index_status != 'closeout-ready':
        steps.append('Rerun the closeout index builder until status is closeout-ready.')
    return steps or ['Review closeout summary inputs and rerun the builder.']


def render_markdown(summary):
    lines = [
        '# Archive Governance Final Closeout Summary',
        '',
        f"Generated UTC: {summary['generated_on_utc']}",
        f"Title: **{summary['title']}**",
        f"Owner: **{summary['owner']}**",
        f"Summary status: **{summary['summary_status']}**",
        f"Index source: `{summary['index_path']}`",
        f"Index load status: **{summary['index_load_status']}**",
        f"Index status: **{summary['index_status']}**",
        f"Closure closed: **{summary['closure_closed']}**",
        '',
        '## Counts',
        '',
        f"- Total indexed items: {summary['total_items']}",
        f"- Required items: {summary['required_items']}",
        f"- Existing items: {summary['existing_items']}",
        f"- Missing required count: {summary['missing_required_count']}",
        f"- Invalid JSON count: {summary['invalid_json_count']}",
        '',
        '## Executive Note',
        summary['executive_note'],
        '',
        '## Missing Required Files',
    ]
    if summary['missing_required']:
        for path in summary['missing_required']:
            lines.append(f'- `{path}`')
    else:
        lines.append('- None')
    lines.extend(['', '## Invalid JSON Files'])
    if summary['invalid_json']:
        for path in summary['invalid_json']:
            lines.append(f'- `{path}`')
    else:
        lines.append('- None')
    lines.extend(['', '## Next Steps'])
    for step in summary['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_summary(index, title, owner, out_json, out_md):
    summary = build_summary(index, title, owner)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(summary), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': summary['summary_status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance closeout summary')
    parser.add_argument('--index', default='archive_governance_final_closeout_index.json')
    parser.add_argument('--title', default='Archive Governance Final Closeout Summary')
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--out-json', default='archive_governance_final_closeout_summary.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_FINAL_CLOSEOUT_SUMMARY.md')
    args = parser.parse_args()

    result = write_summary(args.index, args.title, args.owner, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
