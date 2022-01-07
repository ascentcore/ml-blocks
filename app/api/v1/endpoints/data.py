
from typing import List

import logging
import requests
import pandas

from fastapi import APIRouter, Depends, File, UploadFile, Form
from app.store import Storage

from app import deps
from app.runtime import runtime
from app.loaders.loader_factory import get_loader


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def get_data(db: Storage = Depends(deps.get_db)):
    return db.load()

@router.get("/refresh")
def refresh(
        pipeline = Depends(deps.get_piepline),
        runtime=Depends(deps.get_runtime),
        db: Storage = Depends(deps.get_db)):
    if pipeline.dependency != None:
        response = requests.get(f'http://{pipeline.dependency}/api/v1/data')
        data = response.json()
        df = pandas.DataFrame(data)
        runtime.process_dataset(df)
        db.store_pandas(df)


@router.post("/uploadfiles")
def create_upload_file(
        runtime=Depends(deps.get_runtime), 
        pipeline = Depends(deps.get_piepline), 
        files: List[UploadFile] = File(...),
        db = Depends(deps.get_orm_db),
        loader: str = Form('csv'),
        append: bool = Form(None)):
    
    logger.info('File uploaded. Processing...')
    loader = get_loader(loader)
    print({"filenames": [file.filename for file in files]})
    loader.load_files(files)
    output = runtime.process_dataset(loader.data)
    loader.store(output, append)
    pipeline.trigger_downstream(db)
