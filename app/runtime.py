import pickle

from .custom import Custom

def noop(*argv):
    pass

defaults = {
    # 'process_dataset': noop,
    'train': noop,
    'predict': noop,
    'generate_statics': noop
}

class Runtime(Custom):

    model = None

    def __init__(self):
        print('#### runtime initialized')
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
