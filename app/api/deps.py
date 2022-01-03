
from typing import Generator
from app.store import SQLStorage
from app.runtime import Runtime, runtime
from app.db import session, models

models.Base.metadata.create_all(bind=session.engine)

def get_db() -> Generator:
    try:
        db = SQLStorage()
        yield db
    finally:
        pass
        # db.close()

def get_runtime() -> Runtime:
    return runtime

def get_orm_db() -> Generator:
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()