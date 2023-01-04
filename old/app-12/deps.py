from typing import Generator

from app.db import session
from app.flow import Flow
from app.registry import Registry


def get_flow() -> Flow:
    return Flow()


def get_orm_db() -> Generator:
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_registry() -> Registry:
    return Registry()
