#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

SPECS = {
    'vertical': (1080, 1920),
    'horizontal': (1920, 1080),
    'square': (1080, 1080),
}

parser = argparse.ArgumentParser()
parser.add_argument('input', type=Path)
parser.add_argument('--out-dir', type=Path, default=Path('exports/video'))
parser.add_argument('--formats', default='vertical,horizontal')
args = parser.parse_args()

args.out_dir.mkdir(parents=True, exist_ok=True)
selected = [p.strip() for p in args.formats.split(',') if p.strip()]
plan = []
for item in selected:
    if item not in SPECS:
        raise SystemExit(f'Unknown format: {item}')
    width, height = SPECS[item]
    output = args.out_dir / f'{args.input.stem}_{item}_{width}x{height}.mp4'
    plan.append({'format': item, 'width': width, 'height': height, 'input': str(args.input), 'output': str(output)})

manifest = {'exports': plan}
(args.out_dir / 'export_plan.json').write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest, indent=2))
