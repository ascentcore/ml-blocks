from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.storage.base import BlockStorage


class BlockStorageMemory(BlockStorage):

    def __init__(self):
        super().__init__(name="BlockStorageMemory")
        self.log = LogBase.log(self.__class__.__name__)
        self.__dataset = []
        self.log.info(f'In memory storage initialized')

    def store(self, item):
        self.__dataset.append(item)

    def clear(self):
        super().clear()
        self.__dataset = []

    def count(self):
        return len(self.__dataset)

    def query(self, page=0, count=100):
        offset = page * count
        return self.__dataset[offset:offset + count]
