
import logging
from fastapi.param_functions import Depends

from app.api import deps
from fastapi import APIRouter, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.put("/register")
def register(request: Request, runtime = Depends(deps.get_runtime)):
    logger.info(f'Registering host {request.client.host}')
    runtime.register(request.client.host)

