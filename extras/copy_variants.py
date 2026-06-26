#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

VARIANT_STYLES = {
    'direct': {
        'title_prefix': '',
        'cta': 'Watch now and save this for later.',
        'description_lead': 'A clear, direct breakdown for',
    },
    'curiosity': {
        'title_prefix': 'What nobody tells you about',
        'cta': 'Follow for the next practical idea.',
        'description_lead': 'A curiosity-driven angle made for',
    },
    'benefit': {
        'title_prefix': 'How to get better results with',
        'cta': 'Try this workflow in your next project.',
        'description_lead': 'A benefit-first version designed for',
    },
    'problem_solution': {
        'title_prefix': 'Stop struggling with',
        'cta': 'Use this as your quick starting point.',
        'description_lead': 'A problem-solution copy angle for',
    },
}

PLATFORM_HASHTAG_LIMITS = {
    'youtube-shorts': 8,
    'instagram-reels': 12,
    'tiktok': 10,
    'youtube': 8,
    'linkedin': 5,
    'square-feed': 10,
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def trim(text, limit):
    text = ' '.join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + '...'


def normalize_hashtags(hashtags):
    if isinstance(hashtags, str):
        hashtags = hashtags.split()
    clean = []
    for tag in hashtags or []:
        value = str(tag).strip()
        if not value:
            continue
        if not value.startswith('#'):
            value = '#' + value.lstrip('#')
        if value.lower() not in [item.lower() for item in clean]:
            clean.append(value)
    return clean


def build_variant(style_name, style, base_title, topic, audience, platform, hashtags):
    title_core = topic or base_title
    if style['title_prefix']:
        title = f"{style['title_prefix']} {title_core}"
    else:
        title = title_core
    limit = 90 if platform in {'youtube', 'linkedin'} else 70
    selected_hashtags = hashtags[: PLATFORM_HASHTAG_LIMITS.get(platform, 8)]
    return {
        'style': style_name,
        'title': trim(title, limit),
        'description': '\n'.join([
            f"{style['description_lead']} {audience}.",
            f'Topic: {title_core}',
            style['cta'],
            ' '.join(selected_hashtags),
        ]).strip(),
        'call_to_action': style['cta'],
        'hashtags': selected_hashtags,
    }


def build_variants(project, count):
    project_dir = Path(project)
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    manifest = load_json(project_dir / 'production_manifest.json', {})
    preset = load_json(project_dir / 'export_preset.json', {})

    platform = metadata.get('platform') or manifest.get('platform') or preset.get('platform') or 'youtube-shorts'
    base_title = metadata.get('title') or manifest.get('name') or project_dir.name
    topic = manifest.get('topic') or base_title
    audience = metadata.get('audience') or manifest.get('audience') or 'social media audience'
    hashtags = normalize_hashtags(metadata.get('hashtags') or ['#video', '#ai', '#automation', '#openmontage'])

    variants = []
    for style_name, style in VARIANT_STYLES.items():
        variants.append(build_variant(style_name, style, base_title, topic, audience, platform, hashtags))
        if len(variants) >= count:
            break

    return {
        'project': str(project_dir),
        'platform': platform,
        'base_title': base_title,
        'variant_count': len(variants),
        'variants': variants,
    }


def main():
    parser = argparse.ArgumentParser(description='Generate platform copy variants for OpenMontage Plus metadata')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--count', type=int, default=4)
    parser.add_argument('--out', default='projects/demo-video/copy_variants.json')
    args = parser.parse_args()

    data = build_variants(args.project, max(1, args.count))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
