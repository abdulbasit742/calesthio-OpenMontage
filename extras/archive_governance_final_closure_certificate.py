#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def read_json(path_text):
    path = Path(path_text)
    if not path.exists():
        return {'load_status': 'missing', 'path': path_text, 'data': {}}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'load_status': 'invalid-json', 'path': path_text, 'data': {}}
    return {'load_status': 'loaded', 'path': path_text, 'data': data if isinstance(data, dict) else {}}


def build_certificate(acknowledgement_path, certificate_id, owner, closing_note):
    acknowledgement = read_json(acknowledgement_path)
    ack_data = acknowledgement['data']
    ack_status = ack_data.get('acknowledgement_status')
    ready = acknowledgement['load_status'] == 'loaded' and ack_status == 'acknowledged'
    status = 'closed' if ready else 'needs-attention'
    return {
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'certificate_id': certificate_id,
        'owner': owner,
        'closing_note': closing_note,
        'closure_status': status,
        'acknowledgement_path': acknowledgement_path,
        'acknowledgement_load_status': acknowledgement['load_status'],
        'acknowledgement_status': ack_status,
        'package_id': ack_data.get('package_id'),
        'reviewer_name': ack_data.get('reviewer_name'),
        'reviewer_role': ack_data.get('reviewer_role'),
        'decision': ack_data.get('decision'),
        'next_steps': next_steps(status, acknowledgement['load_status'], ack_status),
    }


def next_steps(status, load_status, ack_status):
    if status == 'closed':
        return [
            'Store this closure certificate with the final archive governance package.',
            'No further delivery action is required unless a reviewer reopens the package.',
        ]
    if load_status != 'loaded':
        return ['Regenerate or locate the final delivery acknowledgement before closure.']
    if ack_status != 'acknowledged':
        return ['Resolve the final delivery acknowledgement before closure.']
    return ['Review the final archive package before creating a closure certificate.']


def render_markdown(certificate):
    lines = [
        '# Archive Governance Final Closure Certificate',
        '',
        f"Generated UTC: {certificate['generated_on_utc']}",
        f"Certificate ID: **{certificate['certificate_id']}**",
        f"Closure status: **{certificate['closure_status']}**",
        f"Owner: **{certificate['owner']}**",
        f"Package ID: **{certificate['package_id']}**",
        f"Reviewer: **{certificate['reviewer_name']}**",
        f"Reviewer role: **{certificate['reviewer_role']}**",
        f"Reviewer decision: **{certificate['decision']}**",
        f"Acknowledgement source: `{certificate['acknowledgement_path']}`",
        f"Acknowledgement status: **{certificate['acknowledgement_status']}**",
        '',
        '## Closing Note',
        certificate['closing_note'] or '-',
        '',
        '## Next Steps',
    ]
    for item in certificate['next_steps']:
        lines.append(f'- {item}')
    lines.append('')
    return '\n'.join(lines)


def write_certificate(acknowledgement, certificate_id, owner, closing_note, out_json, out_md):
    certificate = build_certificate(acknowledgement, certificate_id, owner, closing_note)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(certificate, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(certificate), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': certificate['closure_status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive governance closure certificate')
    parser.add_argument('--acknowledgement', default='archive_governance_final_delivery_acknowledgement.json')
    parser.add_argument('--certificate-id', default='archive-governance-final-closure')
    parser.add_argument('--owner', default='Archive Owner')
    parser.add_argument('--closing-note', default='Final archive governance delivery is closed after reviewer acknowledgement.')
    parser.add_argument('--out-json', default='archive_governance_final_closure_certificate.json')
    parser.add_argument('--out-md', default='ARCHIVE_GOVERNANCE_FINAL_CLOSURE_CERTIFICATE.md')
    args = parser.parse_args()

    result = write_certificate(args.acknowledgement, args.certificate_id, args.owner, args.closing_note, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
