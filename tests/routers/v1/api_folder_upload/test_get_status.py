import pytest


pytestmark = pytest.mark.asyncio  # set the mark to all tests in this file.


async def test_get_files_jobs_return_400_when_session_id_header_is_missing(
    test_async_client, httpx_mock
):
    response = await test_async_client.get(
        '/v1/files/jobs',
        query_string={
            'project_code': 'any',
            'operator': 'me'
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


async def test_get_files_jobs_return_200_when_no_job_found(
    test_async_client, httpx_mock
):
    response = await test_async_client.get(
        '/v1/files/jobs',
        headers={'Session-Id': '1234'},
        query_string={
            'project_code': 'any',
            'operator': 'me'
        }

    )
    assert response.status_code == 200
    assert response.json() == {
        'code': 200, 'error_msg': '', 'page': 0, 'total': 1, 'num_of_pages': 1, 'result': []
    }


async def test_get_files_jobs_return_200_and_job_data_in_results(
    create_fake_job, test_async_client, httpx_mock
):
    response = await test_async_client.get(
        '/v1/files/jobs',
        headers={'Session-Id': '1234'},
        query_string={
            'project_code': 'any',
            'operator': 'me'
        }

    )
    assert response.status_code == 200
    result = response.json()['result'][0]
    assert result['session_id'] == '1234'
    assert result['job_id'] == 'fake_global_entity_id'
    assert result['source'] == 'any'
    assert result['action'] == 'data_upload'
    assert result['status'] == 'PRE_UPLOADED'
    assert result['operator'] == 'me'
    assert result['payload']['task_id'] == 'fake_global_entity_id'
    assert result['payload']['resumable_identifier'] == 'fake_global_entity_id'