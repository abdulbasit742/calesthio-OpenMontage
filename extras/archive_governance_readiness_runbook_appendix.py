#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

COMMAND = [
    'python',
    'extras/archive_governance_readiness_summary.py',
    '--audit',
    'archive_toolchain_audit.json',
    '--approval',
    'archive_portfolio_governance_approval_record.json',
    '--out-json',
    'archive_governance_readiness_summary.json',
    '--out-md',
    'ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md',
]


def render_command(command):
    return ' '.join(f'"{part}"' if ' ' in part else part for part in command)


def build_appendix(label='archive-governance-final-checkpoint'):
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'label': label,
        'status': 'ready-to-append',
        'step': {
            'name': 'archive-governance-readiness-summary',
            'purpose': 'Build the final archive governance readiness summary from audit and approval records.',
            'command': COMMAND,
            'output': 'ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md',
            'recommended_position': 'Run this after ARCHIVE_PORTFOLIO_GOVERNANCE_APPROVAL_RECORD.md is generated.',
        },
        'final_outputs': [
            'archive_governance_readiness_summary.json',
            'ARCHIVE_GOVERNANCE_READINESS_SUMMARY.md',
        ],
    }


def render_markdown(appendix):
    step = appendix['step']
    lines = [
        '# Archive Governance Readiness Runbook Appendix',
        '',
        f"Generated UTC: {appendix['generated_on_utc']}",
        f"Label: `{appendix['label']}`",
        f"Status: **{appendix['status']}**",
        '',
        '## Final Runbook Step',
        f"Name: `{step['name']}`",
        f"Purpose: {step['purpose']}",
        f"Recommended position: {step['recommended_position']}",
        f"Output: `{step['output']}`",
        '',
        '```bash',
        render_command(step['command']),
        '```',
        '',
        '## Final Outputs',
    ]
    for output in appendix['final_outputs']:
        lines.append(f'- `{output}`')
    lines.append('')
    return '\n'.join(lines)


def write_appendix(label, out_json, out_md):
    appendix = build_appendix(label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(appendix, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(appendix), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': appendix['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive governance readiness runbook appendix')
    parser.add_argument('--label', default='archive-governance-final-checkpoint')
    parser.add_argument('--out-json', default='archive_governance_readiness_runbook_appendix.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_READINESS_RUNBOOK_APPENDIX.md')
    args = parser.parse_args()

    result = write_appendix(args.label, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
