from importlib.abc import Loader
from typing import Callable

from app.settings import settings


class Runtime:

    report_progress: Callable
    settings: settings
    loader: Loader
