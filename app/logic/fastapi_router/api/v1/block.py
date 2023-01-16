from fastapi import APIRouter, Depends

from app.generic_components.log_mechanism.log_mechanism import LogBase, LOG
from app.generic_components.singleton_base.singleton_base import Singleton
from app.logic.block.base import BlockType
from app.logic.flow.flow import RouterFlow, get_flow


class RouterBlock(APIRouter, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.log.debug("Creating block router")

    def __hash__(self):
        return id(self)


router = RouterBlock()


@router.get("/active")
def active_block(flow: RouterFlow = Depends(get_flow)) -> BlockType:
    LOG.debug(f'Called active_block')
    return flow.block_type()  # FIXME


@router.put("/select")
async def select_block(block_type:BlockType, flow: RouterFlow = Depends(get_flow)) -> BlockType:
    return flow.block.select_block(value=block_type)  # FIXME
