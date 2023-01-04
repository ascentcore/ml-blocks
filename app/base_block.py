import logging
import os

from app.loaders.file_loader import FileLoader
from app.storage.in_memory_storage import InMemoryStorage

logger = logging.getLogger(__name__)


class BaseBlock:

    name = os.getenv("BLOCK_NAME", "Pass Through ML Block")

    root_loaders_classes = [FileLoader]

    storage_class = InMemoryStorage

    def __init__(self, settings):
        logger.info(f'Initializing block: {self.name}')
        self.settings = settings
        self.root_loaders = [loader(settings=settings)
                             for loader in self.root_loaders_classes]

        self.storage = self.storage_class(
            settings=settings) if self.storage_class != None else None

    def itemize(self, data, loader):
        yield data

    def filter(self, item, loader):
        return True

    def train(self):
        pass

    def save_model(self, model):
        return None

    def load_model(self):
        return None