import socket
import os
import logging

from pydantic import BaseSettings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    RUN_ENV: str = os.getenv("RUN_ENV", "")
    ENV_DEVELOPMENT: bool = RUN_ENV == "development"
    PROJECT_NAME: str = "ML-Blocks API"
    VERSION: str = f"1.0.0 {RUN_ENV}".strip()
    API_V1_STR: str = "/api/v1"
    MOUNT_FOLDER: str = "/app/data"
    MESSAGE_BROKER: str = os.getenv("MESSAGE_BROKER", None)
    DATA_DEPENDENCY: str = os.getenv("DATA_DEPENDENCY", None)
    LOGIC_DEPENDENCIES: str = os.getenv("LOGIC_DEPENDENCIES", None)
    REGISTRY: str = os.getenv("REGISTRY", None)
    HOST: str = socket.gethostbyname(socket.gethostname())

    class Config:
        case_sensitive = True


settings = Settings()


def initialize_folder(name: str):
    mount_folder = f'{settings.MOUNT_FOLDER}/{name}'
    try:
        os.mkdir(mount_folder)
        logger.info(f'{mount_folder} created sucesfully')
    except:
        pass
