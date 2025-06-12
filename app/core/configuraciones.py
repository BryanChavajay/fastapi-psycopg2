import os
from dotenv import load_dotenv

load_dotenv()


ALGORITMO = "HS256"

DB_HOST = os.getenv("DB_HOST")
DATA_BASE = os.getenv("DATA_BASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

LLAVE_SECRETA = os.getenv("SECRET_KEY")

EXPIRACION_TOKEN_ACCESO_MINUTOS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
EXPIRACION_REFRESH_TOKEN_DIAS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

API_V1_STR: str = "/api/v1"
