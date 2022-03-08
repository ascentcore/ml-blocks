import asyncio
import logging
import socket
import requests

from app.db import models, crud, session
from app.constants import DEPENDENCY_DATA_TYPE, DEPENDENCY_LOGIC_TYPE
from app.utils.connection_utils import do_connect
from app.flow import Flow
from .config import settings

logger = logging.getLogger(__name__)


class Registry():

    def __init__(self, flow):
        self.try_register(flow)

    def try_register(self, flow):
        self.host = socket.gethostbyname(socket.gethostname())
        logger.info(f'Subscribing to registry')
        if settings.REGISTRY:
            self.connect(
                f'http://{settings.REGISTRY}/api/v1/pipeline/register?name={flow.runtime.name}')
        else:
            db = session.SessionLocal()
            # db.query(models.Block).delete()
            self.register(db, self.host, 'Registry')
            db.commit()
            db.close()

    def register(self, db, host, name):
        logger.info(f'Registering host: {host} with name: {name}')
        block = models.Block(host=host, name=name)
        db.merge(block)
        db.commit()

    def get_graph(self, db, upstream=None, downstream=None, edge_type=None):
        props = [['upstream', upstream], [
            'downstream', downstream], ['edge_type', edge_type]]

        query = db.query(models.Graph)
        for prop in props:
            if prop[1] != None:
                query = query.filter(getattr(models.Graph, prop[0]) == prop[1])
        return query.all()

    def unregister(self, db, host):
        logger.info(f'Unregistering host: {host}')
        db.query(models.Block).filter_by(host=host).delete()
        db.commit()

    def unsubscribe(self):
        if settings.REGISTRY:
            requests.delete(
                f'http://{settings.REGISTRY}/api/v1/pipeline/register')

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
        if settings.REGISTRY:
            content = requests.get(
                f'http://{settings.REGISTRY}/api/v1/pipeline/graph?upstream={self.host}&edge_type=0')
            dependencies = content.json()
            downstream_deps = [dep['downstream'] for dep in dependencies]
        else:
            dependencies = self.get_graph(
                db, upstream=self.host, edge_type=DEPENDENCY_DATA_TYPE)
            downstream_deps = [dep.downstream for dep in dependencies]

        for dep in downstream_deps:
            logger.info(
                f'Notifying downstream dependency: {dep}')
            requests.post(
                f'http://{dep}/api/v1/pipeline/rebuild')

    def rebuild_from_upstream(self, flow: Flow, db):
        if settings.REGISTRY:
            content = requests.get(
                f'http://{settings.REGISTRY}/api/v1/pipeline/graph?downstream={self.host}&edge_type=0')
            dependencies = content.json()
            upstream_deps = [dep['upstream'] for dep in dependencies]
        else:
            dependencies= self.get_graph(
                db, downstream=self.host, edge_type=DEPENDENCY_DATA_TYPE)
            upstream_deps= [dep.upstream for dep in dependencies]


        for dep in upstream_deps:
            upstream_content_types_req= requests.get(
                f'http://{dep}/api/v1/pipeline/content_types')

            upstream_content_types= upstream_content_types_req.json()
            loader_content_types= flow.loader.export_content_types()

            common_types= list(
                set(upstream_content_types).intersection(loader_content_types))

            if len(common_types) > 0:
                # raise RuntimeError(
                #     "Upstream dependency is not exporting data in a format common to the current block")

                selected_type= common_types[0]

                count_req= requests.get(f'http://{dep}/api/v1/data/count')

                count= int(count_req.text)
                logger.info(
                    f'Upstream dependency has {count} items to process')

                page_size= 100000

                reps= int(count / page_size) + 1

                logger.info(f'Number of iterations to process {reps}')
                crud.set_status(db, 'ingesting')

                for i in range(0, reps):
                    content= requests.get(
                        f'http://{dep}/api/v1/data?page={i}&count={page_size}&format={selected_type}')
                    flow.loader.load_content(content, selected_type, i != 0)
                    flow.process_loaded_data(db, None, False)

                flow.train(db)
                flow.generate_statics(db)
                flow.set_pending(db)
                self.notify_downstream(db)
