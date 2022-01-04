import requests
import pickle

from time import sleep

from .custom import Custom


def noop():
    pass

defaults = {
    'name': "Untitled",
    'loader': 'pandas',
    'process_dataset': noop,
    'train': noop,
    'predict': noop
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


    def store(self, model):
        if model != None:
            self.model = model
            outfile = open('/app/model/model.pkl', 'wb')
            pickle.dump(model, outfile)
            outfile.close()


runtime = Runtime()
