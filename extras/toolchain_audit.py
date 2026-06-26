#!/usr/bin/env python3
import argparse
import importlib.util
import json
from collections import Counter
from datetime import date
from pathlib import Path


def load_plus_cli(path):
    cli_path = Path(path)
    if not cli_path.exists():
        raise SystemExit(f'Plus CLI file not found: {cli_path}')
    spec = importlib.util.spec_from_file_location('plus_cli_module', cli_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'TOOLS', {})


def audit_toolchain(cli_path):
    tools = load_plus_cli(cli_path)
    rows = []
    for name, tool in sorted(tools.items()):
        script = Path(tool.get('script', ''))
        rows.append({
            'name': name,
            'area': tool.get('area', 'other'),
            'script': str(script),
            'description': tool.get('description', ''),
            'example': tool.get('example', ''),
            'exists': script.exists(),
        })
    missing = [item for item in rows if not item['exists']]
    area_counts = Counter(item['area'] for item in rows)
    return {
        'generated_on': date.today().isoformat(),
        'cli_path': str(cli_path),
        'status': 'ready' if not missing else 'needs-attention',
        'tool_count': len(rows),
        'missing_count': len(missing),
        'area_counts': dict(sorted(area_counts.items())),
        'missing_tools': missing,
        'tools': rows,
    }


def render_markdown(report):
    lines = [
        '# OpenMontage Plus Toolchain Audit',
        '',
        f"Generated: {report['generated_on']}",
        f"Status: **{report['status']}**",
        f"Tool count: **{report['tool_count']}**",
        f"Missing scripts: **{report['missing_count']}**",
        '',
        '## Area Counts',
    ]
    for area, count in report['area_counts'].items():
        lines.append(f'- {area}: {count}')
    lines.extend([
        '',
        '## Missing Tools',
    ])
    if report['missing_tools']:
        for item in report['missing_tools']:
            lines.append(f"- {item['name']} -> `{item['script']}`")
    else:
        lines.append('- None')
    lines.extend([
        '',
        '## Tool Table',
        '| Name | Area | Exists | Script |',
        '| --- | --- | --- | --- |',
    ])
    for item in report['tools']:
        lines.append(f"| {item['name']} | {item['area']} | {item['exists']} | `{item['script']}` |")
    lines.append('')
    return '\n'.join(lines)


def write_audit(cli_path, out_json, out_md):
    report = audit_toolchain(cli_path)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': report['status'], 'missing_count': report['missing_count']}


def main():
    parser = argparse.ArgumentParser(description='Audit registered OpenMontage Plus CLI tools and missing scripts')
    parser.add_argument('--cli', default='extras/plus_cli.py')
    parser.add_argument('--out-json', default='toolchain_audit.json')
    parser.add_argument('--out-md', default='TOOLCHAIN_AUDIT.md')
    args = parser.parse_args()

    result = write_audit(args.cli, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
