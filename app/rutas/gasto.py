from typing import Any, Annotated
from datetime import date

from fastapi import APIRouter, HTTPException, status, Query, Path

from app.esquemas.gasto import (
    GastoPublico,
    GastoIngreso,
    GastoIngresoCompleto,
    GastoActualizado,
    GastoPublicoReducido,
)
from app.modelos import gasto
from app.core.dependencias import DepSesion, UsuarioActual
from app.core.fechas import obtener_fecha_actual

router = APIRouter(tags=["Gastos"])


@router.post("/", response_model=GastoPublicoReducido)
def registrar_gasto(
    db: DepSesion, usuario: UsuarioActual, datos_gasto: GastoIngreso
) -> Any:
    gasto_completo = GastoIngresoCompleto(
        **datos_gasto.model_dump(), id_usuario=usuario.id_usuario
    )
    nuevo_gasto = gasto.registrar(db=db, gasto=gasto_completo)

    if not nuevo_gasto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo registrar el gasto",
        )

    return nuevo_gasto


@router.get("/", response_model=list[GastoPublico])
def obtener_gastos(
    db: DepSesion,
    usuario: UsuarioActual,
    fecha_inicio: Annotated[date | None, Query(alias="fecha-inicio")] = None,
    fecha_final: Annotated[date | None, Query(alias="fecha-final")] = None,
) -> Any:
    fecha_inicio = fecha_inicio or obtener_fecha_actual()
    fecha_final = fecha_final or obtener_fecha_actual()

    if fecha_inicio > fecha_final:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Fechas incorrectas"
        )

    gastos = gasto.obtener_por_us_fechas(
        db=db,
        id_usuario=usuario.id_usuario,
        fecha_inicio=fecha_inicio,
        fecha_final=fecha_final,
    )

    if not gastos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron gastos"
        )

    return gastos


@router.get("/{id_gasto}", response_model=GastoPublico)
def obtener_gasto(
    db: DepSesion, usuario: UsuarioActual, id_gasto: Annotated[int, Path(gt=0)]
):
    datos_gasto = gasto.obtener_por_id(db=db, id_gasto=id_gasto)

    if not datos_gasto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No se encontro el gasto"
        )

    return datos_gasto


@router.put("/", response_model=GastoPublico)
def actualizar_gasto(
    db: DepSesion, usuario: UsuarioActual, gasto_actualizado: GastoActualizado
):
    nuevo_gasto = gasto.actualizar(db=db, gasto=gasto_actualizado)

    if not nuevo_gasto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar el gasto",
        )

    return nuevo_gasto
