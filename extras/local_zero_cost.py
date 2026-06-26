#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path

LOCAL_STACK = {
    'video_editing': ['ffmpeg'],
    'web_rendering': ['node', 'npm'],
    'python_runtime': ['python'],
    'optional_tts': ['piper'],
    'optional_subtitles': ['whisper'],
}

DEFAULT_CONFIG = {
    'mode': 'local-zero-cost',
    'allow_paid_api_calls': False,
    'prefer_local_tools': True,
    'tools': {
        'video': 'ffmpeg',
        'tts': 'piper optional',
        'subtitles': 'whisper optional',
        'renderer': 'local remotion or ffmpeg',
    },
    'rules': [
        'Do not call paid image, video, music, or voice APIs unless user manually changes this config.',
        'Prefer local assets, local editing, and reusable templates.',
        'Run budget_gate.py before any paid provider is enabled.',
    ],
}


def detect_tools():
    result = {}
    for group, tools in LOCAL_STACK.items():
        result[group] = {tool: bool(shutil.which(tool)) for tool in tools}
    return result


def write_config(project):
    project_dir = Path(project)
    project_dir.mkdir(parents=True, exist_ok=True)
    config_path = project_dir / 'local_zero_cost.json'
    data = dict(DEFAULT_CONFIG)
    data['detected_tools'] = detect_tools()
    config_path.write_text(json.dumps(data, indent=2))
    return config_path, data


def main():
    parser = argparse.ArgumentParser(description='Prepare a local zero-cost OpenMontage Plus config')
    parser.add_argument('command', choices=['detect', 'write'])
    parser.add_argument('--project', default='projects/demo-video')
    args = parser.parse_args()

    if args.command == 'detect':
        print(json.dumps(detect_tools(), indent=2))
    elif args.command == 'write':
        path, data = write_config(args.project)
        print(json.dumps({'written': str(path), 'config': data}, indent=2))


if __name__ == '__main__':
    main()
