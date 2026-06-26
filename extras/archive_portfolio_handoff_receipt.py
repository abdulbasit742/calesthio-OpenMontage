#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

RECEIPT_SOURCES = {
    'handoff_note': 'archive_portfolio_handoff_note.json',
    'release_packet': 'archive_portfolio_release_packet.json',
    'readiness_review': 'archive_portfolio_readiness_review.json',
}

RECEIPT_ATTACHMENTS = [
    'ARCHIVE_PORTFOLIO_HANDOFF_NOTE.md',
    'ARCHIVE_PORTFOLIO_RELEASE_PACKET.md',
    'ARCHIVE_PORTFOLIO_READINESS_REVIEW.md',
    'ARCHIVE_PORTFOLIO_DIGEST.md',
]


def load_json(path):
    file_path = Path(path)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {'status': 'invalid-json'}


def source_rows():
    rows = []
    for name, path in RECEIPT_SOURCES.items():
        data = load_json(path)
        rows.append({
            'name': name,
            'path': path,
            'exists': data is not None,
            'status': data.get('status', 'available') if isinstance(data, dict) else 'missing',
        })
    return rows


def attachment_rows():
    rows = []
    for path in RECEIPT_ATTACHMENTS:
        file_path = Path(path)
        rows.append({
            'path': path,
            'exists': file_path.exists(),
            'size_bytes': file_path.stat().st_size if file_path.exists() else 0,
        })
    return rows


def build_acknowledgement_text(receipt):
    return (
        f"I acknowledge receipt of the archive portfolio handoff package labelled "
        f"{receipt['receipt_label']} with status {receipt['status']}."
    )


def build_next_steps(sources, attachments):
    steps = []
    for row in sources:
        if not row['exists']:
            steps.append(f"Generate missing receipt source: {row['path']}")
        elif row['status'] not in {'ready', 'complete', 'ready-for-final-review', 'ready-to-package', 'ready-to-send'}:
            steps.append(f"Review source status for {row['path']}: {row['status']}")
    for row in attachments:
        if not row['exists']:
            steps.append(f"Attach missing receipt file: {row['path']}")
    if not steps:
        steps.append('Send this receipt with the handoff package and store the signed/confirmed copy.')
    return steps[:12]


def build_receipt(projects_root='projects', recipient_name='', sender_name='', receipt_label='archive-portfolio-receipt'):
    sources = source_rows()
    attachments = attachment_rows()
    missing_sources = [row for row in sources if not row['exists']]
    missing_attachments = [row for row in attachments if not row['exists']]
    attention_sources = [
        row for row in sources
        if row['exists'] and row['status'] not in {'ready', 'complete', 'ready-for-final-review', 'ready-to-package', 'ready-to-send'}
    ]
    status = 'ready-for-acknowledgement' if not missing_sources and not missing_attachments and not attention_sources else 'needs-attention'
    receipt = {
        'receipt_label': receipt_label,
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'projects_root': str(projects_root),
        'recipient_name': recipient_name,
        'sender_name': sender_name,
        'status': status,
        'source_summary': sources,
        'attachments': attachments,
        'missing_source_count': len(missing_sources),
        'missing_attachment_count': len(missing_attachments),
        'attention_source_count': len(attention_sources),
        'next_steps': build_next_steps(sources, attachments),
    }
    receipt['acknowledgement_text'] = build_acknowledgement_text(receipt)
    return receipt


def render_markdown(receipt):
    recipient = receipt['recipient_name'] or 'Recipient'
    sender = receipt['sender_name'] or 'Sender'
    lines = [
        '# Archive Portfolio Handoff Receipt',
        '',
        f"Receipt label: **{receipt['receipt_label']}**",
        f"Generated UTC: {receipt['generated_on_utc']}",
        f"Projects root: `{receipt['projects_root']}`",
        f"Recipient: **{recipient}**",
        f"Sender: **{sender}**",
        f"Status: **{receipt['status']}**",
        '',
        '## Acknowledgement Text',
        receipt['acknowledgement_text'],
        '',
        '## Source Summary',
        '| Source | Path | Exists | Status |',
        '| --- | --- | --- | --- |',
    ]
    for row in receipt['source_summary']:
        lines.append(f"| {row['name']} | `{row['path']}` | {row['exists']} | {row['status']} |")
    lines.extend(['', '## Receipt Attachments', '| File | Exists | Size bytes |', '| --- | --- | ---: |'])
    for row in receipt['attachments']:
        lines.append(f"| `{row['path']}` | {row['exists']} | {row['size_bytes']} |")
    lines.extend(['', '## Counts'])
    lines.append(f"- Missing sources: {receipt['missing_source_count']}")
    lines.append(f"- Missing attachments: {receipt['missing_attachment_count']}")
    lines.append(f"- Sources needing attention: {receipt['attention_source_count']}")
    lines.extend(['', '## Next Steps'])
    for step in receipt['next_steps']:
        lines.append(f'- {step}')
    lines.extend(['', '## Confirmation', '', '- Recipient name:', '- Recipient signature/date:', '- Notes:', ''])
    return '\n'.join(lines)


def write_receipt(projects_root, recipient_name, sender_name, receipt_label, out_json, out_md):
    receipt = build_receipt(projects_root, recipient_name, sender_name, receipt_label)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(receipt), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': receipt['status']}


def main():
    parser = argparse.ArgumentParser(description='Build archive portfolio handoff receipt for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--recipient-name', default='Client Team')
    parser.add_argument('--sender-name', default='OpenMontage Plus')
    parser.add_argument('--receipt-label', default='archive-portfolio-receipt')
    parser.add_argument('--out-json', default='archive_portfolio_handoff_receipt.json')
    parser.add_argument('--out-md', default='ARCHIVE_PORTFOLIO_HANDOFF_RECEIPT.md')
    args = parser.parse_args()

    result = write_receipt(args.projects_root, args.recipient_name, args.sender_name, args.receipt_label, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
