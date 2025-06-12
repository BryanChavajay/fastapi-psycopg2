from fastapi import APIRouter

from app.esquemas.usuario import UsuarioSaliente
from app.core.dependencias import UsuarioActual, DepSesion

router = APIRouter(tags=["Usuarios"])


@router.get("/me", response_model=UsuarioSaliente)
def quien_soy(db: DepSesion, usuario_actual: UsuarioActual):
    return usuario_actual
