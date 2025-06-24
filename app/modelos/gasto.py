from psycopg2.extensions import connection
from datetime import date


from app.esquemas.gasto import (
    GastoIngresoCompleto,
    GastoDB,
    GastoCategoriaDB,
    GastoActualizado,
)


def registrar(db: connection, gasto: GastoIngresoCompleto) -> GastoDB | None:
    cursor = db.cursor()

    consulta = """
                INSERT INTO gastos (id_categoria, descripcion, monto, fecha_gasto, id_usuario)
                VALUES (%(id_categoria)s,%(descripcion)s,%(monto)s,%(fecha_gasto)s,%(id_usuario)s)
                RETURNING id_gasto, id_categoria, descripcion, monto, fecha_gasto, id_usuario
                """
    cursor.execute(consulta, gasto.model_dump())
    gasto_creado = cursor.fetchone()

    if not gasto_creado:
        cursor.close()
        return None

    cursor.close()
    db.commit()
    return GastoDB(
        id_gasto=gasto_creado[0],
        id_categoria=gasto_creado[1],
        descripcion=gasto_creado[2],
        monto=gasto_creado[3],
        fecha_gasto=gasto_creado[4],
        id_usuario=gasto_creado[5],
    )


def obtener_por_id(db: connection, id_gasto: int) -> None | GastoCategoriaDB:
    curso = db.cursor()

    consulta = """
                SELECT gas.id_gasto, gas.id_categoria, gas.descripcion, gas.monto, 
                gas.fecha_gasto, gas.id_usuario, catgas.nombre_categoria
                FROM gastos gas
                INNER JOIN
                    categorias_gastos catgas ON gas.id_categoria = catgas.id_categoria
                WHERE gas.id_gasto=%s
                """
    curso.execute(consulta, (id_gasto,))
    gasto = curso.fetchone()

    if not gasto:
        curso.close()
        return None

    curso.close()
    db.commit()
    return GastoCategoriaDB(
        id_gasto=gasto[0],
        id_categoria=gasto[1],
        descripcion=gasto[2],
        monto=gasto[3],
        fecha_gasto=gasto[4],
        id_usuario=gasto[5],
        nombre_categoria=gasto[6],
    )


def obtener_por_us_fechas(
    db: connection, id_usuario: int, fecha_inicio: date, fecha_final: date
) -> None | list[GastoCategoriaDB]:
    cursor = db.cursor()
    consulta = """
                SELECT gas.id_gasto, gas.id_categoria, gas.descripcion, gas.monto, 
                gas.fecha_gasto, gas.id_usuario, catgas.nombre_categoria
                FROM gastos gas
                INNER JOIN
                    categorias_gastos catgas ON gas.id_categoria = catgas.id_categoria
                WHERE gas.id_usuario=%s AND (gas.fecha_gasto>=%s AND gas.fecha_gasto<=%s)
                """
    cursor.execute(consulta, (id_usuario, fecha_inicio, fecha_final))
    gastos = cursor.fetchall()

    if not gastos:
        cursor.close()
        return None

    cursor.close()
    db.commit()
    return [
        GastoCategoriaDB(
            id_gasto=gasto[0],
            id_categoria=gasto[1],
            descripcion=gasto[2],
            monto=gasto[3],
            fecha_gasto=gasto[4],
            id_usuario=gasto[5],
            nombre_categoria=gasto[6],
        )
        for gasto in gastos
    ]


def actualizar(db: connection, gasto: GastoActualizado) -> None | GastoDB:
    cursor = db.cursor()
    consulta = """
                UPDATE gastos SET id_categoria=%(id_categoria)s, descripcion=%(descripcion)s, 
                monto=%(monto)s, fecha_gasto=%(fecha_gasto)s
                WHERE id_gasto=%(id_gasto)s
                RETURNING id_gasto, id_categoria, descripcion, monto, fecha_gasto, id_usuario
                """
    cursor.execute(consulta, gasto.model_dump())
    gasto_actualizado = cursor.fetchone()

    if not gasto_actualizado:
        cursor.close()
        return None

    cursor.close()
    db.commit()
    return GastoDB(
        id_gasto=gasto_actualizado[0],
        id_categoria=gasto_actualizado[1],
        descripcion=gasto_actualizado[2],
        monto=gasto_actualizado[3],
        fecha_gasto=gasto_actualizado[4],
        id_usuario=gasto_actualizado[5],
    )
