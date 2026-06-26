#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

RATES = {
    'image': 0.02,
    'generated_video_second': 0.035,
    'tts_minute': 0.03,
    'music_track': 0.10,
}


def estimate_cost(plan):
    images = int(plan.get('images', 0))
    video_seconds = float(plan.get('generated_video_seconds', 0))
    tts_minutes = float(plan.get('tts_minutes', 0))
    music_tracks = int(plan.get('music_tracks', 0))
    return round(
        images * RATES['image']
        + video_seconds * RATES['generated_video_second']
        + tts_minutes * RATES['tts_minute']
        + music_tracks * RATES['music_track'],
        4,
    )


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        raise SystemExit(f'File not found: {file_path}')
    return json.loads(file_path.read_text())


def build_report(plan, budget):
    total = estimate_cost(plan)
    approved = total <= budget
    return {
        'approved': approved,
        'estimated_total_usd': total,
        'budget_usd': budget,
        'remaining_usd': round(budget - total, 4),
        'message': 'approved' if approved else 'blocked_budget_exceeded',
    }


def main():
    parser = argparse.ArgumentParser(description='Approve or block a render plan based on budget')
    parser.add_argument('--plan', help='JSON file with images, generated_video_seconds, tts_minutes, music_tracks')
    parser.add_argument('--budget', type=float, default=1.0)
    parser.add_argument('--write-report', default='budget_gate_report.json')
    args = parser.parse_args()

    plan = load_json(args.plan) if args.plan else {}
    report = build_report(plan, args.budget)
    Path(args.write_report).write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if not report['approved']:
        raise SystemExit('Budget gate blocked this plan')


if __name__ == '__main__':
    main()
