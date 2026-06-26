#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def load_jsonl(path):
    file_path = Path(path)
    if not file_path.exists():
        return []
    rows = []
    for line in file_path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                rows.append({'status': 'invalid-jsonl-row', 'raw': line})
    return rows


def project_summary(project_dir):
    project_dir = Path(project_dir)
    manifest = load_json(project_dir / 'production_manifest.json', {})
    preset = load_json(project_dir / 'export_preset.json', {})
    review = load_json(project_dir / 'review_checklist.json', {})
    local_mode = load_json(project_dir / 'local_zero_cost.json', {})

    checks = review.get('checks', [])
    total_checks = len(checks)
    done_checks = len([item for item in checks if item.get('done') is True])
    readiness = 0 if total_checks == 0 else round((done_checks / total_checks) * 100, 2)

    return {
        'folder': project_dir.name,
        'name': manifest.get('name', project_dir.name),
        'platform': manifest.get('platform', preset.get('platform', 'unknown')),
        'duration_seconds': manifest.get('duration_seconds', 0),
        'status': manifest.get('status', 'unknown'),
        'export_preset': preset.get('platform', 'missing'),
        'review_score_percent': readiness,
        'local_zero_cost_enabled': local_mode.get('allow_paid_api_calls') is False,
    }


def build_dashboard(projects_root, history_file):
    root = Path(projects_root)
    root.mkdir(exist_ok=True)
    projects = [project_summary(item) for item in sorted(root.iterdir()) if item.is_dir()]
    history = load_jsonl(history_file)
    total_cost = round(sum(float(item.get('cost_usd', 0) or 0) for item in history), 4)
    completed_renders = len([item for item in history if item.get('status') == 'completed'])

    return {
        'project_count': len(projects),
        'completed_renders': completed_renders,
        'total_render_cost_usd': total_cost,
        'projects': projects,
        'latest_history': history[-10:],
    }


def main():
    parser = argparse.ArgumentParser(description='Build dashboard-ready JSON for OpenMontage Plus')
    parser.add_argument('--projects-root', default='projects')
    parser.add_argument('--history', default='render_history.jsonl')
    parser.add_argument('--out', default='dashboard_data.json')
    args = parser.parse_args()

    data = build_dashboard(args.projects_root, args.history)
    Path(args.out).write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
