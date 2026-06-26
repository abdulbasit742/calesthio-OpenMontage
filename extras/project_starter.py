#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True)
parser.add_argument('--duration', type=int, default=60)
parser.add_argument('--platform', default='youtube-shorts')
args = parser.parse_args()

slug = args.name.lower().replace(' ', '-')
root = Path('projects') / slug
for folder in ['assets', 'scripts', 'renders', 'exports', 'reviews']:
    (root / folder).mkdir(parents=True, exist_ok=True)

manifest = {
    'name': args.name,
    'duration_seconds': args.duration,
    'platform': args.platform,
    'status': 'draft'
}
(root / 'production_manifest.json').write_text(json.dumps(manifest, indent=2))
(root / 'brief.md').write_text(f'# {args.name}\n\nGoal: create a {args.duration}s video for {args.platform}.\n')
print(f'Created {root}')
