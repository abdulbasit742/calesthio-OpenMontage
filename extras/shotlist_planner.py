#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SCENE_TYPES = [
    'hook',
    'problem',
    'solution',
    'proof',
    'benefit',
    'call_to_action',
]


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def split_duration(duration_seconds, scene_count):
    duration = max(1, int(float(duration_seconds or 1)))
    scene_count = max(1, int(scene_count or 1))
    base = duration / scene_count
    slots = []
    for index in range(scene_count):
        start = round(index * base, 2)
        end = round((index + 1) * base, 2)
        slots.append((start, end))
    return slots


def scene_caption(scene_type, topic, audience):
    captions = {
        'hook': f'Here is why {topic} matters.',
        'problem': f'Most {audience} struggle with this problem.',
        'solution': f'The simple solution is to make it visual and repeatable.',
        'proof': f'Show the process, result, or before-and-after moment.',
        'benefit': f'This saves time and makes the message easier to understand.',
        'call_to_action': f'Follow for more {topic} ideas.',
    }
    return captions.get(scene_type, f'Show one clear idea about {topic}.')


def build_shotlist(project, topic, audience, scene_count, visual_style):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    preset = load_json(project_dir / 'export_preset.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    render_plan = load_json(project_dir / 'render_plan.json', {})

    project_name = manifest.get('name', project_dir.name)
    platform = manifest.get('platform', preset.get('platform', 'youtube-shorts'))
    duration = render_plan.get('duration_seconds', manifest.get('duration_seconds', 30))
    topic_text = topic or metadata.get('title') or project_name
    slots = split_duration(duration, scene_count)

    scenes = []
    for index, (start, end) in enumerate(slots, start=1):
        scene_type = SCENE_TYPES[min(index - 1, len(SCENE_TYPES) - 1)]
        scenes.append({
            'scene': index,
            'type': scene_type,
            'start_seconds': start,
            'end_seconds': end,
            'visual': f'{visual_style} shot for {scene_type} about {topic_text}',
            'caption': scene_caption(scene_type, topic_text, audience),
            'audio_note': 'Use clear voiceover and light background music.',
            'asset_needed': 'clip, image, screen recording, or generated visual placeholder',
        })

    return {
        'project': project_name,
        'platform': platform,
        'topic': topic_text,
        'audience': audience,
        'duration_seconds': duration,
        'scene_count': len(scenes),
        'visual_style': visual_style,
        'scenes': scenes,
    }


def main():
    parser = argparse.ArgumentParser(description='Build a scene-by-scene OpenMontage Plus shotlist')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--topic', default='')
    parser.add_argument('--audience', default='social media audience')
    parser.add_argument('--scene-count', type=int, default=6)
    parser.add_argument('--visual-style', default='fast, clean, modern social video')
    parser.add_argument('--out', default='projects/demo-video/shotlist.json')
    args = parser.parse_args()

    data = build_shotlist(args.project, args.topic, args.audience, args.scene_count, args.visual_style)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
