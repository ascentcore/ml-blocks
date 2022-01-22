import logging

from app.loaders.pandas import PandasLoader
from app.loaders.archive import ArchiveLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.runtime import Runtime


class Flow():
    
    loader = ArchiveLoader()

    runtime = Runtime()

    def start_data_ingest(self, content, append):
        self.add_data(content, append)
        self.store_data()

    def add_data(self, content, append):
        logger.info('Started loading data')
        self.loader.load_files(content, append)
        logger.info('Data loading complete')

    def store_data(self):
        logger.info('Processing dataset')

        if hasattr(self.runtime, 'process_dataset'):
            self.loader.data = self.runtime.process_dataset(self.loader.data)
        else:
            self.loader.default_process()

        self.loader.store()
        logger.info('Dataset processed')
