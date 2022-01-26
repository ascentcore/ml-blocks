import pickle

from .custom import Custom

def noop(*argv):
    pass

defaults = {
    'train': noop,
    'predict': noop,
    'generate_statics': noop
}

class Runtime(Custom):

    model = None

    has_static_generation = False

    def __init__(self):
        for prop in defaults.keys():
            print('###', prop)
            if hasattr(self, prop) == False:
                setattr(self, prop, defaults[prop])

        try:
            infile = open('/app/data/model/model.pkl', 'rb')
            self.model = pickle.load(infile)
            infile.close()
        except:
            pass

        self.has_static_generation = self.generate_statics != noop