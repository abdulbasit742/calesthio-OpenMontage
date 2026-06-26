#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

PRIORITY_ORDER = {'high': 0, 'medium': 1, 'low': 2}
STATUS_ORDER = {'open': 0, 'in-progress': 1, 'blocked': 2, 'resolved': 3, 'cancelled': 4}


def load_json(path, default):
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        return json.loads(file_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return default


def save_json(path, data):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2), encoding='utf-8')
    return str(output)


def load_tracker(path):
    data = load_json(path, {})
    if data:
        data.setdefault('revisions', [])
        return data
    return {
        'created_on': date.today().isoformat(),
        'updated_on': date.today().isoformat(),
        'revisions': [],
    }


def next_revision_id(revisions):
    return f'REV-{len(revisions) + 1:03d}'


def add_revision(path, project, source, note, priority, owner, due_date):
    tracker = load_tracker(path)
    revision = {
        'id': next_revision_id(tracker['revisions']),
        'project': project,
        'source': source,
        'note': note,
        'priority': priority,
        'owner': owner,
        'status': 'open',
        'created_on': date.today().isoformat(),
        'due_date': due_date,
        'resolved_on': '',
        'resolution_note': '',
    }
    tracker['revisions'].append(revision)
    tracker['updated_on'] = date.today().isoformat()
    save_json(path, tracker)
    return revision


def update_revision(path, revision_id, status, owner, resolution_note):
    tracker = load_tracker(path)
    updated = None
    for revision in tracker['revisions']:
        if revision['id'] == revision_id:
            if status:
                revision['status'] = status
                if status == 'resolved':
                    revision['resolved_on'] = date.today().isoformat()
            if owner:
                revision['owner'] = owner
            if resolution_note:
                revision['resolution_note'] = resolution_note
            updated = revision
            break
    if not updated:
        raise SystemExit(f'Revision not found: {revision_id}')
    tracker['updated_on'] = date.today().isoformat()
    save_json(path, tracker)
    return updated


def import_from_client_review(project, tracker_path):
    project_dir = Path(project)
    checklist = load_json(project_dir / 'client_review_checklist.json', {})
    tracker = load_tracker(tracker_path)
    imported = []
    existing_notes = {item.get('note') for item in tracker['revisions']}

    for item in checklist.get('items', []):
        needs_revision = item.get('revision_required') is True or item.get('status') in {'changes-requested', 'rejected'}
        comment = item.get('client_comment', '').strip()
        if needs_revision and comment and comment not in existing_notes:
            revision = {
                'id': next_revision_id(tracker['revisions']),
                'project': str(project_dir),
                'source': f"client-checklist:{item.get('id')}",
                'note': comment,
                'priority': 'medium',
                'owner': 'editor',
                'status': 'open',
                'created_on': date.today().isoformat(),
                'due_date': '',
                'resolved_on': '',
                'resolution_note': '',
            }
            tracker['revisions'].append(revision)
            imported.append(revision)
            existing_notes.add(comment)

    tracker['updated_on'] = date.today().isoformat()
    save_json(tracker_path, tracker)
    return {'imported_count': len(imported), 'imported': imported}


def tracker_summary(path):
    tracker = load_tracker(path)
    revisions = tracker['revisions']
    sorted_revisions = sorted(
        revisions,
        key=lambda item: (
            STATUS_ORDER.get(item.get('status', 'open'), 99),
            PRIORITY_ORDER.get(item.get('priority', 'medium'), 99),
            item.get('due_date') or '9999-99-99',
        ),
    )
    return {
        'tracker': str(path),
        'total': len(revisions),
        'open': len([item for item in revisions if item.get('status') == 'open']),
        'in_progress': len([item for item in revisions if item.get('status') == 'in-progress']),
        'blocked': len([item for item in revisions if item.get('status') == 'blocked']),
        'resolved': len([item for item in revisions if item.get('status') == 'resolved']),
        'revisions': sorted_revisions,
    }


def main():
    parser = argparse.ArgumentParser(description='Track client revision requests for OpenMontage Plus projects')
    subparsers = parser.add_subparsers(dest='command', required=True)

    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--tracker', default='revision_tracker.json')
    add_parser.add_argument('--project', default='projects/demo-video')
    add_parser.add_argument('--source', default='manual')
    add_parser.add_argument('--note', required=True)
    add_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium')
    add_parser.add_argument('--owner', default='editor')
    add_parser.add_argument('--due-date', default='')

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('--tracker', default='revision_tracker.json')
    update_parser.add_argument('--id', required=True)
    update_parser.add_argument('--status', choices=['open', 'in-progress', 'blocked', 'resolved', 'cancelled'])
    update_parser.add_argument('--owner')
    update_parser.add_argument('--resolution-note', default='')

    import_parser = subparsers.add_parser('import-review')
    import_parser.add_argument('--project', default='projects/demo-video')
    import_parser.add_argument('--tracker', default='revision_tracker.json')

    summary_parser = subparsers.add_parser('summary')
    summary_parser.add_argument('--tracker', default='revision_tracker.json')

    args = parser.parse_args()
    if args.command == 'add':
        result = add_revision(args.tracker, args.project, args.source, args.note, args.priority, args.owner, args.due_date)
    elif args.command == 'update':
        result = update_revision(args.tracker, args.id, args.status, args.owner, args.resolution_note)
    elif args.command == 'import-review':
        result = import_from_client_review(args.project, args.tracker)
    else:
        result = tracker_summary(args.tracker)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
