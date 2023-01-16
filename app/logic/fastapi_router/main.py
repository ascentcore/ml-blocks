from typing import List, Dict

from fastapi import APIRouter

from app.generic_components.generic_interfaces.logic_interface import LogicInterface
from app.generic_components.log_mechanism.log_mechanism import LogBase
from app.logic.fastapi_router.api.v1.block import RouterBlock
from app.logic.fastapi_router.api.v1.data import RouterData
from app.logic.fastapi_router.api.v1.pipeline import RouterPipeline


class RoutesProperties:
    prefix: str = ""
    tags: List[str] = []

    def __init__(self, prefix, tags):
        self.prefix = prefix
        self.tags = tags


class RouterMain(APIRouter):

    def __init__(self):
        super().__init__()
        self.__routes: Dict[APIRouter, RoutesProperties] = {}
        self.log = LogBase.log(class_name=self.__class__.__name__)
        self.log.debug("Creating main router")

    def setup(self):
        """
        Setup all the routes, and link them to main one
        """
        self.construct_routes()
        self.include_routes()

    def construct_routes(self):
        self.__routes[RouterBlock()] = RoutesProperties(prefix="/block", tags=["block"])
        self.__routes[RouterData()] = RoutesProperties(prefix="/data", tags=["data"])
        self.__routes[RouterPipeline()] = RoutesProperties(prefix="/pipeline", tags=["pipeline"])

    def include_routes(self):
        """
        Generic functionality to include the routes to main route
        """
        for route_api in self.__routes:
            route_property = self.__routes[route_api]
            self.include_router(route_api, prefix=route_property.prefix, tags=route_property.tags)
