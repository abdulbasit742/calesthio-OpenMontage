#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path

PACKAGE_FILES = {
    'video': ['renders/final.mp4', 'exports/final.mp4'],
    'captions_srt': ['captions/final.srt', 'exports/final.srt'],
    'captions_vtt': ['captions/final.vtt', 'exports/final.vtt'],
    'metadata': ['metadata_pack.json'],
    'thumbnail_brief': ['thumbnail_brief.json'],
    'review_checklist': ['review_checklist.json'],
    'asset_audit': ['asset_audit.json'],
    'script_timing': ['script_timing.json'],
}


def first_existing(project_dir, candidates):
    for relative in candidates:
        path = project_dir / relative
        if path.exists():
            return path
    return None


def copy_file(source, destination_dir):
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / source.name
    shutil.copy2(source, destination)
    return destination


def build_package(project, out_dir):
    project_dir = Path(project)
    package_dir = Path(out_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    missing = []
    for label, candidates in PACKAGE_FILES.items():
        source = first_existing(project_dir, candidates)
        if source is None:
            missing.append({'label': label, 'candidates': candidates})
            continue
        destination = copy_file(source, package_dir)
        copied.append({'label': label, 'source': str(source), 'destination': str(destination)})

    manifest = {
        'project': str(project_dir),
        'package_dir': str(package_dir),
        'copied_count': len(copied),
        'missing_count': len(missing),
        'copied': copied,
        'missing': missing,
        'status': 'ready' if not missing else 'incomplete',
        'next_steps': [
            'Review metadata_pack.json before publishing.',
            'Confirm captions are synced with final video.',
            'Confirm thumbnail brief or thumbnail image is approved.',
            'Upload final video and captions to the selected platform.',
        ],
    }
    manifest_path = package_dir / 'publish_manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description='Create a publish-ready OpenMontage Plus package')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-dir', default='projects/demo-video/publish')
    args = parser.parse_args()

    manifest = build_package(args.project, args.out_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
