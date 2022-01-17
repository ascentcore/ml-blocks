import pickle

from .custom import Custom

def noop(param1 = None):
    pass

defaults = {
    'name': "Untitled",
    'process_dataset': noop,
    'train': noop,
    'predict': noop,
    'generate_statics': noop
}

class Runtime(Custom):

    model = None

    def __init__(self):
        for prop in defaults.keys():
            if hasattr(self, prop) == False:
                setattr(self, prop, defaults[prop])

        try:
            infile = open('/app/model/model.pkl', 'rb')
            self.model = pickle.load(infile)
            infile.close()
        except:
            pass


runtime = Runtime()
