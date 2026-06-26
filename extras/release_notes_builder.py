#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def bullet_list(items):
    if not items:
        return '- None recorded'
    return '\n'.join(f'- {item}' for item in items)


def extract_copied_files(publish_manifest):
    copied = publish_manifest.get('copied', []) if publish_manifest else []
    return [f"{item.get('label', 'file')}: {item.get('destination', item.get('source', ''))}" for item in copied]


def extract_missing_items(publish_manifest):
    missing = publish_manifest.get('missing', []) if publish_manifest else []
    return [f"{item.get('label', 'item')} missing" for item in missing]


def build_release_data(project):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    quality = load_json(project_dir / 'quality_score.json', {})
    publish_manifest = load_json(project_dir / 'publish' / 'publish_manifest.json', {})
    brand_kit = load_json(project_dir / 'brand_kit.json', {})
    copy_variants = load_json(project_dir / 'copy_variants.json', {})
    asset_audit = load_json(project_dir / 'asset_audit.json', {})

    title = metadata.get('title') or manifest.get('name') or project_dir.name
    platform = metadata.get('platform') or manifest.get('platform') or 'youtube-shorts'
    release_status = quality.get('status') or publish_manifest.get('status') or manifest.get('status', 'draft')

    return {
        'project': manifest.get('name', project_dir.name),
        'project_folder': str(project_dir),
        'release_date': date.today().isoformat(),
        'title': title,
        'platform': platform,
        'status': release_status,
        'quality_score': quality.get('final_score_percent', ''),
        'topic': manifest.get('topic', title),
        'audience': metadata.get('audience') or manifest.get('audience', 'social media audience'),
        'duration_seconds': manifest.get('duration_seconds', ''),
        'brand': brand_kit.get('brand_name', ''),
        'metadata_summary': {
            'description': metadata.get('description', ''),
            'cta': metadata.get('call_to_action', metadata.get('cta', '')),
            'hashtags': metadata.get('hashtags', []),
        },
        'copy_variant_count': copy_variants.get('variant_count', 0),
        'publish_files': extract_copied_files(publish_manifest),
        'missing_items': extract_missing_items(publish_manifest),
        'asset_status': asset_audit.get('status', ''),
        'asset_issues': asset_audit.get('issues', []),
        'next_steps': publish_manifest.get('next_steps', []) or quality.get('recommended_next_steps', []),
    }


def render_markdown(data):
    hashtags = data['metadata_summary'].get('hashtags', [])
    if isinstance(hashtags, list):
        hashtags_text = ' '.join(hashtags)
    else:
        hashtags_text = str(hashtags)

    return '\n'.join([
        f"# Release Notes: {data['title']}",
        '',
        f"**Project:** {data['project']}",
        f"**Platform:** {data['platform']}",
        f"**Status:** {data['status']}",
        f"**Quality Score:** {data['quality_score']}",
        f"**Release Date:** {data['release_date']}",
        '',
        '## Summary',
        f"Topic: {data['topic']}",
        f"Audience: {data['audience']}",
        f"Duration: {data['duration_seconds']} seconds",
        f"Brand: {data['brand'] or 'Not set'}",
        '',
        '## Metadata',
        f"Description: {data['metadata_summary'].get('description', '') or 'Not set'}",
        f"CTA: {data['metadata_summary'].get('cta', '') or 'Not set'}",
        f"Hashtags: {hashtags_text or 'Not set'}",
        f"Copy variants: {data['copy_variant_count']}",
        '',
        '## Publish Package Files',
        bullet_list(data['publish_files']),
        '',
        '## Missing Items',
        bullet_list(data['missing_items']),
        '',
        '## Asset Status',
        f"Status: {data['asset_status'] or 'Not checked'}",
        bullet_list(data['asset_issues']),
        '',
        '## Next Steps',
        bullet_list(data['next_steps']),
        '',
    ])


def build_release_notes(project, out_json, out_md):
    data = build_release_data(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(data), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'release': data}


def main():
    parser = argparse.ArgumentParser(description='Build Markdown and JSON release notes for an OpenMontage Plus project')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/release_notes.json')
    parser.add_argument('--out-md', default='projects/demo-video/RELEASE_NOTES.md')
    args = parser.parse_args()

    result = build_release_notes(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
