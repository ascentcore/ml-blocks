
import logging
import json

from fastapi import APIRouter, Depends, Request
from app.store import Storage
from app.api import deps
from app.runtime import Runtime

import pandas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/train")
def train(db: Storage = Depends(deps.get_db), runtime: Runtime = Depends(deps.get_runtime)):
    data = db.load_pandas()
    model = runtime.train(data)
    runtime.store(model)

@router.post("/predict")
async def predict(data: Request, runtime: Runtime = Depends(deps.get_runtime)):
    json_data = await data.json()
    data = pandas.DataFrame(json_data)
    predicts = runtime.predict(data)
    return json.dumps(predicts)