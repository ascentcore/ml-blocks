import logging
import os
from app.loaders.pandas import PandasLoader
from app.loaders.archive import ArchiveLoader
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.runtime import Runtime

statics_folder = f'{settings.MOUNT_FOLDER}/statics'

class Flow():
    
    loader = PandasLoader()

    runtime = Runtime()

    def __init__(self):
        try:
            os.mkdir(statics_folder)
        except:
            pass

    def start_data_ingest(self, content, append):
        self.add_data(content, append)
        self.process_data()
        self.store_data()
        self.generate_statics()

    def add_data(self, content, append):
        logger.info('Started loading data')
        self.loader.load_files(content, append)
        logger.info('Data loading complete')

    def process_data(self):
        logger.info('Processing dataset')

        if hasattr(self.runtime, 'process_dataset'):
            self.loader.data = self.runtime.process_dataset(self.loader.data)
        else:
            self.loader.default_process()

    def generate_statics(self):
        global statics_folder
        data = self.loader.load_from_store()
        self.runtime.generate_statics(data, statics_folder)

    def list_statics(self):
        return os.listdir(statics_folder)

    def store_data(self):
        logger.info('Storing')
        self.loader.store()
        logger.info('Dataset processed')


