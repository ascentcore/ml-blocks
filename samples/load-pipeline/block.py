import logging
import os



logger = logging.getLogger(__name__)


class Block:
    name = os.getenv("BLOCK_NAME", "Load Pipeline")

    # loaders = ['file_loader', CustomFileLoader()]
    loaders = ['file_loader', 'pandas_loader']


    def process_data(self, loader, data):
        name = loader.__class__.__name__
        if name == 'PandasLoader':
            return data[:5]
        return data