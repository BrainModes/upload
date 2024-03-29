import httpx

from app.config import ConfigClass

class SrvFileDataMgr():
    '''
    Service for File Data Entity INFO Manager
    '''
    base_url = ConfigClass.DATA_OPS_UTIL

    def __init__(self, logger):
        self.logger = logger

    def create(self, uploader, file_name, path,
               file_size, desc, namespace, project_code, labels,
               dcm_id, minio_bucket, minio_object_path, version_id,
               operator=None, from_parents=None,
               process_pipeline=None, parent_folder_geid=None):
        '''
        Create File Data Entity V2
        '''
        url = self.base_url + "filedata/"
        post_json_form = {
            "uploader": uploader,
            "file_name": file_name,
            "path": path,
            "file_size": file_size,
            "description": desc,
            "namespace": namespace,
            "project_code": project_code,
            "labels": labels,
            ConfigClass.DCM_PIPELINE_ID: dcm_id,
            "parent_folder_geid": parent_folder_geid if parent_folder_geid else "",
            # minio attribute
            "bucket": minio_bucket,
            "minio_object_path": minio_object_path,
            "version_id": version_id
        }
        self.logger.debug('SrvFileDataMgr post_json_form' +
                          str(post_json_form))
        if process_pipeline:
            post_json_form['process_pipeline'] = process_pipeline
        if operator:
            post_json_form['operator'] = operator
        if from_parents:
            post_json_form['parent_query'] = from_parents
        with httpx.Client() as client:
            res = client.post(url=url, json=post_json_form)
        self.logger.debug('SrvFileDataMgr create results: ' + res.text)
        if res.status_code == 200:
            return res.json()
        else:
            error_info = {
                "error": "create meta failed",
                "errorcode": res.status_code,
                "errorpayload": post_json_form,
                "error_message": res.text
            }
            return error_info
