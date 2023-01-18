from enum import Enum

from app.configuration.settings import Settings
from app.generic_components.generic_types.error import ErrorInvalidUsage
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.generic_components.sqlite_wrapper.wrapper_sqlite import WrapperSqlite
from app.logic.block.storage.base import BlockStorage


class BlockSqliteCommands(str, Enum):
    create_table = "CREATE TABLE if not  exists \"dataset\" \
                   ( \"id\"	INTEGER, " \
                   "\"data\"	BLOB, " \
                   "PRIMARY KEY(\"id\" AUTOINCREMENT) );"

    count = "SELECT count(*) FROM dataset;"

    clear = "DELETE FROM dataset;"

    insert_data = "INSERT INTO \"dataset\" (\"data\") VALUES (?);"


class BlockStorageSqlite(BlockStorage):

    def __init__(self):
        super().__init__(name="BlockStorageSqlite")
        self.log = LogBase.log(self.__class__.__name__)
        self.__dataset = []
        self.__sqlite_db = WrapperSqlite()
        self.__settings = Settings()
        self.__sqlite_db.connect_database(self.__settings.sqlite_database)
        self.__sqlite_db.send_command(command=BlockSqliteCommands.create_table)
        self.clear()
        self.log.info(f'Sqlite initialized')

    def __del__(self):
        try:
            self.__sqlite_db.close_connection()
        except ErrorInvalidUsage:
            pass

    def clear(self):
        super().clear()
        self.__sqlite_db.send_command(command=BlockSqliteCommands.clear)

    def store(self, item):
        single_item = ' '.join(item).encode('ascii')
        data = self.__sqlite_db.to_blob(data=single_item)
        self.__sqlite_db.send_command(command=BlockSqliteCommands.insert_data, parameters=(data,))

    def count(self):
        no = int(self.__sqlite_db.send_command(command=BlockSqliteCommands.count, query=True, multiple=False)[0])
        self.log.debug(f"Number of entries {no}")
        return no

    def query(self, page=0, count=100):
        offset = page * count
        return ""
