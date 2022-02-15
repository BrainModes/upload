import pytest


def test_create_new_folder_in_entity_service_return_200(
    mock_get_geid_request, test_client, httpx_mock
):
    folder_name = 'test_core3'

    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.216:5062/v1/neo4j/nodes/Container/query',
        json={'any': 'any'},
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url=f'http://10.3.7.216:5062/v1/neo4j/nodes/Folder/query',
        json=[{
            'name': 'any_name',
            'global_entity_id': 'any_hash',
            'folder_level': 1,
            'labels': ['any_label'],
            'folder_relative_path': './folder'
        }],
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url=f'http://10.3.7.216:5062/v1/neo4j/nodes/Greenroom/query',
        json={},
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.239:5063/v2/resource/lock/',
        json={},
        status_code=200,
    )
    httpx_mock.add_response(
        method='DELETE',
        url='http://10.3.7.239:5063/v2/resource/lock/',
        json={},
        status_code=200,
    )

    # entity service call
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.228:5066/v1/folders',
        json={
            'result': {
                'name': folder_name
            }
        },
        status_code=200,
    )

    result = test_client.post('v1/folder', json={
        'folder_name': folder_name,
        'project_code': 'test_folder_creation',
        'uploader': 'admin',
        'destination_geid': 'any',
        'tags': []
    })
    res = result.json()
    assert result.status_code == 200
    assert res['result']['name'] == folder_name


def test_add_a_subfolder_when_request_body_has_destination_geid(
    mock_get_geid_request, test_client, httpx_mock
):
    '''
        I couldn't find anything specific for a sub folder besides this destination_geid.
        If it confirms that it's only that, we could remove this test and add a parameter to the
        previous test to cover this scenario.
    '''
    folder_name = 'sub_folder03'
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.216:5062/v1/neo4j/nodes/Container/query',
        json={'any': 'any'},
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.216:5062/v1/neo4j/nodes/Folder/query',
        json={},
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url=f'http://10.3.7.216:5062/v1/neo4j/nodes/Greenroom/query',
        json={},
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.239:5063/v2/resource/lock/',
        json={},
        status_code=200,
    )
    httpx_mock.add_response(
        method='DELETE',
        url='http://10.3.7.239:5063/v2/resource/lock/',
        json={},
        status_code=200,
    )
    httpx_mock.add_response(
        method='POST',
        url='http://10.3.7.228:5066/v1/folders',
        json={
            'result': {
                'name': folder_name
            }
        },
        status_code=200,
    )

    result = test_client.post('v1/folder', json={
        'folder_name': folder_name,
        'project_code': 'test_folder_creation',
        'uploader': 'admin',
        'tags': [],
        'destination_geid': 'any_container_unique_id'
    })
    res = result.json()
    assert result.status_code == 200
    assert res['result']['name'] == folder_name
