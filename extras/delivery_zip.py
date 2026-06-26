#!/usr/bin/env python3
import argparse
import json
import zipfile
from datetime import date
from pathlib import Path

DEFAULT_INCLUDE_DIRS = ['handoff', 'publish']
DEFAULT_INCLUDE_FILES = [
    'HANDOFF_README.md',
    'handoff_manifest.json',
    'RELEASE_NOTES.md',
    'release_notes.json',
    'metadata_pack.json',
    'copy_variants.json',
    'platform_validation.json',
    'quality_score.json',
    'brand_kit.json',
]


def add_file(zip_handle, source, arcname, entries):
    if source.exists() and source.is_file():
        zip_handle.write(source, arcname)
        entries.append({'source': str(source), 'archive_path': str(arcname)})
        return True
    return False


def add_directory(zip_handle, source_dir, archive_root, entries):
    if not source_dir.exists() or not source_dir.is_dir():
        return 0
    count = 0
    for file_path in sorted(source_dir.rglob('*')):
        if file_path.is_file():
            relative = file_path.relative_to(source_dir)
            arcname = Path(archive_root) / relative
            zip_handle.write(file_path, arcname)
            entries.append({'source': str(file_path), 'archive_path': str(arcname)})
            count += 1
    return count


def build_delivery_zip(project, out_zip, include_project_root):
    project_dir = Path(project)
    output = Path(out_zip)
    output.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    missing = []
    archive_prefix = project_dir.name if include_project_root else ''

    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as zip_handle:
        for folder in DEFAULT_INCLUDE_DIRS:
            source_dir = project_dir / folder
            archive_root = Path(archive_prefix) / folder if archive_prefix else Path(folder)
            added_count = add_directory(zip_handle, source_dir, archive_root, entries)
            if added_count == 0:
                missing.append({'type': 'directory', 'path': str(source_dir)})

        for filename in DEFAULT_INCLUDE_FILES:
            source = project_dir / filename
            arcname = Path(archive_prefix) / filename if archive_prefix else Path(filename)
            if not add_file(zip_handle, source, arcname, entries):
                missing.append({'type': 'file', 'path': str(source)})

        manifest = {
            'project': str(project_dir),
            'archive': str(output),
            'generated_on': date.today().isoformat(),
            'entry_count': len(entries),
            'missing_count': len(missing),
            'entries': entries,
            'missing': missing,
            'status': 'ready' if entries else 'empty',
        }
        manifest_bytes = json.dumps(manifest, indent=2).encode('utf-8')
        manifest_name = Path(archive_prefix) / 'delivery_zip_manifest.json' if archive_prefix else Path('delivery_zip_manifest.json')
        zip_handle.writestr(str(manifest_name), manifest_bytes)

    manifest['archive_size_bytes'] = output.stat().st_size if output.exists() else 0
    return manifest


def main():
    parser = argparse.ArgumentParser(description='Build a client-ready ZIP archive from OpenMontage Plus handoff and publish files')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-zip', default='projects/demo-video/delivery.zip')
    parser.add_argument('--no-project-root', action='store_true')
    args = parser.parse_args()

    result = build_delivery_zip(args.project, args.out_zip, include_project_root=not args.no_project_root)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
