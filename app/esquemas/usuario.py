from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class UsuarioBase(BaseModel):
    nombre_usuario: str = Field(max_length=25, pattern=r"^[a-zA-z0-9ñáéíóúÁÉÍÓÚ]*$")
    correo_electronico: EmailStr = Field(max_length=25)


class UsuarioIngreso(UsuarioBase):
    contrasenia: str = Field(max_length=50)


class UsuarioIngresoDB(UsuarioBase):
    contrasenia: str = Field()


class UsuarioDB(UsuarioBase):
    id_usuario: int = Field()
    codigo_usuario: UUID = Field()
    contrasenia: str = Field()
    version_sesion: int = Field()


class UsuarioSaliente(UsuarioBase):
    pass
