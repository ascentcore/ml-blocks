import pickle
import requests
import os
import json
import socket
from app.custom.block import Block
from .config import settings


def noop(*argv):
    pass


defaults = {
    'name': os.getenv("BLOCK_NAME", "Pass Through ML Block"),
    'initialize': noop,
    'train': noop,
    'predict': noop,
    'generate_statics': noop,
    'settings_schema': noop,
    'predict_schema': noop,
    'loader_config': {},
    'use_loader': None
}


statics_folder = f'{settings.MOUNT_FOLDER}/statics'


class Runtime(Block):

    model = None

    has_static_generation = False

    def __init__(self):
        super().__init__()
        for prop in defaults.keys():
            if hasattr(self, prop) == False:
                setattr(self, prop, defaults[prop])

        self.initialize(settings, statics_folder)
        self.has_static_generation = self.generate_statics != noop
        self._load_model()
        self.host = socket.gethostbyname(socket.gethostname())

    def report_progress(self, progress):
        if settings.REGISTRY:
            requests.post(
                f'http://{settings.REGISTRY}/api/v1/status/report', json={
                    "type": "progress",
                    "value": progress
                })

    def get_settings(self):
        try:
            return json.load(open(f'{settings.MOUNT_FOLDER}/settings.json'))
        except:
            return {}

    def _load_model(self):
        if hasattr(self, 'load_model'):
            self.model = self.load_model()
        else:
            try:
                infile = open(f'{settings.MOUNT_FOLDER}/model.pkl', 'rb')
                self.model = pickle.load(infile)
                infile.close()
            except:
                pass

        return self.model

    def store_model(self, model):
        self.model = model
        if hasattr(self, 'save_model'):
            self.save_model(model)
        else:
            pickle.dump(model, open(
                f'{settings.MOUNT_FOLDER}/model.pkl', 'wb'))
