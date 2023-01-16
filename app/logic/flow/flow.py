from app.generic_components.generic_interfaces.logic_interface import LogicInterface
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.generic_components.singleton_base.singleton_base import Singleton
from app.logic.block.main import BlockMain


# TODO split the flow for each router
class RouterFlow(metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.__block = BlockMain()

    def __call__(self, *args, **kwargs):
        return self

    def register(self, hostname):
        pass

    @property
    def block(self):
        return self.__block

    def block_type(self):
        return self.__block.type()


def get_flow() -> RouterFlow:
    return RouterFlow()
