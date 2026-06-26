#!/usr/bin/env python3
import argparse
import json
import zipfile
from pathlib import Path

REQUIRED_SUFFIXES = [
    'delivery_zip_manifest.json',
    'HANDOFF_README.md',
    'handoff_manifest.json',
    'RELEASE_NOTES.md',
    'metadata_pack.json',
    'platform_validation.json',
    'quality_score.json',
]


def find_entry(entries, suffix):
    for entry in entries:
        if entry.endswith(suffix):
            return entry
    return ''


def read_json_entry(zip_handle, entry_name):
    if not entry_name:
        return {}
    try:
        return json.loads(zip_handle.read(entry_name).decode('utf-8'))
    except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
        return {}


def audit_delivery_zip(zip_path):
    archive = Path(zip_path)
    if not archive.exists():
        return {
            'archive': str(archive),
            'status': 'missing',
            'errors': ['zip-file-not-found'],
            'warnings': [],
        }

    errors = []
    warnings = []
    entries = []
    manifest = {}

    try:
        with zipfile.ZipFile(archive, 'r') as zip_handle:
            bad_file = zip_handle.testzip()
            if bad_file:
                errors.append(f'corrupt-entry:{bad_file}')
            entries = sorted(zip_handle.namelist())
            manifest_entry = find_entry(entries, 'delivery_zip_manifest.json')
            manifest = read_json_entry(zip_handle, manifest_entry)
            if not manifest_entry:
                errors.append('delivery-manifest-missing')
            for suffix in REQUIRED_SUFFIXES:
                if not find_entry(entries, suffix):
                    warnings.append(f'missing-recommended-file:{suffix}')
    except zipfile.BadZipFile:
        return {
            'archive': str(archive),
            'status': 'invalid-zip',
            'errors': ['bad-zip-file'],
            'warnings': warnings,
        }

    video_entries = [entry for entry in entries if entry.lower().endswith(('.mp4', '.mov', '.mkv', '.webm'))]
    caption_entries = [entry for entry in entries if entry.lower().endswith(('.srt', '.vtt'))]
    if not video_entries:
        warnings.append('no-video-file-found')
    if not caption_entries:
        warnings.append('no-caption-file-found')

    return {
        'archive': str(archive),
        'archive_size_bytes': archive.stat().st_size,
        'entry_count': len(entries),
        'manifest_found': bool(manifest),
        'manifest_status': manifest.get('status', ''),
        'video_count': len(video_entries),
        'caption_count': len(caption_entries),
        'entries': entries,
        'video_entries': video_entries,
        'caption_entries': caption_entries,
        'errors': errors,
        'warnings': sorted(set(warnings)),
        'status': 'passed' if not errors else 'failed',
        'advice': 'ZIP is readable. Review warnings before delivery.' if not errors else 'Fix errors and rebuild the delivery ZIP.',
    }


def main():
    parser = argparse.ArgumentParser(description='Audit an OpenMontage Plus delivery ZIP archive')
    parser.add_argument('--zip', default='projects/demo-video/delivery.zip')
    parser.add_argument('--out', default='projects/demo-video/delivery_audit.json')
    args = parser.parse_args()

    report = audit_delivery_zip(args.zip)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
