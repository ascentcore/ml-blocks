import os
import requests
import pickle

from .default.process import process_dataset
from .custom import Custom


def noop():
    pass

defaults = {
    'loader': 'pandas',
    'process_dataset': process_dataset,
    'train': noop,
    'predict': noop
}

class Runtime(Custom):

    dependents = []

    dependency = None

    model = None

    def __init__(self):
        for prop in defaults.keys():
            if hasattr(self, prop) == False:
                setattr(self, prop, defaults[prop])

        dependency = os.environ.get('DEPENDENCY_BLOCK')
        
        if dependency != None:
            self.dependency = dependency
            requests.put(f'http://{dependency}/api/v1/pipe/register')

        try:
            infile = open('/app/model/model.pkl','rb')
            self.model = pickle.load(infile)
            infile.close()
            print(">>> model loaded")
        except: 
            pass

    def register(self, host):
        self.dependents.append(host)

    def store(self, model):
        if model != None:
            outfile = open('/app/model/model.pkl','wb')
            pickle.dump(model,outfile)
            outfile.close()

        

runtime = Runtime()