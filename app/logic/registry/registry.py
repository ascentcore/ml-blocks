import asyncio
import socket
from enum import Enum

from app.configuration.settings import Settings
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.generic_components.sqlite_wrapper.wrapper_sqlite import WrapperSqlite
from app.generic_components.singleton_base.singleton_base import Singleton
from app.utils.connection import do_connect, connect


class RegistrySqliteCommands(str, Enum):
    create_table = "CREATE TABLE if not  exists \"registry\" \
                   ( \"id\"	INTEGER, " \
                   "\"block_identifier\"	TEXT, " \
                   "\"from_host\"	TEXT, " \
                   "\"to_host\"	TEXT, " \
                   "\"type\"	TEXT, " \
                   "PRIMARY KEY(\"id\" AUTOINCREMENT) );"

    clear = "DELETE FROM registry;"

    insert_data = 'INSERT INTO "registry" ("block_identifier", "from_host", "to_host", "type") VALUES (?, ?, ?, ?);'


class Registry(metaclass=Singleton):
    # TODO maybe in the future to make configurable
    __register_addrs = 'http://{}/api/v1/pipeline/register?block_id={}&upstream={}&type=data_dependency'
    __max_retries = 5
    __max_timeout = 5  # seconds

    def __init__(self):
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.__settings = Settings()
        self.__sqlite_db = None

    def initialize(self):
        if self.__settings.registry is not None:
            self.log.info(f'Trying to register to {self.__settings.registry}')
            loop = asyncio.get_event_loop()
            register_fn = self.do_register()
            if loop.is_running():
                loop.create_task(register_fn)
            else:
                loop.run_until_complete(self.do_register())

        else:
            self.log.info(f'Block initialized as registry')
            self.__sqlite_db = WrapperSqlite()
            self.__sqlite_db.connect_database("data/registry.sqlite")
            self.__sqlite_db.send_command(
                command=RegistrySqliteCommands.create_table)
            self.__sqlite_db.send_command(
                command=RegistrySqliteCommands.clear)

    async def do_register(self):
        if self.__settings.data_dependency:
            trials = 0
            while trials < self.__max_retries:
                domain = socket.getfqdn(self.__settings.data_dependency)
                registry_addr = ""
                #TODO maybe improve here and configuration for network names
                if domain != self.__settings.data_dependency and "ml-blocks-net" in domain:
                    ip_addr = socket.gethostbyname(self.__settings.data_dependency)
                    registry_addr    = self.__register_addrs.format(self.__settings.registry, self.__settings.data_dependency, ip_addr)
                    self.log.debug(f'Trying to connect {registry_addr}')
                    result = await connect(registry_addr)
                    if not result:
                        self.log.debug(f'Unable to connect {registry_addr} trial {trials}')
                    else:
                        self.log.debug(f'Connected {registry_addr}')
                        break
                else:
                    self.log.warn(f'Registry for dependency {self.__settings.data_dependency} not found')

                trials = trials + 1                
                await asyncio.sleep(self.__max_timeout)
            if trials == self.__max_retries:
                self.log.warn(f'Unable to connect {registry_addr} register aborted')
        else:
            self.log.info('No dependency given')

    def clear(self):
        self.__sqlite_db.send_command(command=RegistrySqliteCommands.clear)

    def register(self, block_id: str, from_host: str, to_host: str, type: str) -> None:
        data = (block_id, from_host, to_host, type)
        self.__sqlite_db.send_command(
            command=RegistrySqliteCommands.insert_data,
            parameters=data)
