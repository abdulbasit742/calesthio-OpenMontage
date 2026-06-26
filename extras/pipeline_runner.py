#!/usr/bin/env python3
import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

PIPELINE_STEPS = [
    'export_preset',
    'render_plan',
    'script_timer',
    'caption_builder',
    'metadata_builder',
    'thumbnail_brief',
    'asset_audit',
    'publish_package',
    'quality_score',
    'release_notes',
]


def quote(value):
    return shlex.quote(str(value))


def command_plan(project, preset, topic, audience, duration, wpm):
    project = Path(project)
    voiceover = project / 'scripts' / 'voiceover.txt'
    return [
        {
            'step': 'export_preset',
            'command': f'python extras/export_presets.py write --project {quote(project)} --preset {quote(preset)}',
        },
        {
            'step': 'render_plan',
            'command': f'python extras/render_plan_builder.py --project {quote(project)} --out {quote(project / "render_plan.json")}',
        },
        {
            'step': 'script_timer',
            'command': f'python extras/script_timer.py --project {quote(project)} --script {quote(voiceover)} --wpm {int(wpm)} --target-seconds {int(duration)} --out {quote(project / "script_timing.json")}',
        },
        {
            'step': 'caption_builder',
            'command': f'python extras/caption_builder.py --script {quote(voiceover)} --duration {int(duration)} --out-prefix {quote(project / "captions" / "final")}',
        },
        {
            'step': 'metadata_builder',
            'command': f'python extras/metadata_builder.py --project {quote(project)} --topic {quote(topic)} --audience {quote(audience)} --out {quote(project / "metadata_pack.json")}',
        },
        {
            'step': 'thumbnail_brief',
            'command': f'python extras/thumbnail_brief.py --project {quote(project)} --headline {quote(topic)} --subject {quote(audience)} --out {quote(project / "thumbnail_brief.json")}',
        },
        {
            'step': 'asset_audit',
            'command': f'python extras/asset_auditor.py --project {quote(project)} --out {quote(project / "asset_audit.json")}',
        },
        {
            'step': 'publish_package',
            'command': f'python extras/publish_packager.py --project {quote(project)} --out-dir {quote(project / "publish")}',
        },
        {
            'step': 'quality_score',
            'command': f'python extras/quality_score.py --project {quote(project)} --out {quote(project / "quality_score.json")}',
        },
        {
            'step': 'release_notes',
            'command': f'python extras/release_notes_builder.py --project {quote(project)} --out-json {quote(project / "release_notes.json")} --out-md {quote(project / "RELEASE_NOTES.md")}',
        },
    ]


def run_step(step):
    completed = subprocess.run(step['command'], shell=True, text=True, capture_output=True)
    return {
        'step': step['step'],
        'command': step['command'],
        'returncode': completed.returncode,
        'stdout': completed.stdout[-4000:],
        'stderr': completed.stderr[-4000:],
        'status': 'passed' if completed.returncode == 0 else 'failed',
    }


def execute_pipeline(plan, stop_on_failure):
    results = []
    for step in plan:
        result = run_step(step)
        results.append(result)
        if stop_on_failure and result['returncode'] != 0:
            break
    return results


def build_report(args):
    plan = command_plan(args.project, args.preset, args.topic, args.audience, args.duration, args.wpm)
    report = {
        'project': args.project,
        'mode': 'run' if args.run else 'dry-run',
        'step_count': len(plan),
        'steps': plan,
    }
    if args.run:
        results = execute_pipeline(plan, args.stop_on_failure)
        report['results'] = results
        report['passed_count'] = len([item for item in results if item['status'] == 'passed'])
        report['failed_count'] = len([item for item in results if item['status'] == 'failed'])
        report['status'] = 'passed' if report['failed_count'] == 0 else 'failed'
    else:
        report['status'] = 'planned'
        report['note'] = 'Dry-run only. Add --run to execute commands.'
    return report


def main():
    parser = argparse.ArgumentParser(description='Plan or run an OpenMontage Plus project pipeline')
    parser.add_argument('--project', default='projects/demo-video')
    parser.add_argument('--preset', default='youtube-shorts')
    parser.add_argument('--topic', default='AI product launch')
    parser.add_argument('--audience', default='startup founders')
    parser.add_argument('--duration', type=int, default=45)
    parser.add_argument('--wpm', type=int, default=150)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--stop-on-failure', action='store_true')
    parser.add_argument('--out', default='pipeline_report.json')
    args = parser.parse_args()

    report = build_report(args)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    sys.exit(main())
