#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

PLATFORM_LIMITS = {
    'youtube-shorts': {'title': 70, 'hashtags': 8},
    'instagram-reels': {'title': 80, 'hashtags': 12},
    'tiktok': {'title': 80, 'hashtags': 10},
    'youtube': {'title': 90, 'hashtags': 8},
    'linkedin': {'title': 120, 'hashtags': 5},
    'square-feed': {'title': 80, 'hashtags': 10},
}

DEFAULT_KEYWORDS = ['video', 'ai', 'automation', 'creative', 'openmontage']


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def clean_tag(value):
    cleaned = re.sub(r'[^a-zA-Z0-9_]+', '', value.strip().replace(' ', '_'))
    return cleaned.lower()


def make_hashtags(keywords, limit):
    tags = []
    for keyword in keywords:
        tag = clean_tag(keyword)
        if tag and tag not in tags:
            tags.append(tag)
        if len(tags) >= limit:
            break
    return ['#' + tag for tag in tags]


def trim_text(text, max_length):
    text = ' '.join(text.split())
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rstrip() + '...'


def build_metadata(project, topic, audience, cta, keywords):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    preset = load_json(project_dir / 'export_preset.json', {})
    platform = manifest.get('platform', preset.get('platform', 'youtube-shorts'))
    limits = PLATFORM_LIMITS.get(platform, PLATFORM_LIMITS['youtube-shorts'])

    project_name = manifest.get('name', project_dir.name)
    topic_text = topic or project_name
    keyword_list = [item.strip() for item in keywords.split(',') if item.strip()] or DEFAULT_KEYWORDS
    hashtags = make_hashtags(keyword_list, limits['hashtags'])

    title = trim_text(f'{topic_text} | {project_name}', limits['title'])
    description = '\n'.join([
        f'{topic_text} made for {audience}.',
        '',
        cta,
        '',
        ' '.join(hashtags),
    ]).strip()

    return {
        'project': project_name,
        'platform': platform,
        'title': title,
        'description': description,
        'hashtags': hashtags,
        'audience': audience,
        'call_to_action': cta,
        'source': 'OpenMontage Plus metadata builder',
    }


def main():
    parser = argparse.ArgumentParser(description='Build platform-ready social metadata JSON')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--topic', default='')
    parser.add_argument('--audience', default='social media audience')
    parser.add_argument('--cta', default='Follow for more updates.')
    parser.add_argument('--keywords', default=','.join(DEFAULT_KEYWORDS))
    parser.add_argument('--out', default='metadata_pack.json')
    args = parser.parse_args()

    data = build_metadata(args.project, args.topic, args.audience, args.cta, args.keywords)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
