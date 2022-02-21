import pickle

from app.custom.block import Block
from .config import settings

def noop(*argv):
    pass

defaults = {
    'initialize': noop,
    'train': noop,
    'predict': noop,
    'generate_statics': noop,
    'loader_config': {},
    'use_loader': None    
}

class Runtime(Block):

    model = None

    has_static_generation = False

    def __init__(self):
        super().__init__()
        for prop in defaults.keys():         
            if hasattr(self, prop) == False:
                setattr(self, prop, defaults[prop])

        self.initialize(settings)
        self.has_static_generation = self.generate_statics != noop
        self._load_model()

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
            pickle.dump(model, open(f'{settings.MOUNT_FOLDER}/model.pkl', 'wb'))