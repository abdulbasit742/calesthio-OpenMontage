#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

DEFAULT_WPM = 150
PLATFORM_TARGETS = {
    'youtube-shorts': 60,
    'instagram-reels': 60,
    'tiktok': 60,
    'youtube': 180,
    'linkedin': 90,
    'square-feed': 45,
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def read_script(script_path, text):
    if script_path:
        path = Path(script_path)
        if not path.exists():
            raise SystemExit(f'Script file not found: {path}')
        return path.read_text(encoding='utf-8')
    return text


def count_words(text):
    return len(re.findall(r"[A-Za-z0-9']+", text))


def estimate_seconds(word_count, words_per_minute):
    if words_per_minute <= 0:
        raise SystemExit('words_per_minute must be greater than 0')
    return round((word_count / words_per_minute) * 60, 2)


def build_report(project, script_text, words_per_minute, target_seconds):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    preset = load_json(project_dir / 'export_preset.json', {})
    render_plan = load_json(project_dir / 'render_plan.json', {})

    platform = manifest.get('platform', preset.get('platform', 'youtube-shorts'))
    target = target_seconds or render_plan.get('duration_seconds') or manifest.get('duration_seconds') or PLATFORM_TARGETS.get(platform, 60)
    words = count_words(script_text)
    estimate = estimate_seconds(words, words_per_minute)
    difference = round(estimate - float(target), 2)

    if difference > 3:
        status = 'too-long'
        advice = f'Trim about {round((difference / 60) * words_per_minute)} words.'
    elif difference < -3:
        status = 'too-short'
        advice = f'Add about {round((abs(difference) / 60) * words_per_minute)} words or add visual-only pacing.'
    else:
        status = 'on-target'
        advice = 'Script timing is close to target duration.'

    return {
        'project': manifest.get('name', project_dir.name),
        'platform': platform,
        'target_seconds': float(target),
        'words_per_minute': words_per_minute,
        'word_count': words,
        'estimated_seconds': estimate,
        'difference_seconds': difference,
        'status': status,
        'advice': advice,
    }


def main():
    parser = argparse.ArgumentParser(description='Estimate script voiceover duration for OpenMontage Plus projects')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--script', help='Script text file to analyze')
    parser.add_argument('--text', default='OpenMontage Plus helps creators plan, package, and review social videos faster.')
    parser.add_argument('--wpm', type=int, default=DEFAULT_WPM)
    parser.add_argument('--target-seconds', type=float)
    parser.add_argument('--out', default='projects/demo-video/script_timing.json')
    args = parser.parse_args()

    script_text = read_script(args.script, args.text)
    report = build_report(args.project, script_text, args.wpm, args.target_seconds)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
