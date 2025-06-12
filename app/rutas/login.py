from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.configuraciones import EXPIRACION_TOKEN_ACCESO_MINUTOS
from app.core.dependencias import DepSesion
from app.core.seguridad import creat_token_acceso
from app.modelos.usuario import autenticar_usuario
from app.esquemas.token import TokenPayload, Token

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_token_acceso(
    db: DepSesion, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    usuario = autenticar_usuario(
        db=db, correo_o_usuario=form_data.username, contrasenia=form_data.password
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo o contraseña incorrectos",
        )

    contenido_token = TokenPayload(
        sub=str(usuario.codigo_usuario), sv=usuario.version_sesion
    )

    expiracion_token = timedelta(minutes=EXPIRACION_TOKEN_ACCESO_MINUTOS)

    return Token(
        access_token=creat_token_acceso(
            subject=contenido_token.model_dump(), expires_delta=expiracion_token
        )
    )
