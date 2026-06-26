#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DEFAULT_BRAND_KIT = {
    'brand_name': 'OpenMontage Plus Project',
    'tone': 'clear, helpful, modern, confident',
    'colors': {
        'primary': '#111827',
        'secondary': '#2563EB',
        'accent': '#FACC15',
        'background': '#FFFFFF',
        'text': '#111827',
    },
    'fonts': {
        'heading': 'Inter Bold',
        'body': 'Inter Regular',
        'caption': 'Inter Medium',
    },
    'logo': {
        'primary': 'assets/logo.png',
        'mark': 'assets/logo-mark.png',
        'safe_area': 'keep 10 percent margin around logo',
    },
    'visual_rules': [
        'Use high contrast text over video.',
        'Keep captions inside platform safe zones.',
        'Use one main accent color per scene.',
        'Avoid tiny text and cluttered backgrounds.',
    ],
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def save_json(path, data):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2), encoding='utf-8')
    return str(output)


def create_brand_kit(project, brand_name, primary, secondary, accent, tone, overwrite):
    project_dir = Path(project)
    output = project_dir / 'brand_kit.json'
    if output.exists() and not overwrite:
        return {
            'status': 'skipped-existing',
            'path': str(output),
            'message': 'Use --overwrite to replace the existing brand kit.',
        }

    kit = json.loads(json.dumps(DEFAULT_BRAND_KIT))
    kit['brand_name'] = brand_name
    kit['tone'] = tone
    kit['colors']['primary'] = primary
    kit['colors']['secondary'] = secondary
    kit['colors']['accent'] = accent
    save_json(output, kit)
    return {'status': 'written', 'path': str(output), 'brand_kit': kit}


def audit_brand_kit(project):
    project_dir = Path(project)
    path = project_dir / 'brand_kit.json'
    kit = load_json(path, {})
    issues = []
    if not kit:
        issues.append('brand-kit-missing')
    if kit and not kit.get('brand_name'):
        issues.append('brand-name-missing')
    if kit and not kit.get('tone'):
        issues.append('tone-missing')
    colors = kit.get('colors', {}) if kit else {}
    for key in ['primary', 'secondary', 'accent', 'background', 'text']:
        if not colors.get(key):
            issues.append(f'color-{key}-missing')
    fonts = kit.get('fonts', {}) if kit else {}
    for key in ['heading', 'body', 'caption']:
        if not fonts.get(key):
            issues.append(f'font-{key}-missing')

    return {
        'project': str(project_dir),
        'path': str(path),
        'status': 'ready' if not issues else 'needs-attention',
        'issues': issues,
        'brand_kit': kit,
    }


def main():
    parser = argparse.ArgumentParser(description='Create or audit an OpenMontage Plus brand kit')
    subparsers = parser.add_subparsers(dest='command', required=True)

    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('--project', default='projects/demo-video')
    create_parser.add_argument('--brand-name', default='OpenMontage Plus Project')
    create_parser.add_argument('--primary', default='#111827')
    create_parser.add_argument('--secondary', default='#2563EB')
    create_parser.add_argument('--accent', default='#FACC15')
    create_parser.add_argument('--tone', default='clear, helpful, modern, confident')
    create_parser.add_argument('--overwrite', action='store_true')

    audit_parser = subparsers.add_parser('audit')
    audit_parser.add_argument('--project', default='projects/demo-video')
    audit_parser.add_argument('--out', default='projects/demo-video/brand_kit_audit.json')

    args = parser.parse_args()
    if args.command == 'create':
        result = create_brand_kit(args.project, args.brand_name, args.primary, args.secondary, args.accent, args.tone, args.overwrite)
    else:
        result = audit_brand_kit(args.project)
        save_json(args.out, result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
