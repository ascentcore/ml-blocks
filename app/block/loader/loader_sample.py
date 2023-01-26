from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.loader.base import BlockLoader, BlockFormats


class BlockLoaderSample(BlockLoader):

    def __init__(self):
        super().__init__(name="BlockLoaderSample")
        self.log = LogBase.log(self.__class__.__name__)

    def initialize(self):
        self.log.warn("implementation not done")

    def refresh(self):
        self.log.warn("implementation not done")

    def query(self, page=0, count=100, output_format: BlockFormats = BlockFormats.raw):
        self.log.warn("implementation not done")
