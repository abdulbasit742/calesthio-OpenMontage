#!/usr/bin/env python3
import argparse
import json
import shutil
from datetime import date
from pathlib import Path

HANDOFF_SOURCES = {
    'brief': ['brief.md'],
    'manifest': ['production_manifest.json'],
    'brand_kit': ['brand_kit.json'],
    'metadata': ['metadata_pack.json'],
    'copy_variants': ['copy_variants.json'],
    'quality_score': ['quality_score.json'],
    'platform_validation': ['platform_validation.json'],
    'release_notes_json': ['release_notes.json'],
    'release_notes_md': ['RELEASE_NOTES.md'],
    'publish_manifest': ['publish/publish_manifest.json'],
    'captions_srt': ['captions/final.srt', 'exports/final.srt'],
    'captions_vtt': ['captions/final.vtt', 'exports/final.vtt'],
    'final_video': ['publish/final.mp4', 'renders/final.mp4', 'exports/final.mp4'],
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def first_existing(project_dir, candidates):
    for candidate in candidates:
        path = project_dir / candidate
        if path.exists():
            return path
    return None


def copy_optional(source, destination_dir):
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / source.name
    shutil.copy2(source, destination)
    return destination


def build_readme(project_dir, manifest, metadata, quality, validation, copied, missing):
    name = manifest.get('name') or project_dir.name
    platform = metadata.get('platform') or manifest.get('platform') or validation.get('platform') or 'not set'
    title = metadata.get('title') or name
    quality_score = quality.get('final_score_percent', 'not scored')
    status = quality.get('status') or validation.get('status') or manifest.get('status', 'draft')
    lines = [
        f'# Handoff Packet: {name}',
        '',
        f'Generated: {date.today().isoformat()}',
        f'Project folder: `{project_dir}`',
        f'Platform: **{platform}**',
        f'Title: **{title}**',
        f'Status: **{status}**',
        f'Quality score: **{quality_score}**',
        '',
        '## Included Files',
    ]
    if copied:
        lines.extend([f"- {item['label']}: `{item['file']}`" for item in copied])
    else:
        lines.append('- No files copied yet.')
    lines.extend(['', '## Missing / Not Generated Yet'])
    if missing:
        lines.extend([f"- {item['label']}: expected one of {', '.join(item['candidates'])}" for item in missing])
    else:
        lines.append('- None')
    lines.extend([
        '',
        '## Recommended Handoff Order',
        '1. Review RELEASE_NOTES.md first.',
        '2. Check metadata_pack.json and copy_variants.json.',
        '3. Confirm platform_validation.json has no blocking errors.',
        '4. Confirm final video and captions exist before sending to client.',
        '5. Zip this handoff folder for delivery.',
        '',
    ])
    return '\n'.join(lines)


def build_handoff(project, out_dir):
    project_dir = Path(project)
    handoff_dir = Path(out_dir)
    handoff_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_json(project_dir / 'production_manifest.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    quality = load_json(project_dir / 'quality_score.json', {})
    validation = load_json(project_dir / 'platform_validation.json', {})

    copied = []
    missing = []
    for label, candidates in HANDOFF_SOURCES.items():
        source = first_existing(project_dir, candidates)
        if source:
            destination = copy_optional(source, handoff_dir)
            copied.append({'label': label, 'source': str(source), 'file': str(destination)})
        else:
            missing.append({'label': label, 'candidates': candidates})

    readme = build_readme(project_dir, manifest, metadata, quality, validation, copied, missing)
    readme_path = handoff_dir / 'HANDOFF_README.md'
    readme_path.write_text(readme, encoding='utf-8')

    manifest_out = {
        'project': str(project_dir),
        'handoff_dir': str(handoff_dir),
        'generated_on': date.today().isoformat(),
        'copied_count': len(copied),
        'missing_count': len(missing),
        'copied': copied,
        'missing': missing,
        'status': 'complete' if not missing else 'incomplete',
        'readme': str(readme_path),
    }
    manifest_path = handoff_dir / 'handoff_manifest.json'
    manifest_path.write_text(json.dumps(manifest_out, indent=2), encoding='utf-8')
    return manifest_out


def main():
    parser = argparse.ArgumentParser(description='Build a client/developer handoff packet for an OpenMontage Plus project')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-dir', default='projects/demo-video/handoff')
    args = parser.parse_args()

    result = build_handoff(args.project, args.out_dir)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
