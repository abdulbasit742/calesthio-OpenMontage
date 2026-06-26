#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

RISK_RULES = [
    {
        'id': 'music-license',
        'level': 'warning',
        'terms': ['trending song', 'popular song', 'famous music', 'copyright music'],
        'message': 'Check music licensing before publishing.',
    },
    {
        'id': 'third-party-logo',
        'level': 'warning',
        'terms': ['brand logo', 'company logo', 'celebrity photo', 'screenshot from'],
        'message': 'Confirm permission for third-party visual assets.',
    },
    {
        'id': 'personal-data',
        'level': 'blocker',
        'terms': ['phone number', 'home address', 'email address', 'private message'],
        'message': 'Remove or redact personal information before delivery.',
    },
    {
        'id': 'unverified-claim',
        'level': 'warning',
        'terms': ['guaranteed', '100% result', 'instant success', 'risk free'],
        'message': 'Avoid strong claims unless they are verified and supported.',
    },
    {
        'id': 'medical-financial-claim',
        'level': 'warning',
        'terms': ['cure', 'diagnose', 'investment advice', 'profit guaranteed'],
        'message': 'Review regulated claims carefully before publishing.',
    },
]


def load_text(path):
    file_path = Path(path)
    if not file_path.exists():
        return ''
    return file_path.read_text(encoding='utf-8', errors='ignore')


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def collect_project_text(project_dir):
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    manifest = load_json(project_dir / 'production_manifest.json', {})
    publishing = load_json(project_dir / 'publishing_instructions.json', {})
    script_text = ''
    for candidate in ['scripts/voiceover.txt', 'scripts/captions.txt', 'brief.md']:
        script_text += '\n' + load_text(project_dir / candidate)
    return '\n'.join([
        json.dumps(manifest, ensure_ascii=False),
        json.dumps(metadata, ensure_ascii=False),
        json.dumps(publishing, ensure_ascii=False),
        script_text,
    ])


def scan_text(text):
    lower_text = text.lower()
    findings = []
    for rule in RISK_RULES:
        hits = [term for term in rule['terms'] if term in lower_text]
        if hits:
            findings.append({
                'id': rule['id'],
                'level': rule['level'],
                'matched_terms': hits,
                'message': rule['message'],
            })
    return findings


def build_report(project):
    project_dir = Path(project)
    text = collect_project_text(project_dir)
    findings = scan_text(text)
    blockers = [item for item in findings if item['level'] == 'blocker']
    warnings = [item for item in findings if item['level'] == 'warning']
    return {
        'project': str(project_dir),
        'generated_on': date.today().isoformat(),
        'status': 'blocked' if blockers else ('needs-review' if warnings else 'clear'),
        'blocker_count': len(blockers),
        'warning_count': len(warnings),
        'findings': findings,
        'recommended_next_steps': next_steps(blockers, warnings),
    }


def next_steps(blockers, warnings):
    steps = []
    if blockers:
        steps.append('Fix blocker items before client delivery or publishing.')
    if warnings:
        steps.append('Review warning items and document approvals or edits.')
    if not blockers and not warnings:
        steps.append('No configured content risks were detected.')
    steps.append('This tool is a checklist helper, not legal advice.')
    return steps


def render_markdown(report):
    lines = [
        '# Content Risk Check',
        '',
        f"Generated: {report['generated_on']}",
        f"Project: `{report['project']}`",
        f"Status: **{report['status']}**",
        f"Blockers: **{report['blocker_count']}**",
        f"Warnings: **{report['warning_count']}**",
        '',
        '## Findings',
    ]
    if report['findings']:
        for item in report['findings']:
            terms = ', '.join(item['matched_terms'])
            lines.append(f"- **{item['level']}** `{item['id']}`: {item['message']} Matched: {terms}")
    else:
        lines.append('- None')
    lines.extend(['', '## Recommended Next Steps'])
    for step in report['recommended_next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_report(project, out_json, out_md):
    report = build_report(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': report['status']}


def main():
    parser = argparse.ArgumentParser(description='Scan an OpenMontage Plus project for common content review risks')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/content_risk_check.json')
    parser.add_argument('--out-md', default='projects/demo-video/CONTENT_RISK_CHECK.md')
    args = parser.parse_args()

    result = write_report(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
