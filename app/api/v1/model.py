
import logging
import pickle
from fastapi import APIRouter, Query, Depends, Request, BackgroundTasks
from typing import Optional
from app.deps import get_flow, get_orm_db
from app.flow import Flow
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


async def get_data(replay, request, flow):
    dump_file = f'{settings.MOUNT_FOLDER}/last_predict.pkl'

    if replay:
        infile = open(dump_file, 'rb')
        data = pickle.load(infile)
        infile.close()
    else:

        data = await flow.loader.load_request(request)
        outfile = open(dump_file, 'wb')
        pickle.dump(data, outfile)
        outfile.close()

    return data


@router.post("/train")
async def train(
        background_tasks: BackgroundTasks,
        request: Request,
        flow: Flow = Depends(get_flow),
        db=Depends(get_orm_db)):
    background_tasks.add_task(flow.retrain, db, request)


@router.post("/predict")
async def predict(request: Request, replay: Optional[bool] = Query(False), db=Depends(get_orm_db), flow: Flow = Depends(get_flow)):
    data = await get_data(replay, request, flow)
    predicts = flow.predict(db, data, request)
    return predicts


@router.post("/predict_bg")
async def predict(background_tasks: BackgroundTasks,  request: Request, replay: Optional[bool] = Query(False), db=Depends(get_orm_db), flow: Flow = Depends(get_flow)):
    data = await get_data(replay, request, flow)
    background_tasks.add_task(flow.predict, db, data, request)


@router.get("/predict_schema")
async def get_interract_schema(flow: Flow = Depends(get_flow)):
    return flow.runtime.predict_schema()
