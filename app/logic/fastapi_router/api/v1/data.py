from fastapi import APIRouter, Depends

from app.generic_components.log_mechanism.log_mechanism import LogBase, LOG
from app.generic_components.singleton_base.singleton_base import Singleton
from app.logic.block.loader.base import BlockFormats
from app.logic.flow.flow import RouterFlow, get_flow


class RouterData(APIRouter, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.log.debug("Creating data router")

    def __hash__(self):
        return id(self)


router = RouterData()


@router.get("/count")
def get_count(flow: RouterFlow = Depends(get_flow)) -> int:
    return flow.block.block_active.count()


@router.get("/dataset")
def get_dataset(page: int = 0,
                count: int = 10,
                output_format: BlockFormats = BlockFormats.raw,
                flow: RouterFlow = Depends(get_flow)) :
    return flow.block.block_active.query(page=page, count=count, output_format=output_format)  # FIXME
