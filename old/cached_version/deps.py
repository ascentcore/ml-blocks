from old.cached_version.flow import Flow
from old.cached_version.block.block import Block

from old.cached_version.settings import settings

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
