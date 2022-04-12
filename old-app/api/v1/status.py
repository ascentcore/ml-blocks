import logging
import json
from fastapi import APIRouter, Depends, Request
from app.config import settings
from app.flow import Flow
from app.deps import get_flow, get_orm_db
from app.db.crud import get_status, get_graph
from app.db.models import Report
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

    try:
        with open(f'{settings.MOUNT_FOLDER}/progress.txt', 'r') as outfile:
            progress = int(outfile.read())
    except:
        progress = 100
        pass

    return {
        "name": flow.runtime.name,
        "operations": list(operations),
        "status": get_status(db),
        "export_formats": flow.loader.export_content_types(),
        "dependencies": get_graph(db),
        "progress": progress
    }


@router.post("/report")
async def report(
        request: Request,
        db=Depends(get_orm_db)):

    host = request.client.host

    json_data = await request.json()

    report = Report(
        host=host, type=json_data["type"], value=json_data["value"])
    db.merge(report)
    db.commit()


@router.get("/report")
async def report(
        db=Depends(get_orm_db)):
    return db.query(Report).all()


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
