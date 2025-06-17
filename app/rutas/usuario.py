from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.esquemas.usuario import UsuarioSaliente, UsuarioIngreso
from app.core.dependencias import UsuarioActual, DepSesion
from app.modelos.usuario import registrar_usuario

router = APIRouter(tags=["Usuarios"])


@router.get("/yo", response_model=UsuarioSaliente)
def quien_soy(db: DepSesion, usuario_actual: UsuarioActual) -> Any:
    return usuario_actual


@router.post("/", response_model=UsuarioSaliente)
def crear_usuario(db: DepSesion, datos_usuario: UsuarioIngreso) -> Any:
    nuevo_usuario = registrar_usuario(datos_usuario, db)

    if not nuevo_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puedo crear al usuario",
        )

    return nuevo_usuario
