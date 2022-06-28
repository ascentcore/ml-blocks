

import logging
import os

from fastapi import APIRouter, Depends

from app.deps import get_flow
from app.flow import Flow
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def get_dataset_length(flow: Flow = Depends(get_flow)):
    search_dir = f'{flow.runtime.settings.MOUNT_FOLDER}/statics'
    os.chdir(search_dir)
    files = filter(os.path.isfile, os.listdir(search_dir))
    files = [(search_dir, f, os.path.getmtime(os.path.join(search_dir, f)))
             for f in files]  # add path to each file
    files.sort(key=lambda x: -x[2])

    return files
