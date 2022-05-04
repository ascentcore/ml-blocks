import logging
import os
import pandas as pd
import json

logger = logging.getLogger(__name__)


class PandasLoader:

    dataset = None

    def __init__(self, settings):
        pass

    def _create_or_append_to_dataset(self, data_file):
        current_dataset = None

        try:
            _, file_extension = os.path.splitext(data_file)
            if file_extension == '.csv':
                current_dataset = pd.read_csv(data_file)
        except:
            logger.info(f'Unable to load file {data_file} ')

        if isinstance(current_dataset, pd.DataFrame):
            current_dataset = self.process_fn(self, current_dataset) 
            if isinstance(self.dataset, pd.DataFrame):                
                self.dataset = self.dataset.append(current_dataset)
            else:
                self.dataset = current_dataset

        return current_dataset

    def initialize(self, settings, prev_loader_dataset):
        logger.info('Initializing pandas Loader')
        if prev_loader_dataset:
            for data_file in prev_loader_dataset:
                self._create_or_append_to_dataset(data_file)

        else:
            raise Exception(
                'pandas loader requires a file_loader to provide with data files')

        return self.dataset

    def count(self):
        return len(self.dataset.index)

    def clean(self):
        self.dataset = None

    def load_content(self, file_location, *args):
        return self._create_or_append_to_dataset(file_location)

    def query(self, page=0, count=100, format = ''):
        return json.loads(self.dataset[page * count:page * count + count].to_json(orient='records'))
