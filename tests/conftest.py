import pytest

from fastapi.testclient import TestClient
from async_asgi_testclient import TestClient as TestAsyncClient

from app.config import ConfigClass
from run import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def test_async_client():
    return TestAsyncClient(app)


@pytest.fixture
def mock_get_geid_request(httpx_mock):
    # configService
    httpx_mock.add_response(
        method='GET',
        url='http://10.3.7.222:5062/v1/utility/id',
        json={
            'result': 'fake_global_entity_id',
        },
        status_code=200,
    )


@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    monkeypatch.setattr(ConfigClass, 'ROOT_PATH', './tests/')
    monkeypatch.setattr(ConfigClass, 'TEMP_BASE', './tests/')
