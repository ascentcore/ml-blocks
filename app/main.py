from fastapi import FastAPI

from .default.name import get_name

app = FastAPI()

@app.get("/")
def read_root():
    return {"App": get_name()}

