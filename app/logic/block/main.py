from app.configuration.settings import Settings
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.generic_components.singleton_base.singleton_base import Singleton
from app.logic.block.base import BlockBase
from app.logic.block.loader.base import BlockLoader
from app.logic.block.storage.base import BlockStorage


class BlockMain(metaclass=Singleton):
    __block_active: BlockBase = None
    __block_loader: BlockLoader = None
    __block_storage: BlockStorage = None

    def __init__(self):
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.__settings = Settings()
        self.load_block_storage()
        self.load_block_loader()
        self.load_block_type()

    # TODO make more generic functions here
    def load_block_storage(self):
        self.log.debug(f'BlockStorage.plugins {len(BlockStorage.plugins)}')
        for loader in BlockStorage.plugins:
            inst = loader()
            if self.__settings.active_block_storage == inst.name:
                self.log.debug(f'>Activated storage {inst.name} {type(inst)}')
                self.__block_storage = inst
                break

    def load_block_loader(self):
        self.log.debug(f'BlockLoader.plugins {len(BlockLoader.plugins)}')
        for loader in BlockLoader.plugins:
            inst = loader()
            if self.__settings.active_block_loader == inst.name:
                self.log.debug(f'>Activated loader {inst.name} {type(inst)}')
                self.__block_loader = inst
                break

    def load_block_type(self):
        self.log.debug(f'BlockBase plugins {len(BlockBase.plugins)} wanted {self.__settings.active_block}')
        for block in BlockBase.plugins:
            inst = block(loader=self.__block_loader, storage=self.__block_storage)
            if self.__settings.active_block == inst.name:
                self.log.debug(f'>Activated block {inst.name} {type(inst)}')
                self.__block_active = inst
                self.load_data(from_scratch=True)  # TODO split into multiple functions for reusable purpose
                break

    @property
    def block_active(self):
        return self.__block_active

    def load_data(self, from_scratch=False):
        self.block_active.load_data(from_scratch=from_scratch)
