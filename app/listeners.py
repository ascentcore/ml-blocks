import os
import json
import logging
from app.settings import settings


logger = logging.getLogger(__name__)

listeners = {'data': -1, 'model': -1, 'preferences': -1}
callbacks = {'data': [], 'model': [], 'preferences': []}

for file in listeners.keys():
    fn = f'{settings.MOUNT_FOLDER}/listeners/{file}'
    if not os.path.exists(fn):
        with open(fn, 'w') as fp:
            fp.write('')
            fp.close()

    listeners[file] = int(os.path.getmtime(fn))


def touch_file(file, data):
    global listeners
    fn = f'{settings.MOUNT_FOLDER}/listeners/{file}'
    logger.info(f'Touching file: {file}')
    with open(fn, 'w') as fp:
        fp.write('' if data == None else json.dumps(data, indent = 4))
        fp.close()

    listeners[file] = int(os.path.getmtime(fn))


def load_data_file(file):
    fn = f'{settings.MOUNT_FOLDER}/listeners/{file}'
    logger.info(f'Loading file: {file}')
    with open(fn, 'r') as fp:
        data = json.load(fp)
        fp.close()
    return data

def register_callback(file, fn):
    global callbacks
    callbacks[file].append(fn)

