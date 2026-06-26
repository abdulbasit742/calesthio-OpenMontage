#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REPORT_CANDIDATES = [
    'production_manifest.json',
    'render_plan.json',
    'metadata_pack.json',
    'platform_validation.json',
    'quality_score.json',
    'content_risk_check.json',
    'delivery_audit.json',
    'client_review_checklist.json',
    'revision_report.json',
    'approval_gate.json',
    'project_review_summary.json',
    'review_pipeline_report.json',
]


def load_status(path):
    if not path.exists() or path.suffix.lower() != '.json':
        return 'missing'
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return 'invalid-json'
    return data.get('status') or data.get('approval_decision') or 'available'


def file_row(project_dir, relative_path):
    path = project_dir / relative_path
    exists = path.exists()
    stat = path.stat() if exists else None
    modified = None
    if stat:
        modified = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
    return {
        'path': str(path),
        'relative_path': relative_path,
        'exists': exists,
        'size_bytes': stat.st_size if stat else 0,
        'modified_utc': modified,
        'status': load_status(path),
    }


def build_index(project):
    project_dir = Path(project)
    rows = [file_row(project_dir, item) for item in REPORT_CANDIDATES]
    missing = [item for item in rows if not item['exists']]
    invalid = [item for item in rows if item['status'] == 'invalid-json']
    available = [item for item in rows if item['exists'] and item['status'] != 'invalid-json']
    return {
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'needs-attention' if missing or invalid else 'complete',
        'report_count': len(rows),
        'available_count': len(available),
        'missing_count': len(missing),
        'invalid_count': len(invalid),
        'reports': rows,
    }


def render_markdown(index):
    lines = [
        '# Project Report Index',
        '',
        f"Generated UTC: {index['generated_on_utc']}",
        f"Project: `{index['project']}`",
        f"Status: **{index['status']}**",
        f"Reports: **{index['available_count']} available / {index['report_count']} tracked**",
        f"Missing: **{index['missing_count']}**",
        f"Invalid JSON: **{index['invalid_count']}**",
        '',
        '## Reports',
        '| Report | Exists | Status | Size | Modified UTC |',
        '| --- | --- | --- | ---: | --- |',
    ]
    for item in index['reports']:
        modified = item['modified_utc'] or '-'
        lines.append(
            f"| `{item['relative_path']}` | {item['exists']} | {item['status']} | {item['size_bytes']} | {modified} |"
        )
    lines.append('')
    return '\n'.join(lines)


def write_index(project, out_json, out_md):
    index = build_index(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(index, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(index), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': index['status']}


def main():
    parser = argparse.ArgumentParser(description='Build an index of OpenMontage Plus project reports')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/report_index.json')
    parser.add_argument('--out-md', default='projects/demo-video/REPORT_INDEX.md')
    args = parser.parse_args()

    result = write_index(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
