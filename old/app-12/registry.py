import logging
import socket
import json
import os
import requests

from app.decorators.singleton import singleton
from app.settings import settings
from app.utils.connection import connect
from app.settings import settings, initialize_folder

logger = logging.getLogger(__name__)


@singleton
class Registry:

    def __init__(self, name='Default Block', on_connect=None):
        if settings.REGISTRY:
            registry_host = socket.gethostbyname(settings.REGISTRY)
            logger.info(
                f'Block initialized with registry {settings.REGISTRY} [Host: {registry_host}]')
            connect(f'http://{settings.REGISTRY}/api/v1/registry/subscribe?hostname={settings.HOSTNAME}', method='post', data={
                'block_host': settings.HOST,
                'registry': False,
                'default_data_dependency': socket.gethostbyname(settings.DATA_DEPENDENCY),
                'name': name
            }, on_connect=on_connect)
        else:
            logger.info(
                f'Block acts as registry with host: {settings.HOST}')
            initialize_folder('registry')
            for root, dirs, files in os.walk(f'{settings.MOUNT_FOLDER}/registry/'):
                for file in files:
                    if file.endswith('.json'):
                        self.update_registry(file[:-5], {}, {'registered': False})

            self.update_registry(settings.HOSTNAME, {
                'stage': 'pending',
                'block_host': settings.HOST,
                'name': name,
                'registry': True}, {'registered': True})

    
    async def get_data_parent_meta(self):
        if settings.DATA_DEPENDENCY is not None:
            count = requests.get(f'http://{settings.DATA_DEPENDENCY}/api/v1/data/count').json()
            formats = requests.get(f'http://{settings.DATA_DEPENDENCY}/api/v1/data/formats').json()

            return {
                'count': count,
                'formats': formats
            }
    

    def initialize(self):
        pass

    def send_data(self, data):
        if settings.REGISTRY:
            logger.info(f'Sending data to registry')
            connect(
                f'http://{settings.REGISTRY}/api/v1/registry/update?hostname={settings.HOSTNAME}', method='put', data=data)
        else:
            self.update(settings.HOST, data)

    def update_registry(self, host, data={}, override_data={}):
        file_name = f'{settings.MOUNT_FOLDER}/registry/{host}.json'
        overrides = ['data_dependency']

        data_obj = {}

        try:
            if os.path.exists(file_name):
                data_obj = json.load(open(file_name, 'r'))
        except Exception as e:
            logger.error(e)

        data.update(data_obj)
        for key in overrides:
            if data_obj.get(key):
                data[key] = data_obj[key]

        for key in overrides:
            if f'default_{key}' in data.keys() and key not in data.keys():
                data[key] = data[f'default_{key}']

        data.update(override_data)

        json.dump(data, open(
            f'{settings.MOUNT_FOLDER}/registry/{host}.json', 'w'), indent=2)

    def unsubscribe(self):
        connect(
            f'http://{settings.REGISTRY}/api/v1/registry/update?hostname={settings.HOSTNAME}', method='put', data={
                'stage': 'stopped'
            })

    def delete(self, host):
        try:
            os.remove(
                f'{settings.MOUNT_FOLDER}/registry/{host}.json')
        except:
            pass

    def get_graph(self):
        for root, dirs, files in os.walk(f'{settings.MOUNT_FOLDER}/registry/'):
            for file in files:
                if file.endswith('.json'):
                    yield json.load(open(f'{root}/{file}', 'r'))

    def fetch_from_upstream(self, page, count, format):
        return requests.get(f'http://{settings.DATA_DEPENDENCY}/api/v1/data?page={page}&count={count}&format={format}')
