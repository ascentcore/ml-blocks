from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.base import BlockBase


class BlockSample(BlockBase):

    def __init__(self):
        super().__init__(name="BlockSample")
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