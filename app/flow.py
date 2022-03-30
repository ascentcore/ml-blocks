import requests
from app.db.crud import set_status
from app.runtime import Runtime
import logging
import os
from app.config import settings
from app.loaders import get_loader
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


statics_folder = f'{settings.MOUNT_FOLDER}/statics'


class Flow():

    def __init__(self):
        self.runtime = Runtime()
        self.runtime.statics_folder = statics_folder
        loader_name = os.getenv("LOADER", self.runtime.use_loader)
        loader_class = get_loader(loader_name)
        self.loader = loader_class(self.runtime.loader_config)

        logger.info(f'Initialized block with {loader_class.__name__} instance')

        try:
            os.mkdir(statics_folder)
        except:
            pass

    def report_status(self, db, value):
        set_status(db, value)
        if settings.REGISTRY:
            requests.post(
                f'http://{settings.REGISTRY}/api/v1/status/report', json={
                    "type": "status",
                    "value": value
                })

    def start_data_ingest(self, db, content, append, extras):
        self.report_status(db, 'ingesting')
        self.add_data(content, append)
        self.report_status(db, 'processing')
        self.process_loaded_data(db, extras)
        self.train(db, None)
        self.generate_statics(db)
        self.set_pending(db)

    def train(self, db, request=None):
        self.report_status(db, 'training')
        model = self.runtime.train(self.loader, request)
        self.runtime.store_model(model)
        self.set_pending(db)

    def retrain(self, db, request):
        self.train(db, request)
        self.generate_statics(db)

    def process_loaded_data(self, db, extras, update_status=True):
        self.process_data(extras)
        if update_status:
            self.report_status(db, 'storing')
        self.store_data()

    def set_pending(self, db):
        self.runtime.report_progress(100)
        self.report_status(db, 'pending')

    def add_data(self, content, append):
        logger.info('Started loading data')
        self.loader.load_files(content, append)
        logger.info('Data loading complete')

    def process_data(self, extras=None):
        logger.info('Processing dataset')

        if hasattr(self.runtime, 'process_dataset'):
            self.loader.data = self.runtime.process_dataset(
                self.loader.data, extras)
        else:
            self.loader.default_process()

    def predict(self, db, data, request):
        logger.info('Start predicting...')
        self.report_status(db, 'predicting')
        if self.runtime.model == None:
            self.runtime._load_model()
        result = self.runtime.predict(data, request)
        self.report_status(db, 'pending')
        return result

    def generate_statics(self, db):
        logger.info('Generating statics')
        self.report_status(db, 'statics')
        global statics_folder
        if self.runtime.has_static_generation == True:
            data = self.loader.load_from_store()
            self.runtime.generate_statics(data, statics_folder)
        else:
            logger.info('Block implementation has no statics generation code')
        self.report_status(db, 'pending')

    def list_statics(self):
        # return os.listdir(statics_folder)
        search_dir = statics_folder
        os.chdir(search_dir)
        files = filter(os.path.isfile, os.listdir(search_dir))
        files = [(search_dir, f, os.path.getmtime(os.path.join(search_dir, f))) for f in files] # add path to each file
        files.sort(key=lambda x: -x[2])
        
        return files

    def store_data(self):
        logger.info('Storing')
        self.loader.store()
        logger.info('Dataset processed')
