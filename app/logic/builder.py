from app.configuration.settings import Settings
from app.generic_components.fastapi_wrapper.fastapi_app_wrapper import FastApiApp
from app.generic_components.generic_types.error import ErrorBase, ErrorFatal
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.generic_components.generic_interfaces.logic_interface import LogicInterface
from app.logic.fastapi_router.main import RouterMain


class Builder(LogicInterface):

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(class_name=self.__class__.__name__)

        self.__settings = Settings()
        self.__router = RouterMain()
        self.__fastapi_app = FastApiApp()
        
        self.__settings.print()
        self.log.info("Initialized application {}-{}".format(self.__settings.version, self.__settings.environment))  # TODO add version here

    def __del__(self):
        pass

    @property
    def app(self):
        return self.__fastapi_app.app

    def setup(self):
        try:
            self.__router.setup()
            self.__fastapi_app.setup(self.__router, self.__settings.api)
        except ErrorBase as exp:
            self.log.warn("Setup failed {}".format(str(exp)))
            raise ErrorFatal()

    def start(self):
        self.log.info("Starting logic")

    def stop(self):
        self.log.info("Stopping logic")
