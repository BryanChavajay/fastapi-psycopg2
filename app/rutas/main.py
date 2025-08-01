from fastapi import APIRouter

from app.rutas import login, usuario, categoria, gasto

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login")
api_router.include_router(usuario.router, prefix="/usuario")
api_router.include_router(categoria.router, prefix="/categoria")
api_router.include_router(gasto.router, prefix="/gasto")
