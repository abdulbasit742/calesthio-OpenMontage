#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_rollup(path_text):
    path = Path(path_text)
    if not path.exists():
        return {'state': 'missing', 'data': {}}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'state': 'invalid-json', 'data': {}}
    return {'state': 'loaded', 'data': data if isinstance(data, dict) else {}}


def build_gate(rollup_path, reviewer, decision):
    loaded = load_rollup(rollup_path)
    data = loaded['data']
    rollup_ready = loaded['state'] == 'loaded' and data.get('rollup_status') == 'ready'
    decision = decision.lower().strip()
    approved = rollup_ready and decision == 'approve'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'reviewer': reviewer,
        'decision': decision,
        'gate_status': 'approved' if approved else 'blocked',
        'rollup_path': rollup_path,
        'rollup_load_state': loaded['state'],
        'rollup_status': data.get('rollup_status'),
        'index_status': data.get('index_status'),
        'summary_status': data.get('summary_status'),
        'closure_closed': data.get('closure_closed'),
        'missing_required': data.get('missing_required', []),
        'invalid_json': data.get('invalid_json', []),
        'review_note': review_note(approved, rollup_ready, decision),
        'next_steps': next_steps(approved, rollup_ready, decision),
    }


def review_note(approved, rollup_ready, decision):
    if approved:
        return 'Final archive closeout review gate is approved.'
    if not rollup_ready:
        return 'Final archive closeout review gate is blocked because the rollup is not ready.'
    if decision != 'approve':
        return 'Final archive closeout review gate is blocked because reviewer decision is not approve.'
    return 'Final archive closeout review gate is blocked.'


def next_steps(approved, rollup_ready, decision):
    if approved:
        return ['Store the gate file with the final archive package.', 'Proceed with final reviewer handoff.']
    steps = []
    if not rollup_ready:
        steps.append('Regenerate or repair the rollup until it reports ready.')
    if decision != 'approve':
        steps.append('Set decision to approve only after reviewer confirms the rollup is ready.')
    return steps or ['Review gate inputs and rerun this builder.']


def render_markdown(gate):
    lines = [
        '# Archive Closeout Review Gate',
        '',
        f"Generated UTC: {gate['generated_on_utc']}",
        f"Reviewer: **{gate['reviewer']}**",
        f"Decision: **{gate['decision']}**",
        f"Gate status: **{gate['gate_status']}**",
        f"Rollup path: `{gate['rollup_path']}`",
        '',
        '## Rollup Snapshot',
        f"- Rollup load state: {gate['rollup_load_state']}",
        f"- Rollup status: {gate['rollup_status']}",
        f"- Index status: {gate['index_status']}",
        f"- Summary status: {gate['summary_status']}",
        f"- Closure closed: {gate['closure_closed']}",
        '',
        '## Review Note',
        gate['review_note'],
        '',
        '## Missing Required Files',
    ]
    for item in gate['missing_required'] or ['None']:
        lines.append(f'- `{item}`' if item != 'None' else '- None')
    lines.extend(['', '## Invalid JSON Files'])
    for item in gate['invalid_json'] or ['None']:
        lines.append(f'- `{item}`' if item != 'None' else '- None')
    lines.extend(['', '## Next Steps'])
    for step in gate['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_gate(rollup, reviewer, decision, out_json, out_md):
    gate = build_gate(rollup, reviewer, decision)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.write_text(json.dumps(gate, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(gate), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': gate['gate_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout review gate')
    parser.add_argument('--rollup', default='archive_closeout_rollup.json')
    parser.add_argument('--reviewer', default='Archive Reviewer')
    parser.add_argument('--decision', default='approve', choices=['approve', 'hold'])
    parser.add_argument('--out-json', default='archive_closeout_review_gate.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_REVIEW_GATE.md')
    args = parser.parse_args()
    print(json.dumps(write_gate(args.rollup, args.reviewer, args.decision, args.out_json, args.out_md), indent=2))


if __name__ == '__main__':
    main()
