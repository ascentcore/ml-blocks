"""
ML Blocks startup
"""
# !/usr/bin/env python
import os
import sys

try:
    """
    Relative path import is done to search automatically for teh modules
    """
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(os.path.dirname(__file__))
except ImportError:
    print('Relative import failed')

# Force load of settings first to ensure that we can propagate all the info to the platform also 
from app.configuration.settings import Settings
settings = Settings()

from fastapi import FastAPI
from app.generic_components.fastapi_wrapper.fastapi_app_wrapper import FastApiApp
from app.logic.builder import Builder

builder = Builder()
builder.setup()
fastapi = FastApiApp()
app: FastAPI() = fastapi.app
