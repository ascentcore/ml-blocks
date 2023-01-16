from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.block.base import BlockBase, BlockType
from app.logic.block.plugin.csv_plugin import BlockCSV


class BlockMain:

    __block_type: BlockType = BlockType.base
    __block_active: BlockBase = None

    def __init__(self):
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.reload_configuration(value=BlockType.csv_loader)  # FIXME

    def reload_configuration(self, value=BlockType.base):
        old_value = self.__block_type
        self.__block_type = value
        # TODO add also load from env variables
        if value == BlockType.base:
            # TODO clean old block model or whatever needed
            self.__block_active = BlockBase()
        elif value == BlockType.csv_loader:
            self.__block_active = BlockCSV()
        else:
            self.__block_type = old_value
            self.log.warn("Unsupported type {}".format(value))

        if self.__block_type != old_value:
            self.load_data(from_scratch=True)

        return self.__block_type

    def type(self):
        return self.__block_type

    @property
    def block_active(self):
        return self.__block_active

    def select_block(self, value):
        return self.reload_configuration(value=value)

    def load_data(self, from_scratch = False):
        self.block_active.load_data(from_scratch=from_scratch)
