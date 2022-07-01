import logging
import socket
import json
import os

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
                'data_dependency': settings.DATA_DEPENDENCY,
                'data_dependency_host': socket.gethostbyname(settings.DATA_DEPENDENCY),
                'name': name
            }, on_connect=on_connect)
        else:
            logger.info(
                f'Block acts as registry with host: {settings.HOST}')
            initialize_folder('registry')
            for root, dirs, files in os.walk(f'{settings.MOUNT_FOLDER}/registry/'):
                for file in files:
                    if file.endswith('.json'):
                        self.update(file[:-5], {'registered': False})
            logger.info('>>>>>>>>>> <<<<<<<<<<<<<<<')
            logger.info(settings.HOSTNAME)
            self.subscribe(settings.HOSTNAME, {
                           'block_host': settings.HOST,
                           'name': name,
                           'registry': True})

    def initialize(self):
        pass

    def send_data(self, data):
        if settings.REGISTRY:
            logger.info(f'Sending data to registry')
            connect(
                f'http://{settings.REGISTRY}/api/v1/registry/update?hostname={settings.HOSTNAME}', method='put', data=data)
        else:
            self.update(settings.HOST, data)

    def subscribe(self, host, data={}):
        logger.info(f'Subscribed Host: {host}')
        data.update({'registered': True})

        json.dump(data, open(
            f'{settings.MOUNT_FOLDER}/registry/{host}.json', 'w'), indent=2)

        logger.info(f'dumped to {settings.MOUNT_FOLDER}/registry/{host}.json')

    def unsubscribe(self):
        logger.info('************************************')
        logger.info(f'Sending unsubscribe event')
        connect(
            f'http://{settings.REGISTRY}/api/v1/registry/subscribe?hostname={settings.HOSTNAME}', method='delete')

    def delete(self, host):
        try:
            os.remove(
                f'{settings.MOUNT_FOLDER}/registry/{host}.json')
        except:
            pass

    def update(self, host, data={}):
        logger.info(f'Updating Host: {host}')
        data_obj = json.load(
            open(f'{settings.MOUNT_FOLDER}/registry/{host}.json', 'r'))
        data_obj.update(data)
        json.dump(data_obj, open(
            f'{settings.MOUNT_FOLDER}/registry/{host}.json', 'w'), indent=2)

    def get_graph(self):
        for root, dirs, files in os.walk(f'{settings.MOUNT_FOLDER}/registry/'):
            for file in files:
                if file.endswith('.json'):
                    yield json.load(open(f'{root}/{file}', 'r'))
