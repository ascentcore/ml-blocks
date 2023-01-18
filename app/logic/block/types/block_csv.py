from threading import Lock

import pandas as pd

from app.generic_components.csv_wrapper.wrapper_csv import WrapperCSV
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.base import BlockBase
from app.logic.block.filters.filter import bigger_then


class BlockCSV(BlockBase):

    def __init__(self, loader, storage):
        super().__init__(name="CSV Block",
                         loader=loader,
                         storage=storage)
        self.log = LogBase.log(self.__class__.__name__)
        self.__lock = Lock()

    @property
    def lock(self):
        return self.__lock

    def itemize(self, data):
        return WrapperCSV.yield_rows(path=data)

    def filter(self, item):
        return bigger_then(variable=item[1], threshold=0.2)  # FIXME

    async def train(self):
        self.log.info('')
        df = pd.DataFrame(self.storage.query(0, self.storage.count()))
        self.log.info(df)

    def load_data(self, from_scratch=False):
        if from_scratch:
            self.log.debug(f'Clearing storage')
            self.clear_storage()

        for data in self.loader.entries():
            if self.storage.is_completed(data):
                self.log.debug(f'Entry already parsed, skipping...')
            else:
                self.log.debug(f'New entry found, parsing...')
                self.lock.acquire()
                for item in self.itemize(data):
                    if self.filter(item=item):
                        self.storage.store(item)
                    else:
                        pass
                        # self.log.debug(f'Rejected: {item}')
                self.storage.set_completed(data)
                self.lock.release()

        self.log.info(f'Stored {self.storage.count()} items')

    def count(self):
        return self.storage.count()

    def query(self, page=0, count=100, format='raw'):
        return self.loader.query(page, count, format)
