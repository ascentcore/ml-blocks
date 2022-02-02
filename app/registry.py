import asyncio
import logging
import requests
from app.db import models
from app.flow import Flow

from .config import settings

logger = logging.getLogger(__name__)

class Registry():

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


    def get_dependency_url(self):
        return f'http://{settings.DEPENDENCY_BLOCK}/api/'

    async def try_connect(self):
        dependency = self.get_dependency_url()
        result = requests.put(f'{dependency}v1/pipeline/register')
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

    def notify_downstream(self, db):
        dependencies = db.query(models.Dependency).all()
        for dep in dependencies:
            logger.info(f'Notifying downstream dependency: {dep.dependency}')
            requests.post(f'http://{dep.dependency}/api/v1/pipeline/rebuild')


    def rebuild_from_upstream(self, flow: Flow):
        upstream_dep = self.get_dependency_url()        
        upstream_content_types_req = requests.get(f'{upstream_dep}v1/pipeline/content_types')

        upstream_content_types = upstream_content_types_req.json()
        loader_content_types = flow.loader.export_content_types()
        
        common_types = list(set(upstream_content_types).intersection(loader_content_types))

        if len(common_types) == 0:
            raise RuntimeError("Upstream dependency is not exporting data in a format common to the current block") 

        selected_type = common_types[0]
        
        count_req = requests.get(f'{upstream_dep}v1/data/count')
        
        count = int(count_req.text)
        logger.info(f'Upstream dependency has {count} items to process')

        page_size = 100

        reps = int(count / page_size) + 1

        logger.info(f'Number of iterations to process {reps}')

        for i in range(0, reps):
            content = requests.get(f'{upstream_dep}v1/data?page={i}&count={page_size}&format={selected_type}')
            flow.loader.load_content(content, selected_type, i != 0)
            flow.process_loaded_data(None)

        
    