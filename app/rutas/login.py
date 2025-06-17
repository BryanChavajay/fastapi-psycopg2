from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from app.core.configuraciones import (
    EXPIRACION_TOKEN_ACCESO_MINUTOS,
    EXPIRACION_REFRESH_TOKEN_DIAS,
)
from app.core.dependencias import DepSesion, verificar_refresh_token
from app.core.seguridad import crear_token_acceso
from app.modelos.usuario import autenticar_usuario
from app.esquemas.token import TokenPayload, Token, RefreshTokenPayload

router = APIRouter(tags=["login"])


@router.post("/access-token", response_model=Token)
def login_token_acceso(
    db: DepSesion,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    respuesta: Response,
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

    contenido_refresh_token = RefreshTokenPayload(sub=str(usuario.codigo_usuario))
    expiracion_refresh_token = timedelta(days=EXPIRACION_REFRESH_TOKEN_DIAS)
    refresh_token = crear_token_acceso(
        subject=contenido_refresh_token.model_dump(),
        expires_delta=expiracion_refresh_token,
    )
    respuesta.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return Token(
        access_token=crear_token_acceso(
            subject=contenido_token.model_dump(), expires_delta=expiracion_token
        )
    )


@router.post("/refresh", response_model=Token)
def refrescar_roken_acceso(
    db: DepSesion, respuesta: Response, refresh_token: str = Cookie(None)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sin token de refresco",
        )

    usuario = verificar_refresh_token(sesion=db, refresh_roken=refresh_token)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo comprobar el token",
        )

    contenido_token = TokenPayload(
        sub=str(usuario.codigo_usuario), sv=usuario.version_sesion
    )
    expiracion_token = timedelta(minutes=EXPIRACION_TOKEN_ACCESO_MINUTOS)

    contenido_refresh_token = RefreshTokenPayload(sub=str(usuario.codigo_usuario))
    expiracion_refresh_token = timedelta(days=EXPIRACION_REFRESH_TOKEN_DIAS)
    refresh_token = crear_token_acceso(
        subject=contenido_refresh_token.model_dump(),
        expires_delta=expiracion_refresh_token,
    )
    respuesta.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return Token(
        access_token=crear_token_acceso(
            subject=contenido_token.model_dump(), expires_delta=expiracion_token
        )
    )


@router.post("/logout")
def finalizar_sesion(respuesta: Response, peticion: Request, db: DepSesion):
    refresh_token = peticion.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de refresco faltante",
        )

    respuesta.delete_cookie(key="refresh_token")

    return {"detail": "Sesion cerrada"}
