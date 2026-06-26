#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ARCHIVE_FILES = [
    {'key': 'delivery_zip', 'path': 'delivery.zip', 'category': 'package'},
    {'key': 'project_closeout', 'path': 'project_closeout.json', 'category': 'closeout'},
    {'key': 'closeout_ops_report', 'path': 'closeout_ops_report.json', 'category': 'closeout'},
    {'key': 'client_feedback_report', 'path': 'client_feedback_report.json', 'category': 'feedback'},
    {'key': 'client_feedback_tracker', 'path': 'client_feedback_tracker.json', 'category': 'feedback'},
    {'key': 'delivery_manifest', 'path': 'delivery_manifest.json', 'category': 'manifest'},
    {'key': 'delivery_handoff_checklist', 'path': 'delivery_handoff_checklist.json', 'category': 'handoff'},
    {'key': 'client_delivery_email', 'path': 'client_delivery_email.json', 'category': 'communication'},
    {'key': 'publishing_instructions', 'path': 'publishing_instructions.json', 'category': 'publishing'},
    {'key': 'metadata_pack', 'path': 'metadata_pack.json', 'category': 'publishing'},
]

RETENTION_NOTES = [
    'Keep final delivery package and closeout report together.',
    'Keep client feedback tracker for audit and future revision context.',
    'Keep publishing metadata with final video assets.',
    'Do not delete source project files until client approval is confirmed.',
]


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def describe_file(project_dir, item):
    path = project_dir / item['path']
    exists = path.exists()
    stat = path.stat() if exists else None
    return {
        'key': item['key'],
        'category': item['category'],
        'relative_path': item['path'],
        'exists': exists,
        'size_bytes': stat.st_size if stat else 0,
        'modified_utc': datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat() if stat else None,
    }


def build_archive_manifest(project):
    project_dir = Path(project)
    closeout = load_json(project_dir / 'project_closeout.json', {})
    files = [describe_file(project_dir, item) for item in ARCHIVE_FILES]
    missing = [item for item in files if not item['exists']]
    available = [item for item in files if item['exists']]
    closeout_status = closeout.get('status', 'missing')
    ready = closeout_status == 'closed' and not missing
    return {
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'archive-ready' if ready else 'needs-attention',
        'closeout_status': closeout_status,
        'available_count': len(available),
        'missing_count': len(missing),
        'total_size_bytes': sum(item['size_bytes'] for item in files),
        'files': files,
        'retention_notes': RETENTION_NOTES,
    }


def render_markdown(manifest):
    lines = [
        '# Project Archive Manifest',
        '',
        f"Generated UTC: {manifest['generated_on_utc']}",
        f"Project: `{manifest['project']}`",
        f"Status: **{manifest['status']}**",
        f"Closeout status: **{manifest['closeout_status']}**",
        f"Available files: **{manifest['available_count']}**",
        f"Missing files: **{manifest['missing_count']}**",
        f"Total size bytes: **{manifest['total_size_bytes']}**",
        '',
        '## Archive Files',
        '| Key | Category | Exists | File | Size | Modified UTC |',
        '| --- | --- | --- | --- | ---: | --- |',
    ]
    for item in manifest['files']:
        modified = item['modified_utc'] or '-'
        lines.append(f"| {item['key']} | {item['category']} | {item['exists']} | `{item['relative_path']}` | {item['size_bytes']} | {modified} |")
    lines.extend(['', '## Retention Notes'])
    for note in manifest['retention_notes']:
        lines.append(f'- {note}')
    lines.append('')
    return '\n'.join(lines)


def write_manifest(project, out_json, out_md):
    manifest = build_archive_manifest(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(manifest), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': manifest['status']}


def main():
    parser = argparse.ArgumentParser(description='Build an archive manifest for a closed OpenMontage Plus project')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/project_archive_manifest.json')
    parser.add_argument('--out-md', default='projects/demo-video/PROJECT_ARCHIVE_MANIFEST.md')
    args = parser.parse_args()

    result = write_manifest(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
