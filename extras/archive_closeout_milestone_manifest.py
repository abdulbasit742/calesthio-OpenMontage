#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ARTIFACTS = [
    {'feature': 201, 'path': 'extras/archive_closeout_rollup.py', 'kind': 'builder', 'purpose': 'Build archive closeout rollup.'},
    {'feature': 202, 'path': 'docs/ARCHIVE_CLOSEOUT_ROLLUP_GUIDE.md', 'kind': 'guide', 'purpose': 'Document rollup builder usage.'},
    {'feature': 203, 'path': 'extras/archive_closeout_rollup_helper.py', 'kind': 'helper', 'purpose': 'Expose rollup helper commands.'},
    {'feature': 204, 'path': 'docs/ARCHIVE_CLOSEOUT_ROLLUP_HELPER_GUIDE.md', 'kind': 'guide', 'purpose': 'Document rollup helper usage.'},
    {'feature': 205, 'path': 'docs/ARCHIVE_CLOSEOUT_ROLLUP_HELPER_AUDIT_NOTE.md', 'kind': 'audit-note', 'purpose': 'Record rollup helper audit coverage.'},
    {'feature': 206, 'path': 'extras/archive_closeout_review_gate.py', 'kind': 'builder', 'purpose': 'Build final review gate.'},
    {'feature': 207, 'path': 'docs/ARCHIVE_CLOSEOUT_REVIEW_GATE_GUIDE.md', 'kind': 'guide', 'purpose': 'Document review gate usage.'},
    {'feature': 208, 'path': 'extras/archive_closeout_review_gate_helper.py', 'kind': 'helper', 'purpose': 'Expose review gate helper commands.'},
    {'feature': 209, 'path': 'docs/ARCHIVE_CLOSEOUT_REVIEW_GATE_HELPER_GUIDE.md', 'kind': 'guide', 'purpose': 'Document review gate helper usage.'},
    {'feature': 210, 'path': 'docs/ARCHIVE_CLOSEOUT_REVIEW_GATE_HELPER_AUDIT_NOTE.md', 'kind': 'audit-note', 'purpose': 'Record review gate helper audit coverage.'},
    {'feature': 211, 'path': 'docs/ARCHIVE_CLOSEOUT_FEATURE_201_210_MILESTONE_SUMMARY.md', 'kind': 'summary', 'purpose': 'Summarize closeout milestone artifacts.'},
]


def inspect_artifact(row):
    path = Path(row['path'])
    item = dict(row)
    item['exists'] = path.exists()
    item['size_bytes'] = path.stat().st_size if path.exists() else 0
    return item


def build_manifest(label):
    items = [inspect_artifact(row) for row in ARTIFACTS]
    missing = [item['path'] for item in items if not item['exists']]
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'manifest_status': 'complete' if not missing else 'needs-attention',
        'artifact_count': len(items),
        'present_count': len(items) - len(missing),
        'missing_count': len(missing),
        'missing_artifacts': missing,
        'artifacts': items,
        'next_steps': steps(missing),
    }


def steps(missing):
    if not missing:
        return ['Store the manifest with the feature 201-210 closeout package.', 'Use it as a quick artifact completeness check.']
    return ['Add or regenerate missing artifacts, then rerun this manifest builder.']


def render_markdown(manifest):
    lines = [
        '# Archive Closeout Milestone Manifest',
        '',
        f"Generated UTC: {manifest['generated_on_utc']}",
        f"Label: **{manifest['label']}**",
        f"Manifest status: **{manifest['manifest_status']}**",
        f"Artifact count: {manifest['artifact_count']}",
        f"Present count: {manifest['present_count']}",
        f"Missing count: {manifest['missing_count']}",
        '',
        '## Artifacts',
        '',
        '| Feature | Kind | Exists | Size | Path | Purpose |',
        '|---|---|---:|---:|---|---|',
    ]
    for item in manifest['artifacts']:
        lines.append(f"| {item['feature']} | {item['kind']} | {item['exists']} | {item['size_bytes']} | `{item['path']}` | {item['purpose']} |")
    lines.extend(['', '## Missing Artifacts'])
    if manifest['missing_artifacts']:
        for path in manifest['missing_artifacts']:
            lines.append(f'- `{path}`')
    else:
        lines.append('- None')
    lines.extend(['', '## Next Steps'])
    for step in manifest['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_manifest(label, out_json, out_md):
    manifest = build_manifest(label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(manifest), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': manifest['manifest_status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive closeout milestone manifest')
    parser.add_argument('--label', default='archive-closeout-feature-201-210-manifest')
    parser.add_argument('--out-json', default='archive_closeout_milestone_manifest.json')
    parser.add_argument('--out-md', default='ARCHIVE_CLOSEOUT_MILESTONE_MANIFEST.md')
    args = parser.parse_args()
    print(json.dumps(write_manifest(args.label, args.out_json, args.out_md), indent=2))


if __name__ == '__main__':
    main()
