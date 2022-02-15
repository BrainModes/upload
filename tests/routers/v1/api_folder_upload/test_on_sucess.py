import mock
import pytest


pytestmark = pytest.mark.asyncio  # set the mark to all tests in this file.


async def test_on_success_return_400_when_session_id_header_is_missing(
    test_async_client, httpx_mock
):
    response = await test_async_client.post(
        '/v1/files',
        json={
            'project_code': 'any',
            'operator': 'me',
            'resumable_identifier': 'fake_global_entity_id',
            'resumable_filename': 'any',
            'resumable_relative_path': './',
            'resumable_total_chunks': 1,
            'resumable_total_size': 10,
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        'code': 400,
        'error_msg': 'Invalid Session ID: None',
        'page': 0,
        'total': 1,
        'num_of_pages': 1,
        'result': {}
    }


@mock.patch('os.remove')
async def test_on_success_return_200_when_success(
    fake_remove, test_async_client, httpx_mock, create_fake_job, clean_job_from_redis, create_job_folder
):
    httpx_mock.add_response(
        method='DELETE',
        url='http://10.3.7.239:5063/v2/resource/lock/',
        json={},
        status_code=200,
    )
    response = await test_async_client.post(
        '/v1/files',
        headers={'Session-Id': '1234'},
        json={
            'project_code': 'any',
            'operator': 'me',
            'resumable_identifier': 'fake_global_entity_id',
            'resumable_filename': 'any',
            'resumable_relative_path': './',
            'resumable_total_chunks': 1,
            'resumable_total_size': 10,
        }
    )
    assert response.status_code == 200
    result = response.json()['result']
    assert result['session_id'] == '1234'
    assert result['job_id'] == 'fake_global_entity_id'
    assert result['source'] == 'any'
    assert result['action'] == 'data_upload'
    assert result['status'] == 'CHUNK_UPLOADED'
    assert result['operator'] == 'me'
    assert result['payload']['task_id'] == 'fake_global_entity_id'
    assert result['payload']['resumable_identifier'] == 'fake_global_entity_id'
