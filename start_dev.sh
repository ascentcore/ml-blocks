#!/bin/bash
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir --upgrade -r /app/requirements_local.txt
/start-reload.sh