from typing import Annotated
import psycopg2
from psycopg2.extensions import connection
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError


from app.esquemas.usuario import UsuarioDB
from app.esquemas.token import TokenPayload
from app.core.configuraciones import (
    DB_HOST,
    DATA_BASE,
    DB_USER,
    DB_PASSWORD,
    DB_PORT,
    API_V1_STR,
    LLAVE_SECRETA,
    ALGORITMO,
)
from app.modelos.usuario import obtener_usuario_por_codigo

oauth2_reusable = OAuth2PasswordBearer(tokenUrl=f"{API_V1_STR}/login/access-token")


def obtener_db():
    coneccion = psycopg2.connect(
        host=DB_HOST,
        database=DATA_BASE,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )
    try:
        yield coneccion
    finally:
        coneccion.close()


DepSesion = Annotated[connection, Depends(obtener_db)]
DepToken = Annotated[str, Depends(oauth2_reusable)]


def obtener_usuario_actual(sesion: DepSesion, token: DepToken) -> UsuarioDB:
    try:
        payload = jwt.decode(token, LLAVE_SECRETA, algorithms=[ALGORITMO])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = obtener_usuario_por_codigo(token_data.sub, sesion)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return usuario


UsuarioActual = Annotated[UsuarioDB, Depends(obtener_usuario_actual)]
