from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.base import BlockBase
from app.logic.block.storage.base import BlockFormats


class BlockSample(BlockBase):

    def __init__(self, loader, storage):
        super().__init__(name="BlockSample", loader=loader, storage=storage)
        self.log = LogBase.log(self.__class__.__name__)

    def train(self):
        self.log.warn("implementation not done")

    def save_model(self, model):
        self.log.warn("implementation not done")

    def load_model(self):
        self.log.warn("implementation not done")

    def load_data(self, from_scratch=False):
        self.log.warn("implementation not done")

    def count(self):
        self.log.warn("implementation not done")

    def itemize(self, data):
        self.log.warn("implementation not done")

    def query(self, page=0, count=100, output_format: BlockFormats = BlockFormats.raw):
        self.log.warn("implementation not done")
