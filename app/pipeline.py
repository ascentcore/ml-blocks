import os
import requests
import asyncio
import socket

from fastapi.param_functions import Depends

from app.db import models
from app import deps


class Pipeline:

    dependency = None

    registered = False

    graph = None

    def __init__(self):
        dependency = os.environ.get('DEPENDENCY_BLOCK')

        if dependency != None:
            self.dependency = dependency
            self.try_register()

    async def _register(self):
        # await asyncio.sleep(3)
        if self.registered == False:
            try:
                requests.put(f'http://{self.dependency}/api/v1/pipe/register')
                self.registered = True
            except:
                self.try_register()
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


    def get_graph(self, runtime, db):

        root = {
            "name": runtime.name, 
            "children": {}
        }

        children =  db.query(models.Dependency).all()


        for child in children:
            dep = child.dependency
            sub_graph = requests.get(
                f'http://{dep}/api/v1/pipe/graph')            
            root["children"][dep] = sub_graph.json()
            root["children"][dep]['host'] = dep

        self.graph = root
        return root

    def trigger_downstream(self, db):
        try:
            children =  db.query(models.Dependency).all()
            for child in children:
                requests.get(f'http://{child.dependency}/api/v1/data/refresh')
        except: 
            pass


pipeline = Pipeline()