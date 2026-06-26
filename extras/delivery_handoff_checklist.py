#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_ITEMS = [
    {'id': 'delivery-manifest', 'label': 'Delivery manifest generated', 'source': 'delivery_manifest.json'},
    {'id': 'readiness-badge', 'label': 'Delivery readiness badge generated', 'source': 'delivery_readiness_badge.json'},
    {'id': 'approval-gate', 'label': 'Approval gate report generated', 'source': 'approval_gate.json'},
    {'id': 'metadata', 'label': 'Publishing metadata included', 'source': 'metadata_pack.json'},
    {'id': 'publishing-instructions', 'label': 'Publishing instructions included', 'source': 'publishing_instructions.json'},
    {'id': 'delivery-zip', 'label': 'Delivery ZIP package included', 'source': 'delivery.zip'},
]


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def item_status(project_dir, item):
    source_path = project_dir / item['source']
    exists = source_path.exists()
    status = 'complete' if exists else 'missing'
    if item['id'] == 'readiness-badge' and exists:
        badge = load_json(source_path, {})
        status = 'complete' if badge.get('message') == 'ready' else 'needs-review'
    if item['id'] == 'approval-gate' and exists:
        gate = load_json(source_path, {})
        status = 'complete' if gate.get('status') == 'approved-for-delivery' else 'needs-review'
    return {
        'id': item['id'],
        'label': item['label'],
        'source': item['source'],
        'exists': exists,
        'status': status,
    }


def build_checklist(project):
    project_dir = Path(project)
    items = [item_status(project_dir, item) for item in REQUIRED_ITEMS]
    missing = [item for item in items if item['status'] == 'missing']
    needs_review = [item for item in items if item['status'] == 'needs-review']
    status = 'ready-for-handoff' if not missing and not needs_review else 'needs-attention'
    return {
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': status,
        'complete_count': len([item for item in items if item['status'] == 'complete']),
        'missing_count': len(missing),
        'needs_review_count': len(needs_review),
        'items': items,
        'next_steps': next_steps(missing, needs_review),
    }


def next_steps(missing, needs_review):
    steps = []
    if missing:
        steps.append('Generate missing delivery files before sending to client.')
    if needs_review:
        steps.append('Review approval/readiness outputs before handoff.')
    if not missing and not needs_review:
        steps.append('Package and send the final delivery to the client.')
    return steps


def render_markdown(checklist):
    lines = [
        '# Delivery Handoff Checklist',
        '',
        f"Generated UTC: {checklist['generated_on_utc']}",
        f"Project: `{checklist['project']}`",
        f"Status: **{checklist['status']}**",
        f"Complete: **{checklist['complete_count']}**",
        f"Missing: **{checklist['missing_count']}**",
        f"Needs review: **{checklist['needs_review_count']}**",
        '',
        '## Checklist',
        '| Item | Status | Source |',
        '| --- | --- | --- |',
    ]
    for item in checklist['items']:
        lines.append(f"| {item['label']} | {item['status']} | `{item['source']}` |")
    lines.extend(['', '## Next Steps'])
    for step in checklist['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_checklist(project, out_json, out_md):
    checklist = build_checklist(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(checklist, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(checklist), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': checklist['status']}


def main():
    parser = argparse.ArgumentParser(description='Build a final delivery handoff checklist for an OpenMontage Plus project')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/delivery_handoff_checklist.json')
    parser.add_argument('--out-md', default='projects/demo-video/DELIVERY_HANDOFF_CHECKLIST.md')
    args = parser.parse_args()

    result = write_checklist(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
