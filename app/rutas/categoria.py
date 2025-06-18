from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.esquemas.categoriagasto import (
    CategoriaIngreso,
    CategoriaActualizada,
    CategoriaPublica,
)
from app.modelos import categoriagasto as categoria
from app.core.dependencias import DepSesion, UsuarioActual

router = APIRouter(tags=["Categorias"])


@router.get("/", response_model=list[CategoriaPublica])
def obtener_categorias_usuario(db: DepSesion, usuario: UsuarioActual) -> Any:
    categorias = categoria.buscar_categorias_usuario(db, usuario.id_usuario)

    if not categorias:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron categorias"
        )

    return categorias


@router.post("/", response_model=CategoriaPublica)
def registrar_categorias(
    db: DepSesion, datos_categoria: CategoriaIngreso, usuario: UsuarioActual
) -> Any:
    categoria_creada = categoria.registrar_categoria_gasto(
        nueva_categoria=datos_categoria, id_usuario=usuario.id_usuario, db=db
    )

    if not categoria_creada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se registrar la categoria",
        )

    return categoria_creada


@router.patch("/", response_model=CategoriaPublica)
def actualizar_categoria(
    db: DepSesion, usuario: UsuarioActual, datos_categoria: CategoriaActualizada
) -> Any:
    nueva_categoria = categoria.actualizar_categoria(db=db, categoria=datos_categoria)

    if not nueva_categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar la categoria",
        )

    return nueva_categoria
