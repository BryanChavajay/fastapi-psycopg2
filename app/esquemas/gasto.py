from decimal import Decimal
from datetime import date
from pydantic import BaseModel, Field

from app.core.fechas import obtener_fecha_hora_actual


class GastoBase(BaseModel):
    descripcion: str = Field(max_length=250)
    monto: Decimal = Field(max_digits=18, decimal_places=2)
    fecha_gasto: date = Field(default_factory=lambda: obtener_fecha_hora_actual())


class GastoIngreso(GastoBase):
    id_categoria: int = Field(gt=0)


class GastoIngresoCompleto(GastoIngreso):
    id_usuario: int = Field(gt=0)


class GastoDB(GastoBase):
    id_gasto: int = Field(gt=0)
    id_categoria: int = Field(gt=0)
    id_usuario: int = Field(gt=0)


class GastoCategoriaDB(GastoDB):
    nombre_categoria: str = Field()


class GastoPublico(GastoBase):
    id_gasto: int = Field(gt=0)
    id_categoria: int = Field(gt=0)
    nombre_categoria: str = Field()


class GastoPublicoReducido(GastoBase):
    id_gasto: int = Field(gt=0)
    id_categoria: int = Field(gt=0)


class GastoActualizado(GastoBase):
    id_gasto: int = Field(gt=0)
    id_categoria: int = Field(gt=0)
