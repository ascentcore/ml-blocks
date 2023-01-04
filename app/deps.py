from typing import Generator

from app.flow import Flow
from app.block.block import Block

from app.settings import settings

# from app.registry import Registry

block = Block(settings)
flow = Flow(block)

flow.to_storage()

def get_flow() -> Flow:
    return flow


# def get_orm_db() -> Generator:
#     db = session.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def get_registry() -> Registry:
#     return Registry()
