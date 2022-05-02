from typing import Callable

from app.settings import settings


class Runtime:

    report_progress: Callable
    settings: settings
