#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

TOOLS = {
    'new-project': {
        'script': 'extras/project_starter.py',
        'example': 'python extras/project_starter.py --name Demo --duration 45 --platform youtube-shorts',
        'description': 'Create a structured project workspace',
        'area': 'projects',
    },
    'workspace': {
        'script': 'extras/workspace_manager.py',
        'example': 'python extras/workspace_manager.py summary',
        'description': 'List and summarize project workspaces',
        'area': 'projects',
    },
    'presets': {
        'script': 'extras/export_presets.py',
        'example': 'python extras/export_presets.py list',
        'description': 'Show or write platform export presets',
        'area': 'exports',
    },
    'budget': {
        'script': 'extras/budget_gate.py',
        'example': 'python extras/budget_gate.py --budget 2.00',
        'description': 'Approve or block a render plan by budget',
        'area': 'cost-control',
    },
    'history': {
        'script': 'extras/render_history.py',
        'example': 'python extras/render_history.py summary',
        'description': 'Track render events and cost history',
        'area': 'history',
    },
    'review': {
        'script': 'extras/review_checklist.py',
        'example': 'python extras/review_checklist.py template',
        'description': 'Create or check a publish review checklist',
        'area': 'quality',
    },
    'local': {
        'script': 'extras/local_zero_cost.py',
        'example': 'python extras/local_zero_cost.py detect',
        'description': 'Prepare local zero-cost mode',
        'area': 'local',
    },
    'dashboard-data': {
        'script': 'extras/dashboard_data.py',
        'example': 'python extras/dashboard_data.py --projects-root projects --out dashboard_data.json',
        'description': 'Generate dashboard data from project folders',
        'area': 'dashboard',
    },
    'health': {
        'script': 'extras/project_health.py',
        'example': 'python extras/project_health.py all --projects-root projects',
        'description': 'Scan project readiness and missing files',
        'area': 'quality',
    },
    'render-plan': {
        'script': 'extras/render_plan_builder.py',
        'example': 'python extras/render_plan_builder.py --project projects/demo-video',
        'description': 'Build a render plan for a project',
        'area': 'render-pipeline',
    },
    'metadata': {
        'script': 'extras/metadata_builder.py',
        'example': 'python extras/metadata_builder.py --project projects/demo-video --topic Demo --audience founders',
        'description': 'Create a metadata pack for publishing',
        'area': 'publishing',
    },
    'captions': {
        'script': 'extras/caption_builder.py',
        'example': 'python extras/caption_builder.py --text "First line" --duration 30 --out-prefix projects/demo-video/captions/final',
        'description': 'Build SRT/VTT caption files',
        'area': 'captions',
    },
    'thumbnail': {
        'script': 'extras/thumbnail_brief.py',
        'example': 'python extras/thumbnail_brief.py --project projects/demo-video --headline Demo',
        'description': 'Create a thumbnail creative brief',
        'area': 'creative',
    },
    'shotlist': {
        'script': 'extras/shotlist_planner.py',
        'example': 'python extras/shotlist_planner.py --project projects/demo-video --topic Demo',
        'description': 'Plan video scenes and shots',
        'area': 'creative',
    },
    'script-timer': {
        'script': 'extras/script_timer.py',
        'example': 'python extras/script_timer.py --text "Demo script" --target-seconds 30',
        'description': 'Estimate script timing against target duration',
        'area': 'script',
    },
    'assets': {
        'script': 'extras/asset_auditor.py',
        'example': 'python extras/asset_auditor.py --project projects/demo-video',
        'description': 'Audit project assets',
        'area': 'assets',
    },
    'publish-package': {
        'script': 'extras/publish_packager.py',
        'example': 'python extras/publish_packager.py --project projects/demo-video',
        'description': 'Package project files for publishing',
        'area': 'publishing',
    },
    'bootstrap': {
        'script': 'extras/project_bootstrapper.py',
        'example': 'python extras/project_bootstrapper.py --name Demo --topic Demo',
        'description': 'Create a full project scaffold',
        'area': 'projects',
    },
    'quality-score': {
        'script': 'extras/quality_score.py',
        'example': 'python extras/quality_score.py --project projects/demo-video',
        'description': 'Calculate project quality score',
        'area': 'quality',
    },
    'batch-create': {
        'script': 'extras/batch_project_creator.py',
        'example': 'python extras/batch_project_creator.py sample --format csv --out batch_projects.csv',
        'description': 'Create projects in batch from CSV or JSON',
        'area': 'projects',
    },
    'copy-variants': {
        'script': 'extras/copy_variants.py',
        'example': 'python extras/copy_variants.py --project projects/demo-video',
        'description': 'Generate publishing copy variants',
        'area': 'publishing',
    },
    'calendar': {
        'script': 'extras/content_calendar.py',
        'example': 'python extras/content_calendar.py --projects-root projects --out-json content_calendar.json',
        'description': 'Create content calendar files',
        'area': 'calendar',
    },
    'brand-kit': {
        'script': 'extras/brand_kit.py',
        'example': 'python extras/brand_kit.py audit --project projects/demo-video',
        'description': 'Create or audit a project brand kit',
        'area': 'brand',
    },
    'release-notes': {
        'script': 'extras/release_notes_builder.py',
        'example': 'python extras/release_notes_builder.py --project projects/demo-video',
        'description': 'Generate release notes',
        'area': 'documentation',
    },
    'pipeline': {
        'script': 'extras/pipeline_runner.py',
        'example': 'python extras/pipeline_runner.py --project projects/demo-video --preset youtube-shorts',
        'description': 'Run the project production pipeline',
        'area': 'automation',
    },
    'platform-check': {
        'script': 'extras/platform_validator.py',
        'example': 'python extras/platform_validator.py --project projects/demo-video',
        'description': 'Validate platform publishing rules',
        'area': 'platform',
    },
    'status-board': {
        'script': 'extras/status_board.py',
        'example': 'python extras/status_board.py --projects-root projects',
        'description': 'Generate project status board',
        'area': 'dashboard',
    },
    'handoff': {
        'script': 'extras/handoff_packet.py',
        'example': 'python extras/handoff_packet.py --project projects/demo-video',
        'description': 'Build a client handoff packet',
        'area': 'handoff',
    },
    'delivery': {
        'script': 'extras/delivery_zip.py',
        'example': 'python extras/delivery_zip.py --project projects/demo-video',
        'description': 'Build a delivery ZIP archive',
        'area': 'delivery',
    },
    'delivery-audit': {
        'script': 'extras/delivery_audit.py',
        'example': 'python extras/delivery_audit.py --zip projects/demo-video/delivery.zip',
        'description': 'Audit a delivery ZIP archive',
        'area': 'delivery',
    },
    'client-review': {
        'script': 'extras/client_review_checklist.py',
        'example': 'python extras/client_review_checklist.py --project projects/demo-video',
        'description': 'Build a client review checklist',
        'area': 'review',
    },
    'revisions': {
        'script': 'extras/revision_tracker.py',
        'example': 'python extras/revision_tracker.py summary --tracker revision_tracker.json',
        'description': 'Track client revision requests',
        'area': 'review',
    },
    'revision-report': {
        'script': 'extras/revision_report.py',
        'example': 'python extras/revision_report.py --tracker revision_tracker.json',
        'description': 'Generate revision progress reports',
        'area': 'review',
    },
    'approval': {
        'script': 'extras/approval_gate.py',
        'example': 'python extras/approval_gate.py --project projects/demo-video',
        'description': 'Run final approval gate',
        'area': 'approval',
    },
    'publishing': {
        'script': 'extras/publishing_instructions.py',
        'example': 'python extras/publishing_instructions.py --project projects/demo-video',
        'description': 'Generate platform publishing instructions',
        'area': 'publishing',
    },
    'feature-registry': {
        'script': 'extras/feature_registry.py',
        'example': 'python extras/feature_registry.py summary',
        'description': 'Inspect completed, issue-logged, and planned features',
        'area': 'roadmap',
    },
    'roadmap-report': {
        'script': 'extras/roadmap_report.py',
        'example': 'python extras/roadmap_report.py --start 1 --end 50',
        'description': 'Generate roadmap JSON and Markdown reports',
        'area': 'roadmap',
    },
}


def list_tools(area=None):
    rows = []
    for name, tool in sorted(TOOLS.items()):
        if area and tool.get('area') != area:
            continue
        rows.append({
            'name': name,
            'area': tool.get('area', ''),
            'script': tool['script'],
            'description': tool['description'],
            'example': tool['example'],
            'exists': Path(tool['script']).exists(),
        })
    return rows


def list_areas():
    areas = sorted({tool.get('area', 'other') for tool in TOOLS.values()})
    return [{'area': area, 'tool_count': len(list_tools(area))} for area in areas]


def run_tool(name, extra_args):
    if name not in TOOLS:
        raise SystemExit(f'Unknown tool: {name}')
    script = Path(TOOLS[name]['script'])
    if not script.exists():
        raise SystemExit(f'Tool script not found: {script}')
    command = [sys.executable, str(script)] + extra_args
    return subprocess.call(command)


def main():
    parser = argparse.ArgumentParser(description='OpenMontage Plus unified helper CLI')
    sub = parser.add_subparsers(dest='command', required=True)

    list_parser = sub.add_parser('list', help='List all Plus helper tools')
    list_parser.add_argument('--area', default='')

    sub.add_parser('areas', help='List tool areas')

    show_parser = sub.add_parser('show', help='Show one helper tool')
    show_parser.add_argument('tool')

    run_parser = sub.add_parser('run', help='Run one helper tool')
    run_parser.add_argument('tool')
    run_parser.add_argument('args', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.command == 'list':
        print(json.dumps(list_tools(args.area or None), indent=2))
    elif args.command == 'areas':
        print(json.dumps(list_areas(), indent=2))
    elif args.command == 'show':
        if args.tool not in TOOLS:
            raise SystemExit(f'Unknown tool: {args.tool}')
        print(json.dumps(TOOLS[args.tool], indent=2))
    elif args.command == 'run':
        raise SystemExit(run_tool(args.tool, args.args))


if __name__ == '__main__':
    main()
