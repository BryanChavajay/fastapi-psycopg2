from fastapi import FastAPI

from app.rutas.main import api_router
from app.core.configuraciones import API_V1_STR

app = FastAPI()

app.include_router(api_router, prefix=API_V1_STR)
