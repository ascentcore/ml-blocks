
import logging

from fastapi import APIRouter, Depends, Request, BackgroundTasks

from app.deps import get_flow, get_orm_db
from app.flow import Flow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/train")
async def train(background_tasks: BackgroundTasks, flow: Flow = Depends(get_flow), db=Depends(get_orm_db)):
    background_tasks.add_task(flow.retrain, db)


@router.post("/predict")
async def predict(request: Request, db=Depends(get_orm_db), flow: Flow = Depends(get_flow)):
    data = await flow.loader.load_request(request)
    predicts = flow.predict(db, data, request)
    return predicts


@router.post("/predict_bg")
async def predict(background_tasks: BackgroundTasks, request: Request, db=Depends(get_orm_db), flow: Flow = Depends(get_flow)):
    data = await flow.loader.load_request(request)
    background_tasks.add_task(flow.predict, db, data, request)


@router.get("/predict_schema")
async def get_interract_schema(flow: Flow = Depends(get_flow)):
    return flow.runtime.predict_schema()
