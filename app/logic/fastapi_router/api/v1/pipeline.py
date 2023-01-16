from fastapi import APIRouter, Depends

from app.generic_components.log_mechanism.log_mechanism import LogBase, LOG
from app.generic_components.singleton_base.singleton_base import Singleton
from app.logic.flow.flow import RouterFlow, get_flow


class RouterPipeline(APIRouter, metaclass=Singleton):
    __flow: RouterFlow() = Depends(get_flow) # FIXME

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.log.debug("Creating pipeline router")

    def __hash__(self):
        return id(self)

    @property
    def flow(self):
        return self.__flow

    @flow.setter
    def flow(self, value):
        self.__flow = value


router = RouterPipeline()


@router.put("/register")
async def register(hostname: str) -> None:
    LOG.debug(f'Called subscribe')
    router.flow.register(hostname)
