import asyncio
import os
import logging
import socket
import requests

from app.db import models, crud
from app.flow import Flow
from app.constants import DEPENDENCY_DATA_TYPE, DEPENDENCY_LOGIC_TYPE

from .config import settings

from app.utils.connection_utils import do_connect

logger = logging.getLogger(__name__)


class Registry():

    connected = False

    dependencies = []

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        logger.info(f'Current IP {self.host}')
    
    def recreate_upstream_connections(self, force = False):
        current_dependencies = []

        def is_registered(host):
            for item in self.dependencies:
                if item[0] == host:
                    return True

            return False

        if settings.DEPENDENCY_BLOCKS:
            dep_list = settings.DEPENDENCY_BLOCKS.split(',')
            for dep in dep_list:
                try:
                    dependency_host = socket.gethostbyname(dep)
                    if not is_registered(dependency_host) or force:
                        logger.info(
                            f'{dependency_host} not registered in {self.dependencies}')
                        current_dependencies.append(
                            [dependency_host, DEPENDENCY_LOGIC_TYPE])
                except:
                    logger.error(f'Unable to find host {dep}')
                    pass

        if settings.UPSTREAM_DATA_BLOCK:
            try:
                dependency_host = socket.gethostbyname(
                    settings.UPSTREAM_DATA_BLOCK)
                if not is_registered(dependency_host) or force:
                    logger.info(
                        f'{dependency_host} not registered in {self.dependencies}')
                    current_dependencies.append(
                        [dependency_host, DEPENDENCY_DATA_TYPE])

            except:
                logger.error(f'Unable to find host {dep}')
                pass

        for dep in current_dependencies:
            self.dependencies.append(dep)
            if dep[1] != DEPENDENCY_LOGIC_TYPE:
                logger.info(
                    f'Registering dependency  downstream={self.host}&upstream={dep[0]}&edge_type={dep[1]}')
                self.connect(
                    f'http://{dep[0]}/api/v1/pipeline/edge?downstream={self.host}&upstream={dep[0]}&edge_type={dep[1]}')

            if settings.REGISTRY:
                logger.info(
                    f'Registering to registry downstream={self.host}&upstream={dep[0]}&edge_type={dep[1]}')
                self.connect(
                    f'http://{settings.REGISTRY}/api/v1/pipeline/edge?downstream={self.host}&upstream={dep[0]}&edge_type={dep[1]}')

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

    def perform_async(self, fn):
        logger.info('Trying to connect to dependency')
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(fn)
        else:
            asyncio.run(fn)

    def create_edge(self, db, upstream, downstream, edge_type):
        logger.info(f'Registering edge: {upstream} -> {downstream}')

        edge = models.Graph(upstream=upstream,
                            downstream=downstream, edge_type=edge_type)
        db.merge(edge)
        db.commit()

    def notify_downstream(self, db):
        dependencies = db.query(models.Graph).all()
        for dep in dependencies:
            if dep.edge_type == DEPENDENCY_DATA_TYPE:
                logger.info(
                    f'Notifying downstream dependency: {dep.downstream}')
                requests.post(
                    f'http://{dep.downstream}/api/v1/pipeline/rebuild')

    def rebuild_from_upstream(self, flow: Flow, db):
        upstream_dep = None
        for dep in self.dependencies:
            if dep[1] == 0:
                upstream_dep = f'http://{dep[0]}'

        if upstream_dep:
            upstream_content_types_req = requests.get(
                f'{upstream_dep}/api/v1/pipeline/content_types')

            upstream_content_types = upstream_content_types_req.json()
            loader_content_types = flow.loader.export_content_types()

            common_types = list(
                set(upstream_content_types).intersection(loader_content_types))

            if len(common_types) > 0:
                # raise RuntimeError(
                #     "Upstream dependency is not exporting data in a format common to the current block")

                selected_type = common_types[0]

                count_req = requests.get(f'{upstream_dep}/api/v1/data/count')

                count = int(count_req.text)
                logger.info(
                    f'Upstream dependency has {count} items to process')

                page_size = 100000

                reps = int(count / page_size) + 1

                logger.info(f'Number of iterations to process {reps}')
                crud.set_status(db, 'ingesting')

                for i in range(0, reps):
                    content = requests.get(
                        f'{upstream_dep}/api/v1/data?page={i}&count={page_size}&format={selected_type}')
                    flow.loader.load_content(content, selected_type, i != 0)
                    flow.process_loaded_data(db, None, False)

                flow.train(db)
                flow.generate_statics(db)
                flow.set_pending(db)
                self.notify_downstream(db)
