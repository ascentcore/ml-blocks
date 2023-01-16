import logging
import os
import csv
import pandas as pd

from old.cached_version.base_block import BaseBlock

logger = logging.getLogger(__name__)


class Block(BaseBlock):

    name = os.getenv("BLOCK_NAME", "Loader Test Block ")

    def __init__(self, settings):
        super().__init__(settings)

    def itemize(self, data, loader):
        with open(data, newline='\n') as csvfile:
            rows = csv.reader(csvfile, delimiter=',')
            for index, row in enumerate(rows):
                if index > 0 and len(row) > 0:
                    yield [row[0], float(row[1]), float(row[2]), float(row[3])]

    def filter(self, item, loader):
        return item[1] > 0.2


    async def train(self):
        logger.info('>>>>>>>>>>>>>>>>>>>> ')
        df = pd.DataFrame(self.storage.query(0, self.storage.count()))
        logger.info(df)
        # return {}