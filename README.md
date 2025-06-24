# FastAPI psycopg2

## DESCRIPCION

Este proyecto es una API REST sencilla para rastrear gastos.

El proyecto utiliza:
- Python 3.13.3
- FastAPI 0.115.12
- psycopg2-binary 2.9.10
- PostgreSQL 16

## INTALACION

Primero ejecuta los scripts de la carpeta _creacion_bd_.

> [NOTE] Recuerda colocar las credenciales de la base de datos en el .env

Por defecto este proyecto utiliza [uv](https://docs.astral.sh/uv/) para gestionar las dependencias.

Para instalar las dependecias puedes utilizar:

```bash
uv sync
```

Luego activa el entorno virtual de acuerdo a tu sistema operativo:

```bash
.venv/bin/activate
```

Por utlimo ejecuta el servidor de desarrollo 🚀:

```bash
fastapi dev app/main.py --port 8080
```

Sino quieres utilizar uv, tambien puedes instalar las depencias de forma tradicional, crea tu entorno virtual e instala las depencias de _requirements.txt_ con pip.
