-- Create Tables
DROP TABLE Department;
DROP TABLE Class;
DROP TABLE Product;
DROP TABLE Family;

CREATE TABLE IF NOT EXISTS Department (
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Class (
    id_department INTEGER NOT NULL,
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id, id_department),
    FOREIGN KEY (id_department) REFERENCES Department(id)
);

CREATE TABLE IF NOT EXISTS Family (
    id_department INTEGER NOT NULL,
    id_class INTEGER NOT NULL,
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (id, id_class, id_department),
    FOREIGN KEY (id_department) REFERENCES Department(id),
    FOREIGN KEY (id_class) REFERENCES Class(id)
);

CREATE TABLE IF NOT EXISTS Product (
    sku INTEGER NOT NULL,
    id_department INTEGER NOT NULL,
    id_class INTEGER NOT NULL,
    id_family INTEGER NOT NULL,
    description TEXT NOT NULL,
    brand TEXT,
    model TEXT,
    stock INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    discontinued BOOLEAN NOT NULL DEFAULT FALSE,
    record_delete DATE NOT NULL DEFAULT "1900-01-01",
    record_data DATE NOT NULL,
    PRIMARY KEY (sku),
    FOREIGN KEY (id_department) REFERENCES Department(id),
    FOREIGN KEY (id_class) REFERENCES Class(id),
    FOREIGN KEY (id_family) REFERENCES Family(id)
);

-- Insert Department
INSERT OR IGNORE INTO Department
VALUES 
    (1, 'Domésticos'),
    (2, 'Electrónica'),
    (3, 'Muebles Sueltos'),
    (4, 'Salas, recamaras y comedores');

-- Insert Class
INSERT OR IGNORE INTO Class (id_department, id, name)
VALUES 
    (1, 1, 'Comestibles'),
    (1, 2, 'Licuadora'),
    (1, 3, 'Batidora'),
    (1, 4, 'Cafetera'),
    (2, 1, 'Amplificadores'),
    (2, 2, 'Auto stereos'),
    (3, 1, 'Colchón'),
    (3, 2, 'Juego box'),
    (4, 1, 'Salas'),
    (4, 2, 'Complementos para sala'),
    (4, 3, 'Sofá-camas');

INSERT OR IGNORE INTO Family (id_department, id_class, id, name)
VALUES
    (1, 1, 1, 'Sin nombre'),
    (1, 2, 1, 'Licuadoras'),
    (1, 2, 1, 'Exclusivo Coppel.com'),
    (1, 3, 1, 'Batidora manual'),
    (1, 3, 2, 'Procesador'),
    (1, 3, 3, 'Picadora'),
    (1, 3, 4, 'Batidora pedestal'),
    (1, 3, 5, 'Batidora fuente'),
    (1, 4, 1, 'Cafeteras'),
    (1, 4, 2, 'Precoladoras'),
    (2, 1, 1, 'Amplificador/Receptor'),
    (2, 1, 2, 'Kit de instalación'),
    (2, 1, 3, 'Amplificadores Coppel'),
    (2, 2, 1, 'Stero CD'),
    (2, 2, 2, 'Accesorio car audio'),
    (2, 2, 3, 'Amplificador'),
    (2, 2, 4, 'Alarma auto/casa/oficina'),
    (2, 2, 5, 'Sin mecanismo'),
    (2, 2, 6, 'Con CD'),
    (2, 2, 7, 'Multimedia'),
    (2, 2, 8, 'Paquete sin mecanismo'),
    (2, 2, 9, 'Paquete con CD'),
    (3, 1, 1, 'Pillow top ks'),
    (3, 1, 2, 'Pillow top double ks'),
    (3, 1, 3, 'Hule espuma ks'),
    (3, 2, 1, 'Estándar individual'),
    (3, 2, 2, 'Pillow top individual'),
    (4, 1, 1, 'Esquineras superiores'),
    (4, 1, 2, 'Tipo seleccional'),
    (4, 2, 1, 'Sillon ocasional'),
    (4, 2, 2, 'Puf'),
    (4, 2, 3, 'Baúl'),
    (4, 2, 4, 'Taburete'),
    (4, 3, 1, 'Sofá-cama tapizado'),
    (4, 3, 2, 'Sofá-cama clásico'),
    (4, 3, 3, 'Estudio')
;

INSERT OR IGNORE INTO Product (
    sku, description, id_department, id_class, id_family, stock, quantity, record_delete, model, brand, record_data, discontinued
) VALUES (1, 'Producto de prueba', 1, 1, 1, 10, 4, '1990-01-01', 'ASD', 'Mabe', '2024-02-10', False)