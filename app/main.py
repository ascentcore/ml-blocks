"""
ML Blocks startup
"""
# !/usr/bin/env python
import os
import sys

from fastapi import FastAPI

from app.generic_components.fastapi_wrapper.fastapi_app_wrapper import FastApiApp
from app.logic.builder import Builder

try:
    """
    Relative path import is done to search automatically for teh modules
    """
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(os.path.dirname(__file__))
except ImportError:
    print('Relative import failed')

builder = Builder()
builder.setup()

fastapi = FastApiApp()
app: FastAPI() = fastapi.app
