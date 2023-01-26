from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.storage.base import BlockStorage, BlockFormats


class BlockStorageSample(BlockStorage):

    def __init__(self):
        super().__init__(name="BlockStorageSample")
        self.log = LogBase.log(self.__class__.__name__)

    def count(self):
        self.log.warn("implementation not done")

    def store(self, item):
        self.log.warn("implementation not done")

    def query(self, page=0, count=100, output_format: BlockFormats = BlockFormats.raw):
        self.log.warn("implementation not done")
