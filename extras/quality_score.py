#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

WEIGHTS = {
    'project_health': 25,
    'asset_audit': 20,
    'script_timing': 15,
    'metadata': 15,
    'review': 15,
    'publish_package': 10,
}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def score_project_health(data):
    if not data:
        return 0, 'project health report missing'
    return min(100, float(data.get('score_percent', 0))), 'project health score imported'


def score_asset_audit(data):
    if not data:
        return 0, 'asset audit missing'
    issues = len(data.get('issues', []))
    score = max(0, 100 - issues * 20)
    return score, f'{issues} asset issue(s) found'


def score_script_timing(data):
    if not data:
        return 0, 'script timing report missing'
    status = data.get('status')
    if status == 'on-target':
        return 100, 'script timing is on target'
    if status in {'too-long', 'too-short'}:
        return 60, data.get('advice', 'script needs timing adjustment')
    return 40, 'script timing status unknown'


def score_metadata(data):
    if not data:
        return 0, 'metadata pack missing'
    required = ['title', 'description', 'hashtags', 'call_to_action']
    present = [key for key in required if data.get(key)]
    score = round((len(present) / len(required)) * 100, 2)
    return score, f'{len(present)}/{len(required)} metadata fields complete'


def score_review(data):
    if not data:
        return 0, 'review checklist missing'
    checks = data.get('checks', [])
    if not checks:
        return 0, 'review checklist has no checks'
    done = [item for item in checks if item.get('done') is True]
    score = round((len(done) / len(checks)) * 100, 2)
    return score, f'{len(done)}/{len(checks)} review checks complete'


def score_publish_package(data):
    if not data:
        return 0, 'publish manifest missing'
    if data.get('status') == 'ready':
        return 100, 'publish package ready'
    missing = data.get('missing_count', 0)
    return max(0, 100 - int(missing) * 12), f'{missing} publish item(s) missing'


def weighted(scores):
    total_weight = sum(WEIGHTS.values())
    value = 0
    for key, weight in WEIGHTS.items():
        value += scores[key]['score'] * weight
    return round(value / total_weight, 2)


def build_quality_report(project):
    project_dir = Path(project)
    sources = {
        'project_health': load_json(project_dir / 'project_health_report.json', {}),
        'asset_audit': load_json(project_dir / 'asset_audit.json', {}),
        'script_timing': load_json(project_dir / 'script_timing.json', {}),
        'metadata': load_json(project_dir / 'metadata_pack.json', {}),
        'review': load_json(project_dir / 'review_checklist.json', {}),
        'publish_package': load_json(project_dir / 'publish' / 'publish_manifest.json', {}),
    }

    scoring_functions = {
        'project_health': score_project_health,
        'asset_audit': score_asset_audit,
        'script_timing': score_script_timing,
        'metadata': score_metadata,
        'review': score_review,
        'publish_package': score_publish_package,
    }

    scores = {}
    for key, function in scoring_functions.items():
        score, note = function(sources[key])
        scores[key] = {'score': round(score, 2), 'weight': WEIGHTS[key], 'note': note}

    final_score = weighted(scores)
    if final_score >= 90:
        status = 'publish-ready'
    elif final_score >= 70:
        status = 'needs-light-review'
    elif final_score >= 45:
        status = 'needs-work'
    else:
        status = 'not-ready'

    return {
        'project': str(project_dir),
        'final_score_percent': final_score,
        'status': status,
        'scores': scores,
        'recommended_next_steps': [note for note in (item['note'] for item in scores.values()) if 'missing' in note or 'issue' in note or 'needs' in note],
    }


def main():
    parser = argparse.ArgumentParser(description='Calculate OpenMontage Plus project quality score')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--out', default='projects/demo-video/quality_score.json')
    args = parser.parse_args()

    report = build_quality_report(args.project)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
