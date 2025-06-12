from fastapi import APIRouter

from app.rutas import login, usuario

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(usuario.router)
