#!/usr/bin/env python3
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--duration', type=float, required=True)
parser.add_argument('--images', type=int, default=0)
parser.add_argument('--generated-video-seconds', type=float, default=0)
parser.add_argument('--tts-minutes', type=float, default=0)
parser.add_argument('--music-tracks', type=int, default=0)
parser.add_argument('--budget', type=float, default=1.0)
args = parser.parse_args()

rates = {
    'image': 0.02,
    'video_second': 0.035,
    'tts_minute': 0.03,
    'music_track': 0.10,
}

costs = {
    'images': args.images * rates['image'],
    'generated_video': args.generated_video_seconds * rates['video_second'],
    'tts': args.tts_minutes * rates['tts_minute'],
    'music': args.music_tracks * rates['music_track'],
}
total = round(sum(costs.values()), 4)
result = {
    'planned_duration_seconds': args.duration,
    'costs_usd': {k: round(v, 4) for k, v in costs.items()},
    'estimated_total_usd': total,
    'budget_usd': args.budget,
    'within_budget': total <= args.budget,
}
print(json.dumps(result, indent=2))
if total > args.budget:
    raise SystemExit('Budget cap exceeded')
