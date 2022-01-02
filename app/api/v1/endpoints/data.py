
import logging
import requests
import pandas
import json

from fastapi import APIRouter, Depends
from app.store import Storage
from app.api import deps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def get_data(db: Storage = Depends(deps.get_db)):
    return db.load()

@router.get("/refresh")
def refresh(runtime = Depends(deps.get_runtime), db: Storage = Depends(deps.get_db)):
    if runtime.dependency != None:
        response = requests.get(f'http://{runtime.dependency}/api/v1/data')
        data = response.json()
        df = pandas.DataFrame(data)
        runtime.process_dataset(df)
        print(df.head)
        db.store_pandas(df)