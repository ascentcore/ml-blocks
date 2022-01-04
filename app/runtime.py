import os
import requests
import pickle
import socket
import asyncio
from time import sleep

from .custom import Custom

from fastapi import Depends
from app.db import models


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

    dependency = None

    model = None

    registered = False

    graph = None

    async def _register(self):
        # await asyncio.sleep(3)
        if self.registered == False:
            try:
                requests.put(f'http://{self.dependency}/api/v1/pipe/register')
                self.registered = True
            except:
                self.retry()
                pass

    def __init__(self):
        for prop in defaults.keys():
            if hasattr(self, prop) == False:
                setattr(self, prop, defaults[prop])

        dependency = os.environ.get('DEPENDENCY_BLOCK')

        if dependency != None:
            self.dependency = dependency
            self.try_register()

        try:
            infile = open('/app/model/model.pkl', 'rb')
            self.model = pickle.load(infile)
            infile.close()
        except:
            pass

    def try_register(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError: 
            loop = None

        if loop and loop.is_running():
            loop.create_task(self._register())
        else:
            asyncio.run(self._register())

    def register(self, host, db):
        dependency = models.Dependency(dependency=host)
        db.add(dependency)
        db.commit()
        db.refresh(dependency)

    def get_root(self):
        root = self.dependency
        if self.dependency:
            potential_root = requests.get(
                f'http://{self.dependency}/api/v1/pipe/root')
            potential_root = potential_root.text
            if potential_root != 'null':
                root = potential_root
            else:
                root = socket.gethostbyname(root)

        return root

    def get_graph(self, children):

        if self.graph != None:
            return self.graph

        root = {"name": self.name, "children": {}}

        for child in children:
            dep = child.dependency
            sub_graph = requests.get(
                f'http://{dep}/api/v1/pipe/graph')            
            root["children"][dep] = sub_graph.json()
            root["children"][dep]['host'] = dep

        self.graph = root
        return root

    def store(self, model):
        if model != None:
            self.model = model
            outfile = open('/app/model/model.pkl', 'wb')
            pickle.dump(model, outfile)
            outfile.close()


runtime = Runtime()
