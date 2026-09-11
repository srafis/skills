"""Offline regression checks. No credentials or network access required."""
from copy import deepcopy
from unittest.mock import patch
from urllib.error import URLError
import clockify_api as api


def check():
    client = api.ClockifyClient('fake', 'workspace')
    existing = {
        'id': 'entry', 'description': 'old', 'projectId': 'project',
        'taskId': 'task', 'billable': True, 'tagIds': ['tag'], 'type': 'REGULAR',
        'timeInterval': {'start': '2026-04-01T09:00:00Z', 'end': '2026-04-01T10:00:00Z'},
        'customFieldValues': None, 'isLocked': False,
    }
    calls = []
    def capture(method, path, payload=None, query=None):
        calls.append((method, path, deepcopy(payload), deepcopy(query)))
        return deepcopy(existing) if method == 'GET' else payload
    client._request = capture
    result = client.update_entry('entry', description='new', billable=False)
    assert result == dict(description='new', projectId='project', taskId='task',
                          billable=False, tagIds=['tag'], type='REGULAR',
                          start=existing['timeInterval']['start'], end=existing['timeInterval']['end'])
    assert [c[0] for c in calls] == ['GET', 'PUT']
    assert client.update_entry('entry', tag_ids=[])['tagIds'] == []
    existing['customFieldValues'] = [{'customFieldId': 'field', 'value': 'keep'}]
    calls.clear()
    try:
        client.update_entry('entry', description='new')
        assert False, 'custom-field update must refuse'
    except RuntimeError:
        assert len(calls) == 1

    calls.clear()
    def paged(method, path, payload=None, query=None):
        calls.append(query.copy())
        return [{'id': str(query['page']), 'name': 'AI'}] if query['page'] <= 2 else []
    client._request = paged
    assert len(client.in_progress(page_size=1)) == 2
    assert [c['page'] for c in calls] == [1, 2, 3]
    calls.clear()
    assert len(client.list_tags(page=2, page_size=1)) == 1
    assert len(calls) == 1
    client.user_id = 'owner'
    assert len(client.list_entries(page_size=1)) == 2
    try:
        client.resolve_tag_ids(tag_names=['AI'])
        assert False, 'ambiguous names must refuse'
    except RuntimeError:
        pass
    client._request = lambda *a, **k: [{'id': 'tag', 'name': 'AI'}] if k.get('query', {}).get('page') == 2 else ([{'id': 'other', 'name': 'AI-ish'}] if k.get('query', {}).get('page') == 1 else [])
    assert client.resolve_tag_ids(tag_names=['AI']) == ['tag']

    calls.clear()
    def identity(method, path, payload=None, query=None):
        calls.append((method, path))
        return {'id': 'owner'}
    client._request = identity
    client.user_id = 'someone-else'
    for operation in (lambda: client.start_timer('work'), client.stop_timer):
        try:
            operation()
            assert False, 'identity mismatch must refuse'
        except RuntimeError:
            assert all(method == 'GET' for method, _ in calls)
    client.user_id = None
    client.stop_timer()
    assert calls[-1] == ('PATCH', '/workspaces/workspace/user/owner/time-entries')
    assert api.build_parser().parse_args(['update', '--id', 'entry', '--description', 'new']).start is None

    real = api.ClockifyClient('fake', 'workspace')
    with patch.object(api.request, 'urlopen', side_effect=URLError('offline')) as mocked:
        try:
            real.get_entry('entry')
            assert False, 'transport failure must be normalized'
        except RuntimeError as exc:
            assert 'before retrying' in str(exc)
        assert mocked.call_args.kwargs['timeout'] == 30
    print('Clockify offline regression checks passed')


if __name__ == '__main__':
    check()
