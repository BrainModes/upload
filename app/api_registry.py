from fastapi import FastAPI

from app.routers import api_root
from app.routers.v1 import api_data_upload
from app.routers.v1 import api_folder_creation


def api_registry(app: FastAPI):
    app.include_router(api_root.router)
    app.include_router(api_data_upload.router, prefix='/v1')
    app.include_router(api_folder_creation.router, prefix='/v1')
