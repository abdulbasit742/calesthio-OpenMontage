#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TOOLS = {
    'delivery-manifest': {
        'script': 'extras/delivery_manifest_builder.py',
        'example': 'python extras/delivery_manifest_builder.py --project projects/demo-video',
        'description': 'Build known-file delivery manifest for a project',
        'area': 'delivery',
    },
    'handoff-checklist': {
        'script': 'extras/delivery_handoff_checklist.py',
        'example': 'python extras/delivery_handoff_checklist.py --project projects/demo-video',
        'description': 'Build final client handoff checklist',
        'area': 'handoff',
    },
    'client-email': {
        'script': 'extras/client_delivery_email_builder.py',
        'example': 'python extras/client_delivery_email_builder.py --project projects/demo-video --client-name Client --sender-name Team',
        'description': 'Build client delivery email draft',
        'area': 'communication',
    },
    'client-feedback': {
        'script': 'extras/client_feedback_tracker.py',
        'example': 'python extras/client_feedback_tracker.py summary --tracker projects/demo-video/client_feedback_tracker.json',
        'description': 'Track post-delivery client feedback',
        'area': 'feedback',
    },
    'feedback-report': {
        'script': 'extras/client_feedback_report.py',
        'example': 'python extras/client_feedback_report.py --tracker projects/demo-video/client_feedback_tracker.json',
        'description': 'Build client feedback closeout report',
        'area': 'feedback',
    },
    'project-closeout': {
        'script': 'extras/project_closeout_builder.py',
        'example': 'python extras/project_closeout_builder.py --project projects/demo-video',
        'description': 'Build final project closeout report',
        'area': 'closeout',
    },
    'closeout-ops': {
        'script': 'extras/closeout_ops_runner.py',
        'example': 'python extras/closeout_ops_runner.py --project projects/demo-video --dry-run',
        'description': 'Refresh final closeout assets for one project',
        'area': 'closeout',
    },
    'archive-manifest': {
        'script': 'extras/project_archive_manifest.py',
        'example': 'python extras/project_archive_manifest.py --project projects/demo-video',
        'description': 'Build project archive manifest',
        'area': 'archive',
    },
    'archive-ops': {
        'script': 'extras/archive_ops_runner.py',
        'example': 'python extras/archive_ops_runner.py --project projects/demo-video --dry-run',
        'description': 'Run closeout and archive manifest steps for one project',
        'area': 'archive',
    },
    'archive-board': {
        'script': 'extras/archive_status_board.py',
        'example': 'python extras/archive_status_board.py --projects-root projects',
        'description': 'Build global archive readiness board',
        'area': 'archive',
    },
    'portfolio-plan': {
        'script': 'extras/portfolio_archive_plan.py',
        'example': 'python extras/portfolio_archive_plan.py --projects-root projects',
        'description': 'Build safe portfolio archive command plan',
        'area': 'portfolio',
    },
    'toolchain-audit': {
        'script': 'extras/archive_toolchain_audit.py',
        'example': 'python extras/archive_toolchain_audit.py --out-json archive_toolchain_audit.json --out-md ARCHIVE_TOOLCHAIN_AUDIT.md',
        'description': 'Audit archive toolchain scripts, docs, and CLI coverage',
        'area': 'audit',
    },
    'archive-badge': {
        'script': 'extras/archive_readiness_badge.py',
        'example': 'python extras/archive_readiness_badge.py --project projects/demo-video',
        'description': 'Build per-project archive readiness badge',
        'area': 'badge',
    },
    'archive-badge-board': {
        'script': 'extras/archive_badge_board.py',
        'example': 'python extras/archive_badge_board.py --projects-root projects',
        'description': 'Build global archive readiness badge board',
        'area': 'badge',
    },
    'archive-badge-plan': {
        'script': 'extras/archive_badge_plan.py',
        'example': 'python extras/archive_badge_plan.py --projects-root projects',
        'description': 'Build safe per-project archive badge command plan',
        'area': 'badge',
    },
    'archive-completion': {
        'script': 'extras/archive_completion_report.py',
        'example': 'python extras/archive_completion_report.py --project projects/demo-video',
        'description': 'Build final per-project archive completion report',
        'area': 'completion',
    },
    'archive-completion-board': {
        'script': 'extras/archive_completion_board.py',
        'example': 'python extras/archive_completion_board.py --projects-root projects',
        'description': 'Build global archive completion board',
        'area': 'completion',
    },
    'archive-completion-plan': {
        'script': 'extras/archive_completion_plan.py',
        'example': 'python extras/archive_completion_plan.py --projects-root projects',
        'description': 'Build safe per-project archive completion command plan',
        'area': 'completion',
    },
    'portfolio-summary': {
        'script': 'extras/archive_portfolio_summary.py',
        'example': 'python extras/archive_portfolio_summary.py --out-json archive_portfolio_summary.json --out-md ARCHIVE_PORTFOLIO_SUMMARY.md',
        'description': 'Summarize archive boards into one portfolio status report',
        'area': 'portfolio',
    },
    'portfolio-runbook': {
        'script': 'extras/archive_portfolio_runbook.py',
        'example': 'python extras/archive_portfolio_runbook.py --projects-root projects --client-name Client --sender-name Team',
        'description': 'Build the complete safe archive portfolio runbook',
        'area': 'portfolio',
    },
    'portfolio-packlist': {
        'script': 'extras/archive_portfolio_packlist.py',
        'example': 'python extras/archive_portfolio_packlist.py --projects-root projects --out-json archive_portfolio_packlist.json --out-md ARCHIVE_PORTFOLIO_PACKLIST.md',
        'description': 'Build final portfolio and per-project archive file checklist',
        'area': 'portfolio',
    },
    'portfolio-index': {
        'script': 'extras/archive_portfolio_index.py',
        'example': 'python extras/archive_portfolio_index.py --projects-root projects --out-json archive_portfolio_index.json --out-md ARCHIVE_PORTFOLIO_INDEX.md',
        'description': 'Build searchable portfolio and project archive document index',
        'area': 'portfolio',
    },
    'portfolio-dashboard': {
        'script': 'extras/archive_portfolio_dashboard.py',
        'example': 'python extras/archive_portfolio_dashboard.py --projects-root projects --out-json archive_portfolio_dashboard.json --out-md ARCHIVE_PORTFOLIO_DASHBOARD.md',
        'description': 'Build one-page archive portfolio dashboard from summary, boards, packlist, index, and audit files',
        'area': 'portfolio',
    },
    'portfolio-digest': {
        'script': 'extras/archive_portfolio_digest.py',
        'example': 'python extras/archive_portfolio_digest.py --projects-root projects --out-json archive_portfolio_digest.json --out-md ARCHIVE_PORTFOLIO_DIGEST.md',
        'description': 'Build executive archive portfolio digest from dashboard, summary, packlist, and index files',
        'area': 'portfolio',
    },
}


def list_tools(area=None):
    rows = []
    for name, tool in sorted(TOOLS.items()):
        if area and tool['area'] != area:
            continue
        rows.append({
            'name': name,
            'area': tool['area'],
            'script': tool['script'],
            'description': tool['description'],
            'example': tool['example'],
            'exists': Path(tool['script']).exists(),
        })
    return rows


def show_tool(name):
    if name not in TOOLS:
        raise SystemExit(f'Unknown archive tool: {name}')
    tool = dict(TOOLS[name])
    tool['name'] = name
    tool['exists'] = Path(tool['script']).exists()
    return tool


def areas():
    return sorted(set(tool['area'] for tool in TOOLS.values()))


def render_shell_command(name, extra_args):
    tool = show_tool(name)
    command = ['python', tool['script']] + extra_args
    return command


def main():
    parser = argparse.ArgumentParser(description='Focused CLI registry for OpenMontage Plus delivery, closeout, and archive tools')
    sub = parser.add_subparsers(dest='command', required=True)

    list_parser = sub.add_parser('list')
    list_parser.add_argument('--area', default='')

    sub.add_parser('areas')

    show_parser = sub.add_parser('show')
    show_parser.add_argument('name')

    command_parser = sub.add_parser('command')
    command_parser.add_argument('name')
    command_parser.add_argument('args', nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.command == 'list':
        result = list_tools(area=args.area or None)
    elif args.command == 'areas':
        result = areas()
    elif args.command == 'show':
        result = show_tool(args.name)
    else:
        result = render_shell_command(args.name, args.args)

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
