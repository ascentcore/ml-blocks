import pickle

from app.custom.custom import Custom
from .config import settings

def noop(*argv):
    pass

defaults = {
    'train': noop,
    'predict': noop,
    'generate_statics': noop,
    'loader_config': {},
    'use_loader': None
}

class Runtime(Custom):

    model = None

    has_static_generation = False

    def __init__(self):
        Custom.__init__(self, settings)
        for prop in defaults.keys():         
            if hasattr(self, prop) == False:
                setattr(self, prop, defaults[prop])

        if hasattr(self, 'load_model'):
            self.model = self.load_model()
        else:
            try:
                infile = open('/app/data/model/model.pkl', 'rb')
                self.model = pickle.load(infile)
                infile.close()
            except:
                pass


        self.has_static_generation = self.generate_statics != noop