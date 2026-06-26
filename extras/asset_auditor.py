#!/usr/bin/env python3
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    'image': ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg'],
    'video': ['.mp4', '.mov', '.webm', '.mkv'],
    'audio': ['.mp3', '.wav', '.m4a', '.ogg'],
    'text': ['.txt', '.md', '.srt', '.vtt', '.json', '.csv'],
}

REQUIRED_ASSET_DIRS = ['assets', 'scripts', 'renders', 'exports', 'captions']


def extension_category(extension):
    extension = extension.lower()
    for category, extensions in SUPPORTED_EXTENSIONS.items():
        if extension in extensions:
            return category
    return 'unsupported'


def scan_files(project):
    project_path = Path(project)
    files = []
    if not project_path.exists():
        return files
    for item in sorted(project_path.rglob('*')):
        if item.is_file():
            relative = item.relative_to(project_path)
            category = extension_category(item.suffix)
            files.append({
                'path': str(relative),
                'name': item.name,
                'extension': item.suffix.lower() or '[none]',
                'category': category,
                'size_bytes': item.stat().st_size,
            })
    return files


def find_duplicates(files):
    by_name = defaultdict(list)
    for item in files:
        by_name[item['name'].lower()].append(item['path'])
    return {name: paths for name, paths in by_name.items() if len(paths) > 1}


def audit_assets(project):
    project_path = Path(project)
    files = scan_files(project_path)
    counts = Counter(item['category'] for item in files)
    unsupported = [item for item in files if item['category'] == 'unsupported']
    missing_dirs = [folder for folder in REQUIRED_ASSET_DIRS if not (project_path / folder).exists()]
    duplicates = find_duplicates(files)
    total_size = sum(item['size_bytes'] for item in files)

    issues = []
    if not project_path.exists():
        issues.append('project-folder-missing')
    if missing_dirs:
        issues.append('required-folders-missing')
    if unsupported:
        issues.append('unsupported-files-found')
    if duplicates:
        issues.append('duplicate-file-names-found')
    if counts.get('image', 0) == 0 and counts.get('video', 0) == 0:
        issues.append('no-visual-assets-found')

    return {
        'project': str(project_path),
        'exists': project_path.exists(),
        'file_count': len(files),
        'total_size_bytes': total_size,
        'category_counts': dict(counts),
        'missing_directories': missing_dirs,
        'unsupported_files': unsupported,
        'duplicate_names': duplicates,
        'issues': issues,
        'status': 'ready' if not issues else 'needs-attention',
    }


def main():
    parser = argparse.ArgumentParser(description='Audit OpenMontage Plus project assets')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out', default='projects/demo-video/asset_audit.json')
    args = parser.parse_args()

    report = audit_assets(args.project)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
