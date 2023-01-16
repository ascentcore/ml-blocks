from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from app.generic_components.generic_interfaces.logic_interface import LogicInterface
from app.generic_components.generic_types.error import ErrorInvalidArgument
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.generic_components.singleton_base.singleton_base import Singleton


class FastApiApp(metaclass=Singleton):

    def __init__(self):
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.__app = FastAPI()

    def setup(self, *args):
        try:
            api_router = args[0]
            prefix = args[1]
        except IndexError:
            self.log.warn("Configuration not sent")
            raise ErrorInvalidArgument()

        self.app.add_middleware(middleware_class=CORSMiddleware,
                                allow_origins=["*"],
                                allow_credentials=True,
                                allow_methods=["*"],
                                allow_headers=["*"],
                                )
        self.app.include_router(router=api_router, prefix=prefix)

    @property
    def app(self):
        return self.__app

    def include_router(self, router: APIRouter, prefix: str):
        if router is None:
            self.log.warn("Router param NOK")
            raise ErrorInvalidArgument()
        if prefix is None or len(prefix) == 0 or "/" not in prefix:
            self.log.warn("Prefix param NOK")
            raise ErrorInvalidArgument()
        self.app.include_router(router=router, prefix=prefix)
