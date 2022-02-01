
from typing import Generator
from app.db import session, models
from app.flow import Flow
from app.registry import Registry

# move away from singleton
flow = Flow()

registry = Registry()

models.Base.metadata.create_all(bind=session.engine)

def get_orm_db() -> Generator:
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_flow() -> Flow:
    return flow


def get_registry() -> Registry:
    return registry