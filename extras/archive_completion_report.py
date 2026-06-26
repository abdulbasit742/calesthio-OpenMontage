#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_FILES = {
    'archive_manifest': 'project_archive_manifest.json',
    'archive_badge': 'archive_readiness_badge.json',
    'project_closeout': 'project_closeout.json',
    'feedback_report': 'client_feedback_report.json',
}


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def source_status(project_dir):
    rows = []
    for key, filename in SOURCE_FILES.items():
        path = project_dir / filename
        data = load_json(path, {})
        rows.append({
            'key': key,
            'path': filename,
            'exists': path.exists(),
            'status': data.get('status') or data.get('level') or data.get('closeout_status') or 'missing',
        })
    return rows


def build_completion_report(project):
    project_dir = Path(project)
    manifest = load_json(project_dir / SOURCE_FILES['archive_manifest'], {})
    badge = load_json(project_dir / SOURCE_FILES['archive_badge'], {})
    closeout = load_json(project_dir / SOURCE_FILES['project_closeout'], {})
    feedback = load_json(project_dir / SOURCE_FILES['feedback_report'], {})
    sources = source_status(project_dir)
    missing_sources = [row for row in sources if not row['exists']]

    archive_status = manifest.get('status', 'missing')
    badge_level = badge.get('level', 'missing-badge')
    closeout_status = closeout.get('status', manifest.get('closeout_status', 'missing'))
    feedback_status = feedback.get('status', 'missing')
    open_feedback_count = feedback.get('open_count', feedback.get('open_feedback_count', 0))

    ready = (
        not missing_sources
        and archive_status == 'archive-ready'
        and badge_level == 'archive-ready'
        and closeout_status == 'closed'
        and open_feedback_count == 0
    )

    return {
        'project': str(project_dir),
        'generated_on_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'complete' if ready else 'incomplete',
        'archive_status': archive_status,
        'badge_level': badge_level,
        'closeout_status': closeout_status,
        'feedback_status': feedback_status,
        'open_feedback_count': open_feedback_count,
        'available_source_count': len(sources) - len(missing_sources),
        'missing_source_count': len(missing_sources),
        'sources': sources,
        'next_steps': next_steps(archive_status, badge_level, closeout_status, open_feedback_count, missing_sources),
    }


def next_steps(archive_status, badge_level, closeout_status, open_feedback_count, missing_sources):
    steps = []
    for row in missing_sources:
        steps.append(f"Generate missing source file: {row['path']}")
    if closeout_status != 'closed':
        steps.append('Complete project closeout before final archive completion.')
    if open_feedback_count:
        steps.append('Resolve or close open client feedback items.')
    if archive_status != 'archive-ready':
        steps.append('Refresh project_archive_manifest.py until archive status is archive-ready.')
    if badge_level != 'archive-ready':
        steps.append('Refresh archive_readiness_badge.py after archive manifest is ready.')
    if not steps:
        steps.append('Archive completion report is complete. Project can be marked archived.')
    return steps


def render_markdown(report):
    lines = [
        '# Archive Completion Report',
        '',
        f"Generated UTC: {report['generated_on_utc']}",
        f"Project: `{report['project']}`",
        f"Status: **{report['status']}**",
        f"Archive status: **{report['archive_status']}**",
        f"Badge level: **{report['badge_level']}**",
        f"Closeout status: **{report['closeout_status']}**",
        f"Feedback status: **{report['feedback_status']}**",
        f"Open feedback count: **{report['open_feedback_count']}**",
        f"Available sources: **{report['available_source_count']}**",
        f"Missing sources: **{report['missing_source_count']}**",
        '',
        '## Source Files',
        '| Key | Exists | Status | Path |',
        '| --- | --- | --- | --- |',
    ]
    for row in report['sources']:
        lines.append(f"| {row['key']} | {row['exists']} | {row['status']} | `{row['path']}` |")
    lines.extend(['', '## Next Steps'])
    for step in report['next_steps']:
        lines.append(f'- {step}')
    lines.append('')
    return '\n'.join(lines)


def write_report(project, out_json, out_md):
    report = build_completion_report(project)
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    md_path.write_text(render_markdown(report), encoding='utf-8')
    return {'json': str(json_path), 'markdown': str(md_path), 'status': report['status']}


def main():
    parser = argparse.ArgumentParser(description='Build final archive completion report for an OpenMontage Plus project')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out-json', default='projects/demo-video/archive_completion_report.json')
    parser.add_argument('--out-md', default='projects/demo-video/ARCHIVE_COMPLETION_REPORT.md')
    args = parser.parse_args()

    result = write_report(args.project, args.out_json, args.out_md)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
