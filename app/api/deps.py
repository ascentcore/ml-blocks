
from typing import Generator
from app.store import SQLStorage
from app.runtime import Runtime, runtime

def get_db() -> Generator:
    try:
        db = SQLStorage()
        yield db
    finally:
        pass
        # db.close()

def get_runtime() -> Runtime:
    return runtime