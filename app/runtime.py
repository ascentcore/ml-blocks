import os
import requests

from .default.process import process_dataset
from .custom import Custom


def noop():
    pass

defaults = {
    'loader': 'pandas',
    'process_dataset': process_dataset,
    'train': noop
}

class Runtime(Custom):

    dependents = []

    dependency = None

    def __init__(self):
        for prop in defaults.keys():
            if hasattr(self, prop) == False:
                setattr(self, prop, defaults[prop])

        dependency = os.environ.get('DEPENDENCY_BLOCK')
        
        if dependency != None:
            self.dependency = dependency
            requests.put(f'http://{dependency}/api/v1/pipe/register')

    def register(self, host):
        self.dependents.append(host)

        

runtime = Runtime()