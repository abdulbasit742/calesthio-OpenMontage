#!/usr/bin/env python3
import argparse
import math
from pathlib import Path


def read_lines(script_path, fallback_text):
    if script_path:
        path = Path(script_path)
        if not path.exists():
            raise SystemExit(f'Script file not found: {path}')
        text = path.read_text(encoding='utf-8')
    else:
        text = fallback_text
    return [line.strip() for line in text.splitlines() if line.strip()]


def seconds_to_srt_time(value):
    millis = int(round(value * 1000))
    hours = millis // 3600000
    millis %= 3600000
    minutes = millis // 60000
    millis %= 60000
    seconds = millis // 1000
    millis %= 1000
    return f'{hours:02}:{minutes:02}:{seconds:02},{millis:03}'


def seconds_to_vtt_time(value):
    return seconds_to_srt_time(value).replace(',', '.')


def build_segments(lines, duration):
    if not lines:
        lines = ['Add your caption text here.']
    total = max(float(duration), len(lines))
    slot = total / len(lines)
    segments = []
    for index, line in enumerate(lines, start=1):
        start = (index - 1) * slot
        end = min(index * slot, total)
        if math.isclose(start, end):
            end = start + 1
        segments.append({'index': index, 'start': start, 'end': end, 'text': line})
    return segments


def render_srt(segments):
    blocks = []
    for item in segments:
        blocks.append('\n'.join([
            str(item['index']),
            f"{seconds_to_srt_time(item['start'])} --> {seconds_to_srt_time(item['end'])}",
            item['text'],
        ]))
    return '\n\n'.join(blocks) + '\n'


def render_vtt(segments):
    blocks = ['WEBVTT', '']
    for item in segments:
        blocks.append('\n'.join([
            f"{seconds_to_vtt_time(item['start'])} --> {seconds_to_vtt_time(item['end'])}",
            item['text'],
        ]))
        blocks.append('')
    return '\n'.join(blocks)


def main():
    parser = argparse.ArgumentParser(description='Build SRT and VTT captions from script lines')
    parser.add_argument('--script', help='Text file where each line becomes a caption segment')
    parser.add_argument('--text', default='OpenMontage Plus caption demo.\nEdit this script and regenerate captions.')
    parser.add_argument('--duration', type=float, default=30)
    parser.add_argument('--out-prefix', default='projects/demo-video/captions/final')
    args = parser.parse_args()

    lines = read_lines(args.script, args.text)
    segments = build_segments(lines, args.duration)
    prefix = Path(args.out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    srt_path = prefix.with_suffix('.srt')
    vtt_path = prefix.with_suffix('.vtt')
    srt_path.write_text(render_srt(segments), encoding='utf-8')
    vtt_path.write_text(render_vtt(segments), encoding='utf-8')
    print(f'Wrote {srt_path}')
    print(f'Wrote {vtt_path}')


if __name__ == '__main__':
    main()
