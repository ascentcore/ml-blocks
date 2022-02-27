import logging
from fastapi import APIRouter, Depends, Request

from app.flow import Flow
from app.deps import get_flow, get_orm_db
from app.db.crud import get_status, get_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def current_status(
    flow: Flow = Depends(get_flow),
    db = Depends(get_orm_db)
):
    return {
        "name": flow.runtime.name,
        "status": get_status(db),
        "export_formats": flow.loader.export_content_types(),
        "dependencies": get_graph(db)
    }

@router.get("/test")
def current_status(
    flow: Flow = Depends(get_flow),
    db = Depends(get_orm_db)
):
    return {
        "name": flow.runtime.name,
        "status": get_status(db),
        "export_formats": flow.loader.export_content_types(),
        "dependencies": get_graph(db)
    }
