import logging
import json
from fastapi import APIRouter, Depends, Request
from app.config import settings
from app.flow import Flow
from app.deps import get_flow, get_orm_db
from app.db.crud import get_status, get_graph
from app.runtime import noop, defaults
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def current_status(
    flow: Flow = Depends(get_flow),
    db=Depends(get_orm_db)
):

    def has_operation(operation):
        try:
            func = getattr(flow.runtime, operation)
            return func != noop and callable(func)
        except:
            return False

    operations = list(defaults.keys())
    operations = filter(lambda key: has_operation(key), operations)

    return {
        "name": flow.runtime.name,
        "operations": list(operations),
        "status": get_status(db),
        "export_formats": flow.loader.export_content_types(),
        "dependencies": get_graph(db)
    }


@router.get("/test")
def current_status(
    flow: Flow = Depends(get_flow),
    db=Depends(get_orm_db)
):
    return {
        "name": flow.runtime.name,
        "status": get_status(db),
        "export_formats": flow.loader.export_content_types(),
        "dependencies": get_graph(db)
    }


@router.get("/settings_schema")
def current_status(
    flow: Flow = Depends(get_flow)
):
    return flow.runtime.settings_schema()


@router.post("/settings")
async def save_settings(request: Request):
    json_data = await request.json()
    with open(f'{settings.MOUNT_FOLDER}/settings.json', 'w') as outfile:
        outfile.write(json.dumps(json_data))


@router.get("/settings")
async def get_settings(flow: Flow = Depends(get_flow)):
    try:
        return flow.runtime.get_settings()
    except:
        return {}
