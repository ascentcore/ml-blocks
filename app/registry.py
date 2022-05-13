import logging
import socket

from app.decorators.singleton import singleton
from app.settings import settings
from app.utils.connection import connect

logger = logging.getLogger(__name__)


@singleton
class Registry:

    def __init__(self, db):
        if settings.REGISTRY:
            registry_host = socket.gethostbyname(settings.REGISTRY)
            logger.info(f'Block initialized with registry {settings.REGISTRY} [Host: {registry_host}]')
        else:
            logger.info(f'Block acts as registry with host: {settings.HOST}')
