#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

REVIEW_ITEMS = [
    {
        'id': 'message-accuracy',
        'section': 'Content',
        'question': 'Is the message accurate and aligned with the campaign goal?',
    },
    {
        'id': 'brand-alignment',
        'section': 'Brand',
        'question': 'Do colors, fonts, tone, and visual style match the brand kit?',
    },
    {
        'id': 'platform-fit',
        'section': 'Platform',
        'question': 'Does the video fit the selected platform format and audience?',
    },
    {
        'id': 'captions-readable',
        'section': 'Accessibility',
        'question': 'Are captions readable, correctly timed, and free from spelling mistakes?',
    },
    {
        'id': 'audio-visual-quality',
        'section': 'Quality',
        'question': 'Are audio, visuals, transitions, and pacing acceptable?',
    },
    {
        'id': 'metadata-approved',
        'section': 'Publishing',
        'question': 'Are title, description, CTA, and hashtags approved?',
    },
    {
        'id': 'final-approval',
        'section': 'Sign-off',
        'question': 'Is this project approved for final publishing or delivery?',
    },
]


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def checklist_item(item):
    return {
        **item,
        'status': 'pending',
        'client_comment': '',
        'revision_required': False,
        'owner': 'client',
    }


def build_checklist(project):
    project_dir = Path(project)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    metadata = load_json(project_dir / 'metadata_pack.json', {})
    validation = load_json(project_dir / 'platform_validation.json', {})
    quality = load_json(project_dir / 'quality_score.json', {})
    delivery_audit = load_json(project_dir / 'delivery_audit.json', {})

    project_name = manifest.get('name') or project_dir.name
    platform = metadata.get('platform') or manifest.get('platform') or validation.get('platform') or 'not set'

    return {
        'project': project_name,
        'project_folder': str(project_dir),
        'generated_on': date.today().isoformat(),
        'platform': platform,
        'title': metadata.get('title', project_name),
        'quality_status': quality.get('status', 'not-scored'),
        'quality_score': quality.get('final_score_percent', ''),
        'validation_status': validation.get('status', 'not-checked'),
        'delivery_audit_status': delivery_audit.get('status', 'not-checked'),
        'review_status': 'pending-client-review',
        'items': [checklist_item(item) for item in REVIEW_ITEMS],
        'revision_summary': {
            'revision_required': False,
            'requested_changes': [],
            'approval_decision': 'pending',
        },
    }


def render_markdown(checklist):
    lines = [
        f"# Client Review Checklist: {checklist['project']}",
        '',
        f"Generated: {checklist['generated_on']}",
        f"Platform: **{checklist['platform']}**",
        f"Title: **{checklist['title']}**",
        f"Quality status: **{checklist['quality_status']}**",
        f"Quality score: **{checklist['quality_score']}**",
        f"Validation status: **{checklist['validation_status']}**",
        f"Delivery audit: **{checklist['delivery_audit_status']}**",
        '',
        '## Client Approval Questions',
    ]
    for item in checklist['items']:
        lines.extend([
            '',
            f"### {item['section']} — {item['id']}",
            f"- Question: {item['question']}",
            '- Status: pending',
            '- Client comment:',
            '- Revision required: no',
        ])
    lines.extend([
        '',
        '## Final Decision',
        '- Approval decision: pending',
        '- Requested changes:',
        '- Approved by:',
        '- Approval date:',
        '',
    ])
    return '\n'.join(lines)


def write_checklist(project, out_json, out_md):
    checklist = build_checklist(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(checklist, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(checklist), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': checklist['review_status']}


def main():
    parser = argparse.ArgumentParser(description='Build a client review and sign-off checklist for an OpenMontage Plus delivery')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/client_review_checklist.json')
    parser.add_argument('--out-md', default='projects/demo-video/CLIENT_REVIEW_CHECKLIST.md')
    args = parser.parse_args()

    result = write_checklist(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
