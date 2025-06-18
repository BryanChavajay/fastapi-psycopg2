from pydantic import BaseModel, Field


class CategoriaGastoBase(BaseModel):
    nombre_categoria: str = Field(max_length=50)


class CategoriaIngreso(CategoriaGastoBase):
    pass


class CategoriaActualizada(CategoriaGastoBase):
    id_categoria: int


class CategoriaPublica(CategoriaGastoBase):
    id_categoria: int
