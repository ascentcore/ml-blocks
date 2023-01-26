from fastapi import APIRouter, Depends, Request

from app.generic_components.log_mechanism.log_mechanism import LogBase, LOG
from app.generic_components.singleton_base.singleton_base import Singleton
from app.logic.flow.flow import RouterFlow, get_flow
from app.logic.registry.registry import Registry
from app.configuration.settings import Settings
from app.generic_components.log_mechanism.log_mechanism import LogBase, LOG


class RouterPipeline(APIRouter, metaclass=Singleton):
    __flow: RouterFlow() = Depends(get_flow)
    __registry: Registry() = Registry()
    __settings: Settings = None

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.log.debug("Creating pipeline router")
        self.__settings = Settings()
        self.__registry.initialize()
        
    def __hash__(self):
        return id(self)

    @property
    def flow(self):
        return self.__flow

    @property
    def settings(self):
        return self.__settings

    @property
    def registry(self):
        return self.__registry

    @flow.setter
    def flow(self, value):
        self.__flow = value


router = RouterPipeline()


@router.put("/register")
async def register(block_id: str, upstream: str, type: str, request: Request) -> None:
    host = request.client.host
    LOG.debug(
        f'Registering from: {host} to {upstream} with blockId: {block_id} and type:{type}')
    router.registry.register(block_id, upstream, host, type)
