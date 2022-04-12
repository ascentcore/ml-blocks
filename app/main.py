import logging
import os
import time
import asyncio

from fastapi import FastAPI, Depends
from fastapi_utils.tasks import repeat_every

from starlette.middleware.cors import CORSMiddleware

from app.flow import Flow
from app.registry import Registry
from app.api.v1 import api_router
from app.settings import settings, initialize_folder

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize folders
initialize_folder('/data')
initialize_folder('/data/listeners')
initialize_folder('/data/statics')
initialize_folder('/data/models')


listeners = {'data': -1, 'model': -1}


def _touch_file(file):
    global listeners
    fn = f'{settings.MOUNT_FOLDER}/data/listeners/{file}'
    logger.info(f'Touching file: {file}')
    with open(fn, 'w') as fp:
        fp.write('')
        fp.close()

    listeners[file] = os.path.getmtime(fn)


for file in listeners.keys():
    fn = f'{settings.MOUNT_FOLDER}/data/listeners/{file}'
    if not os.path.exists(fn):
        with open(fn, 'w') as fp:
            fp.write('')
            fp.close()

    listeners[file] = os.path.getmtime(fn)


def check_file_updates():
    global flow
    global listeners
    for file in listeners.keys():
        timestamp = listeners[file]
        fn = f'{settings.MOUNT_FOLDER}/data/listeners/{file}'
        file_timestamp = os.path.getmtime(fn)

        if file_timestamp != timestamp:
            logger.info(
                f'File {file} timestamp={file_timestamp} -> {timestamp}')
            method_to_call = getattr(flow, f'{file}_update')
            method_to_call()
            listeners[file] = os.path.getmtime(fn)


flow = Flow(_touch_file)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
@repeat_every(seconds=3)  # 1 hour
def remove_expired_tokens_task() -> None:
    check_file_updates()


@app.on_event('shutdown')
async def startup():
    logger.info('Unregistering Block Thread')
