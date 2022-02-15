import httpx

from starlette.concurrency import run_in_threadpool

from app.config import ConfigClass


async def async_lock_resource(resource_key:str, operation:str) -> dict:
    return await run_in_threadpool(lock_resource, resource_key, operation)


async def async_unlock_resource(resource_key:str, operation:str) -> dict:
    return await run_in_threadpool(unlock_resource, resource_key, operation)


def lock_resource(resource_key:str, operation:str) -> dict:
    # operation can be either read or write
    print("====== Lock resource:", resource_key)
    url = ConfigClass.DATA_OPS_UT_V2 + 'resource/lock/'
    post_json = {
        "resource_key": resource_key,
        "operation": operation
    }
    with httpx.Client() as client:
        response = client.post(url, json=post_json)
    if response.status_code != 200:
        raise Exception("resource %s already in used"%resource_key)

    return response.json()


def unlock_resource(resource_key:str, operation:str) -> dict:
    # operation can be either read or write
    print("====== Unlock resource:", resource_key)
    url = ConfigClass.DATA_OPS_UT_V2 + 'resource/lock/'
    post_json = {
        "resource_key": resource_key,
        "operation": operation
    }

    with httpx.Client() as client:
        '''
            httpx.delete doesn't support request body.
            https://www.python-httpx.org/compatibility/#request-body-on-http-methods
        '''
        response = client.request(url=url, method='DELETE', json=post_json)
    if response.status_code != 200:
        raise Exception("Error when unlock resource %s"%resource_key)

    return response.json()
