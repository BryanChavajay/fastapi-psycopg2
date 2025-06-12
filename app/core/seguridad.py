from datetime import datetime, timedelta, timezone
from typing import Any
import jwt

from passlib.context import CryptContext
from app.core.configuraciones import ALGORITMO, LLAVE_SECRETA

pwd_contexto = CryptContext(schemes=["bcrypt"], deprecated="auto")


def obtener_hash_contrasenia(contrasenia: str) -> str:
    return pwd_contexto.hash(contrasenia)


def verificar_contrasenia(hash_contrasenia: str, contrasenia_plana: str) -> bool:
    return pwd_contexto.verify(contrasenia_plana, hash_contrasenia)


def creat_token_acceso(
    subject: dict | Any, expires_delta: timedelta | None = None
) -> str:
    para_encriptar = subject.copy()

    if expires_delta:
        expiracion = datetime.now(timezone.utc) + expires_delta
    else:
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=60)

    para_encriptar.update({"exp": expiracion})
    token_jwt = jwt.encode(para_encriptar, LLAVE_SECRETA, algorithm=ALGORITMO)
    return token_jwt
