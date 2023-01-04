import json
import logging
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, Request

from app.deps import get_flow
from app.flow import Flow

logger = logging.getLogger(__name__)
router = APIRouter()

'''
curl -X 'PUT' 'http://localhost:9080/api/v1/model/train'
'''
@router.put("/train")
def train(
    background_tasks: BackgroundTasks,
    flow: Flow = Depends(get_flow)
):
    background_tasks.add_task(flow.set_stage_and_execute, 'train', stages=[
                              'train', 'generate_statics'])
    return {"message": "Started model training"}


@router.post("/predict")
async def predict(
    request: Request,
    flow: Flow = Depends(get_flow)
):
    data = await request.json()
    flow.set_stage_and_execute(
        'predict', stages=['predict'], data=data)

    return json.dumps(flow.runtime.last_op_data)
    # return json.dumps(result)
