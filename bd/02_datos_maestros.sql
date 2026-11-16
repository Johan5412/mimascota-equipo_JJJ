-- ==========================================================
-- INSERCIÓN DE DATOS
-- ==========================================================

-- 1. INSERCIÓN DE 20 PROPIETARIOS
INSERT INTO propietario (nombre, telefono, correo, direccion) VALUES
('Carlos Mario Ramirez', '3151234567', 'carlos.ramirez@email.com', 'Calle 4 # 5-23, Centro'),
('Maria Fernanda Lopez', '3209876543', 'mafe.lopez@email.com', 'Cra 9 # 12-45, Barrio Campanario'),
('Andres Felipe Muñoz', '3104567890', 'andres.munoz@email.com', 'Calle 15 # 3-12, La Esmeralda'),
('Diana Carolina Diaz', '3115678901', 'diana.diaz@email.com', 'Cra 2 # 8-90, Barrio Bolivar'),
('Luis Eduardo Gaviria', '3186789012', 'luis.gaviria@email.com', 'Calle 7 # 14-22, Prados del Norte'),
('Sandra Milena Rojas', '3147890123', 'sandra.rojas@email.com', 'Cra 6 # 1-15, Ciudad Jardin'),
('Juan Pablo Castillo', '3218901234', 'juan.castillo@email.com', 'Calle 18 # 5-67, Bello Horizonte'),
('Luz Dary Valencia', '3169012345', 'luz.valencia@email.com', 'Cra 11 # 20-34, Santa Clara'),
('Jorge Ivan Ospina', '3120123456', 'jorge.ospina@email.com', 'Calle 5 # 9-45, Centro'),
('Carmen Alicia Silva', '3171239876', 'carmen.silva@email.com', 'Cra 8 # 15-88, Pomona'),
('Victor Hugo Morales', '3192348765', 'victor.morales@email.com', 'Calle 22 # 4-56, La Paz'),
('Patricia Helena Ruiz', '3133457654', 'patricia.ruiz@email.com', 'Cra 3 # 11-23, Modelo'),
('Oscar David Guzman', '3224566543', 'oscar.guzman@email.com', 'Calle 9 # 18-90, El Recuerdo'),
('Claudia Patricia Gomez','3155675432', 'claudia.gomez@email.com', 'Cra 15 # 7-12, Los Hoyos'),
('Diego Fernando Cruz', '3106784321', 'diego.cruz@email.com', 'Calle 13 # 2-34, San Jose'),
('Angela Maria Toro', '3117893210', 'angela.toro@email.com', 'Cra 5 # 19-45, Tomas Cipriano'),
('Ricardo Antonio Vega', '3188902109', 'ricardo.vega@email.com', 'Calle 10 # 6-78, Centro'),
('Martha Lucia Ortiz', '3149011098', 'martha.ortiz@email.com', 'Cra 7 # 22-11, Aida Lucia'),
('Hernan Dario Gomez', '3210120987', 'hernan.gomez@email.com', 'Calle 16 # 8-99, Cadillal'),
('Gloria Ines Vargas', '3161239988', 'gloria.vargas@email.com', 'Cra 10 # 13-44, Las Americas');

-- 2. INSERCIÓN DE 4 VETERINARIOS
INSERT INTO veterinario (nombre, tarjeta_profesional, telefono) VALUES
('Dr. Roberto Jaramillo', 'TP-90812', '3101112233'),
('Dra. Laura Montes', 'TP-77634', '3152223344'),
('Dr. Julian Bastidas', 'TP-55421', '3203334455'),
('Dra. Sofia Vergara', 'TP-11298', '3184445566');

-- 3. INSERCIÓN DE 8 SERVICIOS CLÍNICOS
INSERT INTO servicio (nombre_servicio, precio) VALUES
('Consulta General', 45000.00),
('Consulta Especializada', 70000.00),
('Vacunación', 35000.00),
('Desparasitación', 25000.00),
('Profilaxis Dental', 120000.00),
('Radiografía', 85000.00),
('Ecografía', 95000.00),
('Esterilización', 150000.00);

-- 4. INSERCIÓN DE 10 MEDICAMENTOS (INVENTARIO)
INSERT INTO medicamento (nombre_medicamento, stock) VALUES
('Bravecto 10-20kg', 15),
('NexGard Spectra', 20),
('Meloxicam 1mg', 50),
('Amoxicilina 250mg', 100),
('Doxiciclina 100mg', 80),
('Tramadol gotas', 30),
('Prednisolona 5mg', 60),
('Omeprazol 10mg', 45),
('Ketoconazol champú', 25),
('Complejo B Inyectable', 40);

-- 5. INSERCIÓN DE 30 MASCOTAS
INSERT INTO mascota (nombre, especie, raza, fecha_nacimiento, sexo, estado) VALUES
('Max', 'Perro', 'Labrador Retriever', '2020-05-15', 'Macho', 'activa'),
('Luna', 'Gato', 'Mestizo', '2021-08-20', 'Hembra', 'activa'),
('Rocky', 'Perro', 'Pitbull', '2019-11-10', 'Macho', 'activa'),
('Bella', 'Perro', 'Poodle', '2022-02-28', 'Hembra', 'activa'),
('Milo', 'Gato', 'Siamés', '2023-01-05', 'Macho', 'activa'),
('Kira', 'Perro', 'Husky Siberiano', '2020-09-12', 'Hembra', 'activa'),
('Toby', 'Perro', 'Beagle', '2021-04-18', 'Macho', 'activa'),
('Mia', 'Gato', 'Persa', '2022-07-22', 'Hembra', 'activa'),
('Zeus', 'Perro', 'Pastor Alemán', '2018-12-03', 'Macho', 'activa'),
('Nala', 'Perro', 'Golden Retriever', '2023-03-15', 'Hembra', 'activa'),
('Simba', 'Gato', 'Mestizo', '2020-10-30', 'Macho', 'activa'),
('Lola', 'Perro', 'Bulldog Francés', '2021-11-25', 'Hembra', 'activa'),
('Bruno', 'Perro', 'Boxer', '2019-06-08', 'Macho', 'activa'),
('Chloe', 'Gato', 'Angora', '2022-09-14', 'Hembra', 'activa'),
('Thor', 'Perro', 'Rottweiler', '2020-01-20', 'Macho', 'activa'),
('Sasha', 'Perro', 'Mestizo', '2021-05-12', 'Hembra', 'activa'),
('Leo', 'Gato', 'Maine Coon', '2023-04-02', 'Macho', 'activa'),
('Coco', 'Perro', 'Pug', '2022-08-19', 'Macho', 'activa'),
('Princesa', 'Perro', 'Chihuahua', '2019-03-27', 'Hembra', 'activa'),
('Garfield', 'Gato', 'Mestizo', '2018-07-11', 'Macho', 'activa'),
('Apolo', 'Perro', 'Dálmata', '2021-02-14', 'Macho', 'fallecida'),
('Fiona', 'Perro', 'Schnauzer', '2020-12-05', 'Hembra', 'activa'),
('Tom', 'Gato', 'Siamés', '2022-05-29', 'Macho', 'adoptada'),
('Nina', 'Perro', 'Mestizo', '2023-06-10', 'Hembra', 'activa'),
('Rambo', 'Perro', 'Doberman', '2019-08-22', 'Macho', 'activa'),
('Pelusa', 'Gato', 'Persa', '2021-01-17', 'Hembra', 'activa'),
('Jack', 'Perro', 'Jack Russell', '2020-04-08', 'Macho', 'activa'),
('Maya', 'Perro', 'Border Collie', '2022-10-03', 'Hembra', 'activa'),
('Salem', 'Gato', 'Mestizo', '2019-09-25', 'Macho', 'fallecida'),
('Duke', 'Perro', 'Gran Danés', '2021-07-07', 'Macho', 'activa');

-- 6. ASIGNACIÓN DE MASCOTAS A PROPIETARIOS (REGLA DE NEGOCIO 1)
-- Se asigna 1 o 2 mascotas a cada uno de los primeros 20 propietarios
INSERT INTO historial_propietario (id_mascota, id_propietario, fecha_inicio, fecha_fin) VALUES
(1, 1, '2020-07-01', NULL),
(2, 2, '2021-10-15', NULL),
(3, 3, '2020-01-20', NULL),
(4, 4, '2022-04-10', NULL),
(5, 5, '2023-02-15', NULL),
(6, 6, '2020-11-05', NULL),
(7, 7, '2021-06-10', NULL),
(8, 8, '2022-09-01', NULL),
(9, 9, '2019-02-15', NULL),
(10, 10, '2023-05-20', NULL),
(11, 11, '2020-12-10', NULL),
(12, 12, '2022-01-15', NULL),
(13, 13, '2019-08-20', NULL),
(14, 14, '2022-11-05', NULL),
(15, 15, '2020-03-10', NULL),
(16, 16, '2021-07-22', NULL),
(17, 17, '2023-06-05', NULL),
(18, 18, '2022-10-15', NULL),
(19, 19, '2019-05-10', NULL),
(20, 20, '2018-09-15', NULL),
(21, 1, '2021-04-10', '2023-08-15'), -- Mascota fallecida, tiene fecha_fin
(22, 2, '2021-02-20', NULL),
(23, 3, '2022-07-15', '2023-11-01'), -- Mascota adoptada por otro
(24, 4, '2023-08-01', NULL),
(25, 5, '2019-10-10', NULL),
(26, 6, '2021-03-15', NULL),
(27, 7, '2020-06-20', NULL),
(28, 8, '2022-12-10', NULL),
(29, 9, '2019-11-05', '2022-04-20'), -- Mascota fallecida
(30, 10, '2021-09-15', NULL);