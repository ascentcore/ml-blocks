import asyncio
import logging
import socket
import requests
from app.db import models, crud
from app.flow import Flow

from .config import settings

from app.utils.connection_utils import do_connect

logger = logging.getLogger(__name__)


class Registry():

    connected = False

    def __init__(self):
        if settings.DEPENDENCY_BLOCK != None:
            logger.info(f'Dependency Block: {settings.DEPENDENCY_BLOCK}')
            self.connect(
                f'http://{settings.DEPENDENCY_BLOCK}/api/v1/pipeline/register')
        elif settings.REGISTRY != None:
            logger.info(
                f'Registering edge with self to {settings.REGISTRY}: {settings.DEPENDENCY_BLOCK}')
            host = socket.gethostbyname(socket.gethostname())
            self.connect(
                f'http://{settings.REGISTRY}/api/v1/pipeline/edge?upstream={settings.DEPENDENCY_BLOCK}&downstream={host}')

    def register(self, db, downstream_dep):
        logger.info(f'Registering downstream dependency: {downstream_dep}')

        # dependency = db.query(models.Dependency).filter_by(
        #     dependency=downstream_dep).one()
        # if not dependency:
        dependency = models.Dependency(dependency=downstream_dep)
        db.merge(dependency)
        db.commit()
      

        host = socket.gethostbyname(socket.gethostname())
        if settings.REGISTRY != None:
            logger.info(
                f'Registering edge with self to {settings.REGISTRY}: {downstream_dep}, {host}')
            self.connect(
                f'http://{settings.REGISTRY}/api/v1/pipeline/edge?downstream={downstream_dep}')
        else:
            self.create_edge(db, host, downstream_dep)

    def create_edge(self, db, upstream, downstream):
        logger.info(f'Registering edge: {upstream} -> {downstream}')
       
        edge = models.Graph(upstream=upstream, downstream=downstream)
        db.merge(edge)
        db.commit()

    def get_dependency_url(self):
        return f'http://{settings.DEPENDENCY_BLOCK}/api/'

    def connect(self, url):
        logger.info('Trying to connect to dependency')
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(do_connect(url))
        else:
            asyncio.run(do_connect(url))

    def notify_downstream(self, db):
        dependencies = db.query(models.Dependency).all()
        for dep in dependencies:
            logger.info(f'Notifying downstream dependency: {dep.dependency}')
            requests.post(f'http://{dep.dependency}/api/v1/pipeline/rebuild')

    def rebuild_from_upstream(self, flow: Flow, db):
        upstream_dep = self.get_dependency_url()
        upstream_content_types_req = requests.get(
            f'{upstream_dep}v1/pipeline/content_types')

        upstream_content_types = upstream_content_types_req.json()
        loader_content_types = flow.loader.export_content_types()

        common_types = list(
            set(upstream_content_types).intersection(loader_content_types))

        if len(common_types) == 0:
            raise RuntimeError(
                "Upstream dependency is not exporting data in a format common to the current block")

        selected_type = common_types[0]

        count_req = requests.get(f'{upstream_dep}v1/data/count')

        count = int(count_req.text)
        logger.info(f'Upstream dependency has {count} items to process')

        page_size = 100000

        reps = int(count / page_size) + 1

        logger.info(f'Number of iterations to process {reps}')
        crud.set_status(db, 'ingesting')

        for i in range(0, reps):
            content = requests.get(
                f'{upstream_dep}v1/data?page={i}&count={page_size}&format={selected_type}')
            flow.loader.load_content(content, selected_type, i != 0)
            flow.process_loaded_data(db, None, False)

        flow.generate_statics(db)
        flow.set_pending(db)
        self.notify_downstream(db)
