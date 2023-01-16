import logging

from .base_storage import BaseStorage

logger = logging.getLogger(__name__)


class InMemoryStorage(BaseStorage):

    def __init__(self, settings):
        super().__init__()
        self.dataset = []
        logger.info(
            f'In memory storage initialized')

    def store(self, item):
        self.dataset.append(item)

    def clear(self):
        super().clear()
        self.dataset = []

    def count(self):
        return len(self.dataset)

    def query(self, page=0, count=100):
        offset = page * count
        return self.dataset[offset:offset+count]
