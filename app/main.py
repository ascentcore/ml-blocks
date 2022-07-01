import logging
import os
import time
import asyncio

from fastapi import FastAPI, Depends
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.deps import get_registry
from app.flow import Flow
from app.registry import Registry
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
initialize_folder('')
initialize_folder('internal')
initialize_folder('listeners')
initialize_folder('statics')
initialize_folder('models')



listeners = {'data': -1, 'model': -1, 'preferences': -1}

for file in listeners.keys():
    fn = f'{settings.MOUNT_FOLDER}/listeners/{file}'
    if not os.path.exists(fn):
        with open(fn, 'w') as fp:
            fp.write('')
            fp.close()

    listeners[file] = int(os.path.getmtime(fn))


def _touch_file(file):
    global listeners
    fn = f'{settings.MOUNT_FOLDER}/listeners/{file}'
    logger.info(f'Touching file: {file}')
    with open(fn, 'w') as fp:
        fp.write('')
        fp.close()

    listeners[file] = int(os.path.getmtime(fn))


def check_file_updates():
    # global flow
    # global listeners
    for file in listeners.keys():
        timestamp = listeners[file]
        fn = f'{settings.MOUNT_FOLDER}/listeners/{file}'
        file_timestamp = int(os.path.getmtime(fn))

        if file_timestamp != timestamp:
            logger.info(
                f'File {file} timestamp={file_timestamp} -> {timestamp}')
            # try:
            method_to_call = getattr(flow, f'{file}_update')
            method_to_call()
            listeners[file] = file_timestamp
            logger.info(f'Updated to new timestamp {timestamp}')
            # except:
            #     logger.error('Unkown error')
            #     pass


flow = Flow(_touch_file)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
@repeat_every(seconds=3)  # 1 hour
def remove_expired_tokens_task() -> None:
    flow.initialize()
    check_file_updates()


@app.on_event('shutdown')
async def shutdown():
    logger.info('Unregistering Block Thread')
    flow.unsubscribe()
