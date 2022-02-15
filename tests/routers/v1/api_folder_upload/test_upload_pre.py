import pytest

from unittest.mock import patch


pytestmark = pytest.mark.asyncio  # set the mark to all tests in this file.


async def test_files_jobs_return_400_when_session_id_header_is_missing(
    test_async_client, httpx_mock
):
    response = await test_async_client.post(
        '/v1/files/jobs',
        json={
            'project_code': 'any',
            'operator': 'me',
            'data': [{'resumable_filename': 'any'}]
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


async def test_files_jobs_return_400_when_session_job_type_is_wrong(
    test_async_client, httpx_mock
):
    response = await test_async_client.post(
        '/v1/files/jobs',
        headers={'Session-Id': '1234'},
        json={
            'project_code': 'any',
            'operator': 'me',
            'job_type': 'any',
            'data': [{'resumable_filename': 'any'}]
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        'code': 400,
        'error_msg': 'Invalid job type: any',
        'page': 0,
        'total': 1,
        'num_of_pages': 1,
        'result': []
    }


async def test_files_jobs_return_404_when_project_info_not_found(
    test_async_client, httpx_mock
):
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.216:5062/v1/neo4j/nodes/Container/query',
        json=[],
        status_code=200,
    )

    response = await test_async_client.post(
        '/v1/files/jobs',
        headers={'Session-Id': '1234'},
        json={
            'project_code': 'any',
            'operator': 'me',
            'job_type': 'AS_FILE',
            'data': [{'resumable_filename': 'any'}]
        }
    )
    assert response.status_code == 404
    assert response.json() == {
        'code': 404,
        'error_msg': 'Container or Dataset not found',
        'page': 0,
        'total': 1,
        'num_of_pages': 1,
        'result': {}
    }


async def test_file_with_conflict_path_should_return_409(
    test_async_client, httpx_mock, mock_get_geid_request
):
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.216:5062/v1/neo4j/nodes/Container/query',
        json=[{
            'any': 'any',
            'global_entity_id': 'fake_global_entity_id'
        }],
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url=f'http://10.3.7.216:5062/v1/neo4j/nodes/Core/query',
        json={
            'any': 'any',
        },
        status_code=200,
    )

    response = await test_async_client.post(
        '/v1/files/jobs',
        headers={'Session-Id': '1234'},
        json={
            'project_code': 'any',
            'operator': 'me',
            'job_type': 'AS_FILE',
            'data': [{'resumable_filename': 'any'}]
        }
    )
    assert response.status_code == 409
    assert response.json() == {
        'code': 409,
        'error_msg': '[Invalid File] File Name has already taken by other resources(file/folder)',
        'page': 0,
        'total': 1,
        'num_of_pages': 1,
        'result': {'failed': [{'name': 'any', 'relative_path': '', 'type': 'File'}]}
    }


async def test_files_jobs(
    test_async_client, httpx_mock, mock_get_geid_request, clean_job_from_redis, create_job_folder
):
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.216:5062/v1/neo4j/nodes/Container/query',
        json=[{
            'any': 'any',
            'global_entity_id': 'fake_global_entity_id'
        }],
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url=f'http://10.3.7.216:5062/v1/neo4j/nodes/Core/query',
        json={},
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.239:5063/v2/resource/lock/',
        json={},
        status_code=200,
    )
    response = await test_async_client.post(
        '/v1/files/jobs',
        headers={'Session-Id': '1234'},
        json={
            'project_code': 'any',
            'operator': 'me',
            'job_type': 'AS_FILE',
            'data': [{'resumable_filename': 'any'}]
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
