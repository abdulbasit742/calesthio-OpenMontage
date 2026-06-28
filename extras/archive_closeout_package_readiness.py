#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_ROLLUP = 'archive_closeout_rollup.json'
DEFAULT_GATE = 'archive_closeout_review_gate.json'
DEFAULT_MANIFEST = 'archive_closeout_milestone_manifest.json'


def load_json(path):
    source = Path(path)
    if not source.exists():
        return {'path': str(source), 'loaded': False, 'error': 'missing-file', 'data': {}}
    try:
        return {'path': str(source), 'loaded': True, 'error': None, 'data': json.loads(source.read_text(encoding='utf-8'))}
    except json.JSONDecodeError as exc:
        return {'path': str(source), 'loaded': False, 'error': f'invalid-json: {exc}', 'data': {}}


def status_from(data, keys, default='unknown'):
    for key in keys:
        value = data.get(key)
        if value:
            return value
    return default


def build_readiness(rollup_path, gate_path, manifest_path, label):
    rollup = load_json(rollup_path)
    gate = load_json(gate_path)
    manifest = load_json(manifest_path)

    rollup_status = status_from(rollup['data'], ['rollup_status', 'status']) if rollup['loaded'] else 'missing-or-invalid'
    gate_status = status_from(gate['data'], ['gate_status', 'status']) if gate['loaded'] else 'missing-or-invalid'
    manifest_status = status_from(manifest['data'], ['manifest_status', 'status']) if manifest['loaded'] else 'missing-or-invalid'

    blocking_issues = []
    if rollup_status != 'ready':
        blocking_issues.append(f'Rollup status is {rollup_status}; expected ready.')
    if gate_status != 'approved':
        blocking_issues.append(f'Review gate status is {gate_status}; expected approved.')
    if manifest_status != 'complete':
        blocking_issues.append(f'Manifest status is {manifest_status}; expected complete.')

    readiness_status = 'ready-for-handoff' if not blocking_issues else 'blocked'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'readiness_status': readiness_status,
        'rollup': {'path': rollup['path'], 'loaded': rollup['loaded'], 'error': rollup['error'], 'status': rollup_status},
        'review_gate': {'path': gate['path'], 'loaded': gate['loaded'], 'error': gate['error'], 'status': gate_status},
        'milestone_manifest': {'path': manifest['path'], 'loaded': manifest['loaded'], 'error': manifest['error'], 'status': manifest_status},
        'blocking_issues': blocking_issues,
        'next_steps': next_steps(blocking_issues),
    }


def next_steps(blocking_issues):
    if not blocking_issues:
        return [
            'Attach the readiness Markdown to the final archive package.',
            'Use the readiness JSON as the machine-readable handoff status.',
        ]
    return [
        'Fix the blocking issues listed in this report.',
        'Regenerate the rollup, review gate, or manifest as needed.',
        'Rerun this package readiness builder.',
    ]


def render_markdown(report):
    lines = [
        '# Archive Closeout Package Readiness',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Label: **{report['label']}**",
        f"Readiness status: **{report['readiness_status']}**",
        '',
        '## Inputs',
        '',
        '| Input | Path | Loaded | Status | Error |',
        '|---|---|---:|---|---|',
        f"| Rollup | `{report['rollup']['path']}` | {report['rollup']['loaded']} | {report['rollup']['status']} | {report['rollup']['error']} |",
        f"| Review gate | `{report['review_gate']['path']}` | {report['review_gate']['loaded']} | {report['review_gate']['status']} | {report['review_gate']['error']} |",
        f"| Milestone manifest | `{report['milestone_manifest']['path']}` | {report['milestone_manifest']['loaded']} | {report['milestone_manifest']['status']} | {report['milestone_manifest']['error']} |",
        '',
        '## Blocking Issues',
    ]
    if report['blocking_issues']:
        for issue in report['blocking_issues']:
            lines.append(f'- {issue}')
    else:
        lines.append('- None')
    lines.extend(['', '## Next Steps'])
    for step in report['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_readiness(args):
    report = build_readiness(args.rollup, args.review_gate, args.manifest, args.label)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.write_text(json.dumps(report, indent=2), encoding='utf-8')
    out_md.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(out_json), 'markdown': str(out_md), 'status': report['readiness_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout package readiness report')
    parser.add_argument('--rollup', default=DEFAULT_ROLLUP)
    parser.add_argument('--review-gate', default=DEFAULT_GATE)
    parser.add_argument('--manifest', default=DEFAULT_MANIFEST)
    parser.add_argument('--label', default='archive-closeout-package-readiness')
    parser.add_argument('--out-json', default='archive_closeout_package_readiness.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_PACKAGE_READINESS.md')
    args = parser.parse_args()
    print(json.dumps(write_readiness(args), indent=2))


if __name__ == '__main__':
    main()
