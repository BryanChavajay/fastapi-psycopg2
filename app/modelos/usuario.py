from psycopg2.extensions import connection

from app.esquemas.usuario import UsuarioIngreso, UsuarioIngresoDB, UsuarioDB
from app.core.utilidades import CATEGORIAS_GASTOS_DEFECTO
from app.core.seguridad import obtener_hash_contrasenia, verificar_contrasenia


def registrar_usuario(
    nuevo_usuario: UsuarioIngreso, db: connection
) -> UsuarioDB | None:
    cursor = db.cursor()

    consulta = """
                SELECT nombre_usuario, correo_electronico FROM usuarios
                WHERE nombre_usuario=%s OR correo_electronico=%s
                """
    cursor.execute(
        consulta, (nuevo_usuario.nombre_usuario, nuevo_usuario.correo_electronico)
    )
    usuario_registrado = cursor.fetchone()

    if usuario_registrado is not None:
        cursor.close()
        return None

    contrasenia_hasheada = obtener_hash_contrasenia(nuevo_usuario.contrasenia)
    usuario_db = UsuarioIngresoDB(
        contrasenia=contrasenia_hasheada,
        correo_electronico=nuevo_usuario.correo_electronico,
        nombre_usuario=nuevo_usuario.nombre_usuario,
    )
    consulta = """
                INSERT INTO usuarios(nombre_usuario, correo_electronico, contrasenia) VALUES
                (%(nombre_usuario)s,%(correo_electronico)s,%(contrasenia)s) RETURNING 
                id_usuario, nombre_usuario, correo_electronico, contrasenia, codigo_usuario, version_sesion
                """
    cursor.execute(consulta, usuario_db.model_dump())
    us = cursor.fetchone()

    if us is None:
        cursor.close()
        return None

    consulta = """
                INSERT INTO categorias_gastos(nombre_categoria) VALUES 
                (%s) RETURNING id_categoria
                """
    cursor.executemany(consulta, CATEGORIAS_GASTOS_DEFECTO)
    cats = cursor.fetchall()

    categorias_del_usuario = [(us[0], cat[0]) for cat in cats]
    consulta = """
                INSERT INTO usuarios_categorias (id_usuario, id_categoria) VALUES (%s, %s)
                RETURNING id_usuario
                """
    cursor.executemany(consulta, categorias_del_usuario)
    cats_us = cursor.fetchone()

    if cats_us is None:
        cursor.close()
        return None

    cursor.close()
    db.commit()

    usuario_registrado = UsuarioDB(
        id_usuario=us[0],
        nombre_usuario=us[1],
        correo_electronico=us[2],
        contrasenia=us[3],
        codigo_usuario=us[4],
        version_sesion=us[5],
    )
    return usuario_registrado


def obtener_usuario_por_id(id_usuario: int, db: connection) -> UsuarioDB | None:
    cursor = db.cursor()

    consulta = """
    SELECT id_usuario, codigo_usuario, nombre_usuario, correo_electronico, contrasenia, version_sesion FROM usuarios WHERE id_usuario=%s
    """

    cursor.execute(consulta, (id_usuario,))

    usuario = cursor.fetchone()

    if usuario is None:
        return None

    datos_usuario = UsuarioDB(
        id_usuario=usuario[0],
        codigo_usuario=usuario[1],
        nombre_usuario=usuario[2],
        correo_electronico=usuario[3],
        contrasenia=usuario[4],
        version_sesion=usuario[5],
    )

    return datos_usuario


def obtener_usuario_por_codigo(codigo_usuario: str, db: connection) -> UsuarioDB | None:
    cursor = db.cursor()

    consulta = """
    SELECT id_usuario, codigo_usuario, nombre_usuario, correo_electronico, contrasenia, version_sesion FROM usuarios WHERE codigo_usuario=%s
    """

    cursor.execute(consulta, (codigo_usuario,))

    usuario = cursor.fetchone()

    if usuario is None:
        return None

    datos_usuario = UsuarioDB(
        id_usuario=usuario[0],
        codigo_usuario=usuario[1],
        nombre_usuario=usuario[2],
        correo_electronico=usuario[3],
        contrasenia=usuario[4],
        version_sesion=usuario[5],
    )

    return datos_usuario


def obtener_usuario_por_correo_o_usuario(
    correo_usuario: str, db: connection
) -> UsuarioDB | None:
    cursor = db.cursor()

    consulta = """
    SELECT id_usuario, codigo_usuario, nombre_usuario, correo_electronico, contrasenia, version_sesion FROM usuarios WHERE correo_electronico=%s OR nombre_usuario=%s
    """

    cursor.execute(consulta, (correo_usuario,))

    usuario = cursor.fetchone()

    if usuario is None:
        return None

    datos_usuario = UsuarioDB(
        id_usuario=usuario[0],
        codigo_usuario=usuario[1],
        nombre_usuario=usuario[2],
        correo_electronico=usuario[3],
        contrasenia=usuario[4],
        version_sesion=usuario[5],
    )

    return datos_usuario


def autenticar_usuario(
    correo_o_usuario: str, contrasenia: str, db: connection
) -> UsuarioDB | None:
    cursor = db.cursor()

    consulta = """
    SELECT id_usuario, codigo_usuario, nombre_usuario, correo_electronico, contrasenia, version_sesion FROM usuarios WHERE correo_electronico=%s OR nombre_usuario=%s
    """

    cursor.execute(consulta, (correo_o_usuario,correo_o_usuario))

    usuario = cursor.fetchone()

    if usuario is None:
        return None

    datos_usuario = UsuarioDB(
        id_usuario=usuario[0],
        codigo_usuario=usuario[1],
        nombre_usuario=usuario[2],
        correo_electronico=usuario[3],
        contrasenia=usuario[4],
        version_sesion=usuario[5],
    )

    if not verificar_contrasenia(datos_usuario.contrasenia, contrasenia):
        return None

    return datos_usuario
