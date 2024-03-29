from fastapi import APIRouter

from app.config import ConfigClass

router = APIRouter()


@router.get('/')
async def root():
    """Healthcheck route."""

    # settings = get_settings()

    return {
        'status': 'OK',
        'name': ConfigClass.APP_NAME,
        'version': ConfigClass.VERSION,
    }
