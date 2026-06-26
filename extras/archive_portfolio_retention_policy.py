#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

POLICY_INPUTS = {
    'handoff_receipt': 'archive_portfolio_handoff_receipt.json',
    'handoff_note': 'archive_portfolio_handoff_note.json',
    'release_packet': 'archive_portfolio_release_packet.json',
    'snapshot': 'archive_portfolio_snapshot.json',
}

RETENTION_GROUPS = [
    {
        'group': 'executive-records',
        'files': [
            'ARCHIVE_PORTFOLIO_DIGEST.md',
            'ARCHIVE_PORTFOLIO_HANDOFF_NOTE.md',
            'ARCHIVE_PORTFOLIO_HANDOFF_RECEIPT.md',
        ],
        'default_retention': '24 months',
        'review_cadence': 'quarterly',
        'owner_role': 'delivery lead',
    },
    {
        'group': 'package-manifests',
        'files': [
            'ARCHIVE_PORTFOLIO_RELEASE_PACKET.md',
            'ARCHIVE_PORTFOLIO_SNAPSHOT.md',
            'ARCHIVE_PORTFOLIO_PACKLIST.md',
        ],
        'default_retention': '24 months',
        'review_cadence': 'quarterly',
        'owner_role': 'archive owner',
    },
    {
        'group': 'audit-and-readiness',
        'files': [
            'ARCHIVE_TOOLCHAIN_AUDIT.md',
            'ARCHIVE_PORTFOLIO_READINESS_REVIEW.md',
            'ARCHIVE_PORTFOLIO_DASHBOARD.md',
        ],
        'default_retention': '18 months',
        'review_cadence': 'quarterly',
        'owner_role': 'quality reviewer',
    },
    {
        'group': 'workflow-reference',
        'files': [
            'ARCHIVE_PORTFOLIO_RUNBOOK.md',
            'ARCHIVE_PORTFOLIO_OPERATIONS.md',
            'ARCHIVE_TOOLCHAIN_GUIDE.md',
        ],
        'default_retention': 'until replaced',
        'review_cadence': 'after each toolchain change',
        'owner_role': 'toolchain maintainer',
    },
]


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json'}


def input_rows():
    rows = []
    for name, path in POLICY_INPUTS.items():
        data = load_json(path)
        rows.append({
            'name': name,
            'path': path,
            'exists': data is not None,
            'status': data.get('status', 'available') if isinstance(data, dict) else 'missing',
        })
    return rows


def retention_rows():
    rows = []
    for group in RETENTION_GROUPS:
        available = []
        missing = []
        for path in group['files']:
            if Path(path).exists():
                available.append(path)
            else:
                missing.append(path)
        rows.append({
            'group': group['group'],
            'owner_role': group['owner_role'],
            'default_retention': group['default_retention'],
            'review_cadence': group['review_cadence'],
            'files': group['files'],
            'available_files': available,
            'missing_files': missing,
            'available_count': len(available),
            'missing_count': len(missing),
        })
    return rows


def cleanup_rules():
    return [
        'Do not delete release packet, handoff note, or handoff receipt until the client/team confirms receipt.',
        'Keep one frozen snapshot with the matching release packet for each delivered archive package.',
        'Move superseded working files to cold storage only after a newer runbook and snapshot are available.',
        'Never remove source project folders until project-level archive manifests and completion reports exist.',
        'Log any cleanup action in a project or portfolio closeout note before deleting local working files.',
    ]


def build_next_steps(inputs, rows):
    steps = []
    for item in inputs:
        if not item['exists']:
            steps.append(f"Generate missing policy input: {item['path']}")
        elif item['status'] not in {'ready', 'complete', 'ready-for-final-review', 'ready-to-package', 'ready-to-send', 'ready-for-acknowledgement'}:
            steps.append(f"Review policy input status for {item['path']}: {item['status']}")
    for row in rows:
        if row['missing_count']:
            steps.append(f"Review missing files in retention group {row['group']}: {row['missing_count']} missing")
    if not steps:
        steps.append('Approve this retention policy and store it with the handoff receipt.')
    return steps[:12]


def build_policy(projects_root='projects', policy_label='archive-portfolio-retention-policy', owner_name=''):
    inputs = input_rows()
    rows = retention_rows()
    missing_input_count = sum(1 for item in inputs if not item['exists'])
    attention_input_count = sum(
        1 for item in inputs
        if item['exists'] and item['status'] not in {'ready', 'complete', 'ready-for-final-review', 'ready-to-package', 'ready-to-send', 'ready-for-acknowledgement'}
    )
    missing_file_count = sum(row['missing_count'] for row in rows)
    status = 'ready-for-retention-review' if not missing_input_count and not attention_input_count else 'needs-attention'
    return {
        'policy_label': policy_label,
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'owner_name': owner_name,
        'status': status,
        'input_summary': inputs,
        'retention_groups': rows,
        'missing_input_count': missing_input_count,
        'attention_input_count': attention_input_count,
        'missing_file_count': missing_file_count,
        'cleanup_rules': cleanup_rules(),
        'next_steps': build_next_steps(inputs, rows),
    }


def render_markdown(policy):
    lines = [
        '# Archive Portfolio Retention Policy',
        '',
        f"Policy label: **{policy['policy_label']}**",
        f"Generated UTC: {policy['generated_on_utc']}",
        f"Projects root: `{policy['projects_root']}`",
        f"Owner: **{policy['owner_name'] or 'Unassigned'}**",
        f"Status: **{policy['status']}**",
        '',
        '## Input Summary',
        '| Input | Path | Exists | Status |',
        '| --- | --- | --- | --- |',
    ]
    for item in policy['input_summary']:
        lines.append(f"| {item['name']} | `{item['path']}` | {item['exists']} | {item['status']} |")
    lines.extend(['', '## Retention Groups', '| Group | Owner role | Retention | Review cadence | Available | Missing |', '| --- | --- | --- | --- | ---: | ---: |'])
    for row in policy['retention_groups']:
        lines.append(
            f"| {row['group']} | {row['owner_role']} | {row['default_retention']} | {row['review_cadence']} | {row['available_count']} | {row['missing_count']} |"
        )
        if row['files']:
            lines.append('')
            lines.append(f"Files for `{row['group']}`:")
            for path in row['files']:
                marker = 'available' if path in row['available_files'] else 'missing'
                lines.append(f'- `{path}` — {marker}')
            lines.append('')
    lines.extend(['## Cleanup Rules'])
    for rule in policy['cleanup_rules']:
        lines.append(f'- {rule}')
    lines.extend(['', '## Counts'])
    lines.append(f"- Missing policy inputs: {policy['missing_input_count']}")
    lines.append(f"- Inputs needing attention: {policy['attention_input_count']}")
    lines.append(f"- Missing retention files: {policy['missing_file_count']}")
    lines.extend(['', '## Next Steps'])
    for step in policy['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_policy(projects_root, policy_label, owner_name, out_json, out_md):
    policy = build_policy(projects_root, policy_label, owner_name)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(policy, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(policy), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': policy['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio retention policy for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--policy-label', default='archive-portfolio-retention-policy')
    parser.add_argument('--owner-name', default='')
    parser.add_argument('--out-json', default='archive_portfolio_retention_policy.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_RETENTION_POLICY.md')
    args = parser.parse_args()

    result = write_policy(args.projects_root, args.policy_label, args.owner_name, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
