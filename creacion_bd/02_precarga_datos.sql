INSERT INTO usuarios(nombre_usuario, correo_electronico, contrasenia) VALUES
('GENERAL','general@general.com','$2b$12$c/cDe.TCsIpZyv3m64WM9ejb5/NOUoIUc4LSuiah1m0sM5U0HQqQm');
-- Contrasenia asdf1234

INSERT INTO categorias_gastos(nombre_categoria) VALUES ('Comestibles'), ('Ocio'), ('Electrónica'), ('Utilidades'),
('Ropa'), ('Salud'), ('Otros');

INSERT INTO usuarios_categorias (id_usuario, id_categoria) VALUES
(1,1), (1,2), (1,3), (1,4), (1,5),
(1,6), (1,7); 