
from typing import Generator
from app.db import session, models
from app.flow import Flow
from app.registry import Registry

flow = Flow()

registry = None

try:
    models.Base.metadata.create_all(bind=session.engine)
except:
    pass


def get_orm_db() -> Generator:
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_flow() -> Flow:
    return flow


def get_registry() -> Registry:
    global registry
    if registry == None:
        registry = Registry(flow)
    return registry
