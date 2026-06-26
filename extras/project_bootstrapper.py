#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

PROJECT_DIRS = ['assets', 'scripts', 'renders', 'exports', 'reviews', 'captions', 'publish']

DEFAULT_CHECKS = [
    'captions are readable and synced',
    'thumbnail or thumbnail brief is approved',
    'audio level is clear',
    'metadata pack is complete',
    'export preset matches platform',
    'final review completed',
]


def slugify(value):
    value = value.strip().lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-') or 'untitled-project'


def write_json(path, data, overwrite):
    if path.exists() and not overwrite:
        return {'path': str(path), 'status': 'skipped-existing'}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    return {'path': str(path), 'status': 'written'}


def write_text(path, text, overwrite):
    if path.exists() and not overwrite:
        return {'path': str(path), 'status': 'skipped-existing'}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
    return {'path': str(path), 'status': 'written'}


def bootstrap_project(name, platform, duration, topic, audience, root, overwrite):
    slug = slugify(name)
    project_dir = Path(root) / slug
    project_dir.mkdir(parents=True, exist_ok=True)

    created_dirs = []
    for folder in PROJECT_DIRS:
        target = project_dir / folder
        target.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(target))

    manifest = {
        'name': name,
        'slug': slug,
        'platform': platform,
        'duration_seconds': duration,
        'topic': topic,
        'audience': audience,
        'status': 'draft',
    }
    local_zero_cost = {
        'mode': 'local-zero-cost',
        'allow_paid_api_calls': False,
        'prefer_local_tools': True,
        'recommended_next_command': f'python extras/render_plan_builder.py --project {project_dir} --out {project_dir}/render_plan.json',
    }
    review = {
        'project': name,
        'checks': [{'name': check, 'done': False, 'note': ''} for check in DEFAULT_CHECKS],
    }
    voiceover = '\n'.join([
        f'Hook: Here is why {topic} matters.',
        f'Problem: Most {audience} need a faster way to understand it.',
        'Solution: Show the process visually and keep the message simple.',
        'Proof: Add one clear result, demo, or before-and-after moment.',
        'CTA: Follow for more useful video ideas.',
        '',
    ])
    brief = f'# {name}\n\nTopic: {topic}\nAudience: {audience}\nPlatform: {platform}\nDuration: {duration}s\n\n## Next steps\n- Add assets in assets/\n- Edit scripts/voiceover.txt\n- Generate render plan\n- Build captions and metadata\n- Run review checklist\n'

    writes = [
        write_json(project_dir / 'production_manifest.json', manifest, overwrite),
        write_json(project_dir / 'local_zero_cost.json', local_zero_cost, overwrite),
        write_json(project_dir / 'review_checklist.json', review, overwrite),
        write_text(project_dir / 'scripts' / 'voiceover.txt', voiceover, overwrite),
        write_text(project_dir / 'brief.md', brief, overwrite),
    ]

    return {
        'project_dir': str(project_dir),
        'created_dirs': created_dirs,
        'files': writes,
        'next_commands': [
            f'python extras/export_presets.py write --project {project_dir} --preset {platform}',
            f'python extras/render_plan_builder.py --project {project_dir} --out {project_dir}/render_plan.json',
            f'python extras/script_timer.py --project {project_dir} --script {project_dir}/scripts/voiceover.txt --out {project_dir}/script_timing.json',
            f'python extras/caption_builder.py --script {project_dir}/scripts/voiceover.txt --duration {duration} --out-prefix {project_dir}/captions/final',
            f'python extras/metadata_builder.py --project {project_dir} --topic "{topic}" --audience "{audience}" --out {project_dir}/metadata_pack.json',
        ],
    }


def main():
    parser = argparse.ArgumentParser(description='Bootstrap a complete OpenMontage Plus project workspace')
    parser.add_argument('--name', required=True)
    parser.add_argument('--platform', default='youtube-shorts')
    parser.add_argument('--duration', type=int, default=45)
    parser.add_argument('--topic', default='AI product launch')
    parser.add_argument('--audience', default='social media audience')
    parser.add_argument('--root', default='projects')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()

    result = bootstrap_project(args.name, args.platform, args.duration, args.topic, args.audience, args.root, args.overwrite)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
