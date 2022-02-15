import json
import os
import pytest
import shutil

# from unittest.mock import AsyncMock

from app.commons.data_providers.redis import SrvRedisSingleton
from app.routers.v1 import api_data_upload


REDIS_CLIENT = SrvRedisSingleton()
BASE_FOLDER_PATH = 'tests'


@pytest.fixture
def clean_job_from_redis():
    '''
        ideally we should run redis locally so we could clean the all keys between tests
    '''
    yield
    REDIS_CLIENT.mdelete_by_prefix('dataaction:1234:fake_global_entity_id:data_upload:any:me')


@pytest.fixture()
def create_job_folder():
    folder_path = f'{BASE_FOLDER_PATH}/fake_global_entity_id'
    os.mkdir(folder_path)
    yield
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


@pytest.fixture
async def create_fake_job(monkeypatch):
    fake_job = {
        "session_id": "1234",
        "job_id": "fake_global_entity_id",
        "source": "any",
        "action": "data_upload",
        "status": "PRE_UPLOADED",
        "project_code": "any",
        "operator": "me",
        "progress": 0, "payload": {
            "task_id": "fake_global_entity_id",
            "resumable_identifier": "fake_global_entity_id",
            "parent_folder_geid": None
        },
        "update_timestamp": "1643041439"
    }
    monkeypatch.setattr(SrvRedisSingleton, 'mget_by_prefix', lambda x, y: [bytes(json.dumps(fake_job), 'utf-8')])
