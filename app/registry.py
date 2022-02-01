import asyncio
import logging
from turtle import delay
import requests
from app.db import models

from .config import settings

logger = logging.getLogger(__name__)

class Registry():

    downstream_dependencies = []

    connected = False

    def __init__(self):
        if settings.DEPENDENCY_BLOCK != None:
            logger.info(f'Dependency Block: {settings.DEPENDENCY_BLOCK}')
            self.connect()


    def register(self, db, downstream_dep):
        logger.info(f'Registering downstream dependency: {downstream_dep}')
        dependency = models.Dependency(dependency=downstream_dep)
        db.add(dependency)
        db.commit()
        db.refresh(dependency)

    def dependencies(self):
        return self.downstream_dependencies

    async def try_connect(self):
        result = requests.put(f'http://{settings.DEPENDENCY_BLOCK}/api/v1/pipeline/register')
        return result.status_code == 200

    async def do_connect(self):
        trials = 1
        while trials < 4 and self.connected == False:
            logger.info(f'Attempting to connect to dependency {settings.DEPENDENCY_BLOCK}. Attempt {trials}')
            try:
                res = await self.try_connect()
                if res:
                    self.connected = True
                    break
            except:
                pass

            trials = trials + 1
            logger.info(f'Unable to connect to dependency {settings.DEPENDENCY_BLOCK} - waiting 3s')
            await asyncio.sleep(3)

        logger.info(f'Unable to connect to upstream dependency {settings.DEPENDENCY_BLOCK}')

    def connect(self):
        logger.info('Trying to connect to dependency')
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError: 
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.do_connect())
        else:
            asyncio.run(self.do_connect())
    