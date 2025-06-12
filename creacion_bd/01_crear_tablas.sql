CREATE EXTENSION "uuid-ossp"

CREATE TABLE usuarios(
    id_usuario SERIAL PRIMARY KEY NOT NULL,
    codigo_usuario UUID NOT NULL DEFAULT uuid_generate_v4(),
    nombre_usuario VARCHAR(25) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL,
    contrasenia TEXT,
    version_sesion INT DEFAULT 1
);

CREATE TABLE categorias_gastos(
    id_categoria SERIAL PRIMARY KEY NOT NULL,
    nombre_categoria
);

CREATE TABLE usuarios_categorias(
    id_usuario_categoria SERIAL PRIMARY KEY,
    id_usuario INT,
    id_categoria INT
);

CREATE TABLE gastos(
    id_gasto BIGSERIAL PRIMARY KEY,
    id_categoria INT,
    descripcion VARCHAR(250),
    monto DECIMAL(18,2),
    fecha_gasto DATE,
    id_usuario INT
);

/* CREACION DE RELACIONES */
ALTER TABLE usuarios_categorias ADD FOREIGN KEY ("id_usuario") REFERENCES "usuarios" ("id_usuario");
ALTER TABLE usuarios_categorias ADD FOREIGN KEY ("id_categoria") REFERENCES "categorias_gastos" ("id_categoria");

ALTER TABLE gastos ADD FOREIGN KEY ("id_usuario") REFERENCES "usuarios" ("id_usuario");