from psycopg2.extensions import connection

from app.esquemas.categoriagasto import (
    CategoriaActualizada,
    CategoriaIngreso,
    CategoriaPublica,
)


def registrar_categoria_gasto(
    nueva_categoria: CategoriaIngreso, id_usuario: int, db: connection
) -> CategoriaPublica | None:
    cursor = db.cursor()

    consulta = """
                INSERT INTO categorias_gastos(nombre_categoria)
                VALUES (%(nombre_categoria)s) RETURNING id_categoria, nombre_categoria
                """
    cursor.execute(consulta, nueva_categoria.model_dump())
    categoria_creada = cursor.fetchone()

    if not categoria_creada:
        cursor.close()
        return None

    consulta = """
                INSERT INTO usuarios_categorias(id_usuario, id_categoria)
                VALUES (%s, %s) RETURNING id_usuario_categoria
                """
    cursor.execute(consulta, (id_usuario, categoria_creada[0]))
    categoria_registrada = cursor.fetchone()

    if not categoria_registrada:
        cursor.close()
        return None

    cursor.close()
    db.commit()

    return CategoriaPublica(
        id_categoria=categoria_creada[0], nombre_categoria=categoria_creada[1]
    )


def buscar_categorias_usuario(
    db: connection, id_usuario: int
) -> list[CategoriaPublica] | None:
    cursor = db.cursor()
    consulta = """
                SELECT a.id_categoria, b.nombre_categoria
                FROM usuarios_categorias AS a
                INNER JOIN categorias_gastos AS b
                    ON a.id_categoria = b.id_categoria
                WHERE a.id_usuario = %s
                """
    cursor.execute(consulta, (id_usuario,))
    categorias = cursor.fetchall()

    if not categorias:
        cursor.close()
        return None

    lista_categorias = [
        CategoriaPublica(id_categoria=categoria[0], nombre_categoria=categoria[1])
        for categoria in categorias
    ]
    cursor.close()
    db.commit()

    return lista_categorias


def actualizar_categoria(
    db: connection, categoria: CategoriaActualizada
) -> CategoriaPublica | None:
    cursor = db.cursor()

    consulta = """
                UPDATE categorias_gastos SET nombre_categoria=%(nombre_categoria)s
                WHERE id_categoria=%(id_categoria)s
                RETURNING id_categoria, nombre_categoria
                """
    cursor.execute(consulta, categoria.model_dump())
    nueva_categoria = cursor.fetchone()

    if not nueva_categoria:
        cursor.close()
        return None
    cursor.close()
    db.commit()

    return CategoriaPublica(
        id_categoria=nueva_categoria[0], nombre_categoria=nueva_categoria[1]
    )
