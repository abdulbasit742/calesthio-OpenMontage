#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

PLATFORM_GUIDES = {
    'youtube-shorts': [
        'Open the YouTube upload flow and select the final vertical video.',
        'Paste the prepared title, description, CTA, and hashtags from metadata_pack.json.',
        'Upload captions if an SRT/VTT file exists.',
        'Confirm the video displays correctly on mobile preview.',
        'Set visibility or schedule time based on the content calendar.',
    ],
    'instagram-reels': [
        'Open the Reels publishing flow and select the final vertical video.',
        'Paste caption copy and hashtags from metadata_pack.json or copy_variants.json.',
        'Check cover frame or thumbnail before posting.',
        'Confirm captions and key text are inside safe zones.',
        'Save as draft or publish after final approval.',
    ],
    'tiktok': [
        'Open the TikTok upload flow and select the final vertical video.',
        'Paste caption, CTA, and hashtags from metadata_pack.json.',
        'Check that on-screen text is readable in mobile preview.',
        'Confirm captions are present or burned into the video.',
        'Save draft or publish after final approval.',
    ],
    'youtube': [
        'Open the YouTube upload flow and select the final video file.',
        'Paste title, description, CTA, and hashtags from metadata_pack.json.',
        'Upload captions if available.',
        'Set thumbnail if thumbnail_brief output has been converted into an image.',
        'Review visibility, playlist, and schedule settings before publishing.',
    ],
    'linkedin': [
        'Open the LinkedIn post composer and attach the final video.',
        'Paste the prepared professional caption from metadata_pack.json or copy_variants.json.',
        'Confirm hashtags are concise and relevant.',
        'Check mobile and desktop preview before posting.',
        'Publish after approval gate is passed.',
    ],
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
            return str(path)
    return ''


def normalize_hashtags(value):
    if isinstance(value, list):
        return ' '.join(str(item) for item in value)
    return str(value or '')


def collect_assets(project_dir):
    return {
        'final_video': first_existing(project_dir, ['publish/final.mp4', 'renders/final.mp4', 'exports/final.mp4']),
        'captions_srt': first_existing(project_dir, ['captions/final.srt', 'exports/final.srt']),
        'captions_vtt': first_existing(project_dir, ['captions/final.vtt', 'exports/final.vtt']),
        'thumbnail_brief': first_existing(project_dir, ['thumbnail_brief.json']),
        'delivery_zip': first_existing(project_dir, ['delivery.zip']),
    }


def build_instructions(project):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    approval = load_json(project_dir / 'approval_gate.json', {})
    validation = load_json(project_dir / 'platform_validation.json', {})
    calendar = load_json(project_dir / 'content_calendar_entry.json', {})

    platform = metadata.get('platform') or manifest.get('platform') or validation.get('platform') or 'youtube-shorts'
    project_name = manifest.get('name') or project_dir.name
    title = metadata.get('title') or project_name
    description = metadata.get('description', '')
    cta = metadata.get('call_to_action') or metadata.get('cta', '')
    hashtags = normalize_hashtags(metadata.get('hashtags', []))
    assets = collect_assets(project_dir)

    required_checks = [
        {'name': 'approval_gate', 'passed': approval.get('approved') is True, 'status': approval.get('status', 'missing')},
        {'name': 'platform_validation', 'passed': validation.get('status') == 'valid', 'status': validation.get('status', 'missing')},
        {'name': 'final_video', 'passed': bool(assets['final_video']), 'status': 'found' if assets['final_video'] else 'missing'},
        {'name': 'title', 'passed': bool(title), 'status': 'found' if title else 'missing'},
        {'name': 'description', 'passed': bool(description), 'status': 'found' if description else 'missing'},
    ]

    blockers = [item for item in required_checks if not item['passed']]
    return {
        'project': project_name,
        'project_folder': str(project_dir),
        'generated_on': date.today().isoformat(),
        'platform': platform,
        'status': 'ready-to-publish' if not blockers else 'not-ready',
        'blockers': blockers,
        'metadata': {
            'title': title,
            'description': description,
            'cta': cta,
            'hashtags': hashtags,
        },
        'assets': assets,
        'schedule': {
            'publish_date': calendar.get('publish_date', ''),
            'publish_time': calendar.get('publish_time', ''),
        },
        'steps': PLATFORM_GUIDES.get(platform, PLATFORM_GUIDES['youtube-shorts']),
        'pre_publish_checks': required_checks,
    }


def render_markdown(data):
    lines = [
        f"# Publishing Instructions: {data['project']}",
        '',
        f"Generated: {data['generated_on']}",
        f"Platform: **{data['platform']}**",
        f"Status: **{data['status']}**",
        '',
        '## Metadata to Paste',
        f"**Title:** {data['metadata']['title']}",
        '',
        f"**Description:** {data['metadata']['description'] or 'Not set'}",
        '',
        f"**CTA:** {data['metadata']['cta'] or 'Not set'}",
        '',
        f"**Hashtags:** {data['metadata']['hashtags'] or 'Not set'}",
        '',
        '## Assets',
    ]
    for key, value in data['assets'].items():
        lines.append(f"- {key}: `{value or 'missing'}`")
    lines.extend(['', '## Pre-Publish Checks'])
    for item in data['pre_publish_checks']:
        lines.append(f"- {item['name']}: {item['status']} ({'passed' if item['passed'] else 'needs attention'})")
    lines.extend(['', '## Publishing Steps'])
    for index, step in enumerate(data['steps'], start=1):
        lines.append(f'{index}. {step}')
    if data['schedule']['publish_date'] or data['schedule']['publish_time']:
        lines.extend(['', '## Schedule', f"Publish date: {data['schedule']['publish_date'] or 'not set'}", f"Publish time: {data['schedule']['publish_time'] or 'not set'}"])
    lines.append('')
    return '\n'.join(lines)


def write_instructions(project, out_json, out_md):
    instructions = build_instructions(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(instructions, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(instructions), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': instructions['status']}


def main():
    parser = argparse.ArgumentParser(description='Generate platform publishing instructions for an OpenMontage Plus project')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/publishing_instructions.json')
    parser.add_argument('--out-md', default='projects/demo-video/PUBLISHING_INSTRUCTIONS.md')
    args = parser.parse_args()

    result = write_instructions(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
