import pytest

from app.resources.helpers import get_geid, async_get_geid


def test_get_id_should_return_global_entity_id_in_result_when_200(httpx_mock, mock_get_geid_request):
    result = get_geid()
    assert result == 'fake_global_entity_id'


def test_get_id_should_raise_exception_when_not_200(httpx_mock):
    httpx_mock.add_response(
        method='GET',
        url='http://10.3.7.222:5062/v1/utility/id',
        status_code=404,
    )
    with pytest.raises(Exception) as excinfo:
        result = get_geid()
    assert str(excinfo.value) == '404: http://10.3.7.222:5062/v1/utility/id'


@pytest.mark.asyncio
async def test_async_get_geid_should_return_200(httpx_mock, mock_get_geid_request):
    result = await async_get_geid()
    assert result == 'fake_global_entity_id'
