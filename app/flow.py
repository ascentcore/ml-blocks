import logging
import os
from app.config import settings
from app.loaders import get_loader
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.runtime import Runtime

statics_folder = f'{settings.MOUNT_FOLDER}/statics'

class Flow():
    
    loader = None

    runtime = Runtime()

    def __init__(self):
        loader_class = get_loader(self.runtime.use_loader)      
        self.loader = loader_class(self.runtime.loader_config)

        logger.info(f'Initialized block with {loader_class.__name__} instance')

        try:
            os.mkdir(statics_folder)
        except:
            pass

    def start_data_ingest(self, content, append, extras):
        self.add_data(content, append)
        self.process_data(extras)
        self.store_data()
        self.generate_statics()

    def add_data(self, content, append):
        logger.info('Started loading data')
        self.loader.load_files(content, append)
        logger.info('Data loading complete')

    def process_data(self, extras = None):
        logger.info('Processing dataset')

        if hasattr(self.runtime, 'process_dataset'):
            self.loader.data = self.runtime.process_dataset(self.loader.data, extras)
        else:
            self.loader.default_process()

    def generate_statics(self):
        logger.info('Generating statics')
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


