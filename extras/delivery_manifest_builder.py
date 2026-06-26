#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DELIVERY_FILES = [
    {'key': 'metadata', 'path': 'metadata_pack.json', 'group': 'publishing'},
    {'key': 'publishing_instructions', 'path': 'publishing_instructions.json', 'group': 'publishing'},
    {'key': 'content_risk', 'path': 'content_risk_check.json', 'group': 'review'},
    {'key': 'project_review', 'path': 'project_review_summary.json', 'group': 'review'},
    {'key': 'approval_gate', 'path': 'approval_gate.json', 'group': 'review'},
    {'key': 'report_index', 'path': 'report_index.json', 'group': 'ops'},
    {'key': 'readiness_badge', 'path': 'delivery_readiness_badge.json', 'group': 'ops'},
    {'key': 'delivery_zip', 'path': 'delivery.zip', 'group': 'delivery'},
]


def describe_file(project_dir, item):
    path = project_dir / item['path']
    exists = path.exists()
    stat = path.stat() if exists else None
    return {
        'key': item['key'],
        'group': item['group'],
        'relative_path': item['path'],
        'exists': exists,
        'size_bytes': stat.st_size if stat else 0,
        'modified_utc': datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat() if stat else None,
    }


def build_manifest(project):
    project_dir = Path(project)
    files = [describe_file(project_dir, item) for item in DELIVERY_FILES]
    missing = [item for item in files if not item['exists']]
    available = [item for item in files if item['exists']]
    return {
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'complete' if not missing else 'needs-attention',
        'available_count': len(available),
        'missing_count': len(missing),
        'files': files,
    }


def render_markdown(manifest):
    lines = [
        '# Delivery Manifest',
        '',
        f"Generated UTC: {manifest['generated_on_utc']}",
        f"Project: `{manifest['project']}`",
        f"Status: **{manifest['status']}**",
        f"Available: **{manifest['available_count']}**",
        f"Missing: **{manifest['missing_count']}**",
        '',
        '| Key | Group | Exists | File | Size | Modified UTC |',
        '| --- | --- | --- | --- | ---: | --- |',
    ]
    for item in manifest['files']:
        modified = item['modified_utc'] or '-'
        lines.append(f"| {item['key']} | {item['group']} | {item['exists']} | `{item['relative_path']}` | {item['size_bytes']} | {modified} |")
    lines.append('')
    return '\n'.join(lines)


def write_manifest(project, out_json, out_md):
    manifest = build_manifest(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(manifest), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': manifest['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a client delivery manifest from known OpenMontage Plus output files')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/delivery_manifest.json')
    parser.add_argument('--out-md', default='projects/demo-video/DELIVERY_MANIFEST.md')
    args = parser.parse_args()

    result = write_manifest(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
