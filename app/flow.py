from re import M
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

    def start_data_ingest(self, db, content, append, extras):
        set_status(db, 'ingesting')
        self.add_data(content, append)
        set_status(db, 'processing')
        self.process_loaded_data(db, extras)        
        self.train(db)
        self.generate_statics(db)
        self.set_pending(db)

    def train(self, db):
        set_status(db, 'training')
        model = self.runtime.train(self.loader)
        self.runtime.store_model(model)

    def retrain(self, db):
        self.train(db)
        self.set_pending(db)

    def process_loaded_data(self, db, extras, update_status = True):
        self.process_data(extras)
        if update_status:
            set_status(db, 'storing')
        self.store_data()

    def set_pending(self, db):
        set_status(db, 'pending')

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

    def generate_statics(self, db):
        logger.info('Generating statics')
        set_status(db, 'statics')
        global statics_folder
        if self.runtime.has_static_generation == True:
            data = self.loader.load_from_store()
            self.runtime.generate_statics(data, statics_folder)
        else:
            logger.info('Block implementation has no statics generation code')

    def list_statics(self):
        return os.listdir(statics_folder)

    def store_data(self):
        logger.info('Storing')
        self.loader.store()
        logger.info('Dataset processed')
