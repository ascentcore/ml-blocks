import json
import logging

from fastapi import Request, APIRouter, Depends
from old.cached_version.settings import settings
from old.cached_version.deps import get_flow
from old.cached_version.flow import Flow


logger = logging.getLogger(__name__)
router = APIRouter()


@router.put("/trigger")
def get_dataset_length(
    stage: str,
    flow: Flow = Depends(get_flow)
):
    return flow.trigger(stage)


@router.get("/stage")
def get_dataset_length():
    with open(f'{settings.MOUNT_FOLDER}/internal/stage', 'r') as infile:
        return infile.read()


@router.post("/preferences")
async def update_preferences(request: Request, flow: Flow = Depends(get_flow)):
    json_data = await request.json()
    if json_data != None:
        with open(f'{settings.MOUNT_FOLDER}/internal/preferences.json', 'w') as outfile:
            outfile.write(json.dumps(json_data))
            flow._touch_file('preferences')