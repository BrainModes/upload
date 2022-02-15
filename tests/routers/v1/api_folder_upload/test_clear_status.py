import pytest


pytestmark = pytest.mark.asyncio  # set the mark to all tests in this file.


async def test_get_status_return_400_when_session_id_header_is_missing(
    test_async_client, httpx_mock
):
    response = await test_async_client.delete(
        '/v1/files/jobs',
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


async def test_get_status_return_200_when_success(
    test_async_client, httpx_mock
):
    response = await test_async_client.delete(
        '/v1/files/jobs',
        headers={'Session-Id': '1234'},
    )
    assert response.status_code == 200
    assert response.json() == {
        'code': 200, 'error_msg': '', 'page': 0, 'total': 1, 'num_of_pages': 1, 'result': {'message': 'Success'}
    }
