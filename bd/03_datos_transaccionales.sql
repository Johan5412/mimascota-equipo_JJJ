-- ==========================================================
-- ENTREGABLE BD3: INSERCIÓN DE DATOS (BLOQUE 2 - TRANSACCIONALES)
-- ==========================================================

-- 1. INSERCIÓN DE 60 CITAS
-- id_mascota (1-30), id_veterinario (1-4), id_servicio (1-8)
INSERT INTO cita (id_mascota, id_veterinario, id_servicio, fecha_hora, estado) VALUES
(1, 1, 1, '2023-01-10 08:00:00', 'atendida'), (2, 2, 3, '2023-01-10 09:00:00', 'atendida'),
(3, 3, 2, '2023-01-11 10:00:00', 'atendida'), (4, 4, 4, '2023-01-11 11:00:00', 'atendida'),
(5, 1, 5, '2023-01-12 14:00:00', 'atendida'), (6, 2, 6, '2023-01-12 15:00:00', 'atendida'),
(7, 3, 7, '2023-01-13 16:00:00', 'atendida'), (8, 4, 8, '2023-01-13 17:00:00', 'atendida'),
(9, 1, 1, '2023-02-14 08:30:00', 'atendida'), (10, 2, 3, '2023-02-14 09:30:00', 'atendida'),
(11, 3, 2, '2023-02-15 10:30:00', 'atendida'), (12, 4, 4, '2023-02-15 11:30:00', 'atendida'),
(13, 1, 5, '2023-02-16 14:30:00', 'atendida'), (14, 2, 6, '2023-02-16 15:30:00', 'atendida'),
(15, 3, 7, '2023-02-17 16:30:00', 'atendida'), (16, 4, 8, '2023-02-17 17:30:00', 'atendida'),
(17, 1, 1, '2023-03-20 08:00:00', 'atendida'), (18, 2, 3, '2023-03-20 09:00:00', 'atendida'),
(19, 3, 2, '2023-03-21 10:00:00', 'atendida'), (20, 4, 4, '2023-03-21 11:00:00', 'atendida'),
(21, 1, 5, '2023-03-22 14:00:00', 'atendida'), (22, 2, 6, '2023-03-22 15:00:00', 'atendida'),
(23, 3, 7, '2023-03-23 16:00:00', 'atendida'), (24, 4, 8, '2023-03-23 17:00:00', 'atendida'),
(25, 1, 1, '2023-04-24 08:30:00', 'atendida'), (26, 2, 3, '2023-04-24 09:30:00', 'atendida'),
(27, 3, 2, '2023-04-25 10:30:00', 'atendida'), (28, 4, 4, '2023-04-25 11:30:00', 'atendida'),
(29, 1, 5, '2023-04-26 14:30:00', 'atendida'), (30, 2, 6, '2023-04-26 15:30:00', 'atendida'),
-- Citas programadas (futuras o pendientes)
(1, 3, 1, '2026-12-01 08:00:00', 'programada'), (2, 4, 3, '2026-12-01 09:00:00', 'programada'),
(3, 1, 2, '2026-12-02 10:00:00', 'programada'), (4, 2, 4, '2026-12-02 11:00:00', 'programada'),
(5, 3, 5, '2026-12-03 14:00:00', 'programada'), (6, 4, 6, '2026-12-03 15:00:00', 'programada'),
(7, 1, 7, '2026-12-04 16:00:00', 'programada'), (8, 2, 8, '2026-12-04 17:00:00', 'programada'),
(9, 3, 1, '2026-12-05 08:30:00', 'programada'), (10, 4, 3, '2026-12-05 09:30:00', 'programada'),
(11, 1, 2, '2026-12-06 10:30:00', 'programada'), (12, 2, 4, '2026-12-06 11:30:00', 'programada'),
(13, 3, 5, '2026-12-07 14:30:00', 'programada'), (14, 4, 6, '2026-12-07 15:30:00', 'programada'),
(15, 1, 7, '2026-12-08 16:30:00', 'programada'), (16, 2, 8, '2026-12-08 17:30:00', 'programada'),
-- Citas canceladas
(17, 3, 1, '2023-05-10 08:00:00', 'cancelada'), (18, 4, 3, '2023-05-10 09:00:00', 'cancelada'),
(19, 1, 2, '2023-05-11 10:00:00', 'cancelada'), (20, 2, 4, '2023-05-11 11:00:00', 'cancelada'),
(21, 3, 5, '2023-05-12 14:00:00', 'cancelada'), (22, 4, 6, '2023-05-12 15:00:00', 'cancelada'),
(23, 1, 7, '2023-05-13 16:00:00', 'cancelada'), (24, 2, 8, '2023-05-13 17:00:00', 'cancelada'),
(25, 3, 1, '2023-06-14 08:30:00', 'cancelada'), (26, 4, 3, '2023-06-14 09:30:00', 'cancelada'),
(27, 1, 2, '2023-06-15 10:30:00', 'cancelada'), (28, 2, 4, '2023-06-15 11:30:00', 'cancelada'),
(29, 3, 5, '2023-06-16 14:30:00', 'cancelada'), (30, 4, 6, '2023-06-16 15:30:00', 'cancelada');

-- 2. INSERCIÓN DE 30 HISTORIALES CLÍNICOS (1 por cada cita atendida - id_cita del 1 al 30)
INSERT INTO historial_clinico (id_cita, diagnostico, peso_actual, observaciones) VALUES
(1, 'Chequeo general sano', 25.5, 'Todo normal'), (2, 'Gastroenteritis leve', 4.2, 'Dieta blanda por 3 días'),
(3, 'Dermatitis alérgica', 18.0, 'Evitar pollo'), (4, 'Otitis canina', 6.5, 'Limpieza semanal'),
(5, 'Control post-operatorio', 5.0, 'Herida sanando bien'), (6, 'Fractura de tibia', 22.1, 'Reposo absoluto'),
(7, 'Infección urinaria', 12.3, 'Control en 15 días'), (8, 'Conjuntivitis', 3.8, 'Aplicar gotas cada 8h'),
(9, 'Chequeo general sano', 30.5, 'Vacunas al día'), (10, 'Parásitos intestinales', 28.0, 'Desparasitación completa'),
(11, 'Problema renal incipiente', 4.5, 'Cambio a alimento medicado'), (12, 'Alergia estacional', 11.2, 'Baños medicados'),
(13, 'Soplo cardíaco leve', 24.0, 'Ecocardiograma sugerido'), (14, 'Gingivitis', 3.5, 'Programar profilaxis'),
(15, 'Golpe de calor', 45.0, 'Hidratación constante'), (16, 'Herida por mordedura', 15.6, 'Curaciones diarias'),
(17, 'Chequeo geriátrico', 6.8, 'Exámenes de sangre normales'), (18, 'Obesidad', 9.0, 'Reducir ración 20%'),
(19, 'Dolor articular', 3.2, 'Condroprotectores'), (20, 'Problema respiratorio', 4.1, 'Nebulizaciones'),
(21, 'Revisión cachorros', 19.5, 'Crecimiento adecuado'), (22, 'Cuerpo extraño estomacal', 7.5, 'Cirugía programada'),
(23, 'Intoxicación leve', 4.0, 'Vómito inducido exitoso'), (24, 'Chequeo general sano', 14.2, 'Todo normal'),
(25, 'Sarna sarcóptica', 26.8, 'Aislamiento temporal'), (26, 'Caída de pelo severa', 3.9, 'Suplemento vitamínico'),
(27, 'Fiebre de origen desconocido', 8.5, 'Antipiréticos y observación'), (28, 'Gastroenteritis severa', 16.0, 'Hospitalización 24h'),
(29, 'Traumatismo leve', 4.8, 'Analgésicos'), (30, 'Chequeo general sano', 50.5, 'Mascota muy activa');

-- 3. INSERCIÓN DE DETALLES DE ATENCIÓN (Recetas para los historiales 1 al 30)
INSERT INTO detalle_atencion (id_historial_clinico, id_medicamento, dosis) VALUES
(2, 8, '1/4 tableta cada 24h'), (3, 7, '1/2 tableta cada 12h'),
(4, 9, 'Baño semanal por 1 mes'), (6, 3, '1 tableta cada 24h por 5 días'),
(7, 4, '1 cápsula cada 12h por 7 días'), (8, 5, '1 gota cada 8h'),
(10, 2, '1 tableta dosis única'), (11, 8, '1/2 tableta cada 24h'),
(12, 9, 'Baño cada 15 días'), (14, 4, '1/2 cápsula cada 12h'),
(16, 4, '1 cápsula cada 8h'), (19, 3, '1/4 tableta cada 24h'),
(20, 7, '1/2 tableta cada 12h'), (23, 8, '1/4 tableta cada 12h'),
(25, 1, '1 tableta dosis única'), (26, 10, '1ml vía oral diario'),
(27, 3, '1/2 tableta cada 24h'), (28, 4, '1 cápsula cada 8h'),
(28, 8, '1/2 tableta cada 12h'), (29, 3, '1 tableta cada 24h');

-- 4. INSERCIÓN DE 50 VACUNAS
INSERT INTO vacuna (id_mascota, nombre_vacuna, fecha_aplicacion, fecha_proxima_dosis) VALUES
(1, 'Rabia', '2023-01-15', '2024-01-15'), (1, 'Hexavalente', '2023-02-10', '2024-02-10'),
(2, 'Triple Felina', '2023-03-05', '2024-03-05'), (2, 'Rabia', '2023-04-12', '2024-04-12'),
(3, 'Rabia', '2023-05-20', '2024-05-20'), (3, 'Parvovirus', '2023-06-18', '2024-06-18'),
(4, 'Pentavalente', '2023-07-22', '2024-07-22'), (4, 'Rabia', '2023-08-30', '2024-08-30'),
(5, 'Leucemia Felina', '2023-09-15', '2024-09-15'), (5, 'Rabia', '2023-10-25', '2024-10-25'),
(6, 'Rabia', '2023-11-11', '2024-11-11'), (6, 'Hexavalente', '2023-12-05', '2024-12-05'),
(7, 'Tos de las perreras', '2024-01-20', '2025-01-20'), (7, 'Rabia', '2024-02-28', '2025-02-28'),
(8, 'Triple Felina', '2024-03-15', '2025-03-15'), (8, 'Rabia', '2024-04-10', '2025-04-10'),
(9, 'Rabia', '2024-05-05', '2025-05-05'), (9, 'Pentavalente', '2024-06-12', '2025-06-12'),
(10, 'Parvovirus', '2024-07-08', '2025-07-08'), (10, 'Rabia', '2024-08-16', '2025-08-16'),
(11, 'Triple Felina', '2024-09-22', '2025-09-22'), (11, 'Rabia', '2024-10-30', '2025-10-30'),
(12, 'Rabia', '2024-11-15', '2025-11-15'), (12, 'Hexavalente', '2024-12-20', '2025-12-20'),
(13, 'Tos de las perreras', '2025-01-10', '2026-01-10'), (13, 'Rabia', '2025-02-18', '2026-02-18'),
(14, 'Leucemia Felina', '2025-03-25', '2026-03-25'), (14, 'Rabia', '2025-04-05', '2026-04-05'),
(15, 'Rabia', '2025-05-12', '2026-05-12'), (15, 'Pentavalente', '2025-06-22', '2026-06-22'),
(16, 'Parvovirus', '2025-07-30', '2026-07-30'), (16, 'Rabia', '2025-08-15', '2026-08-15'),
(17, 'Triple Felina', '2025-09-10', '2026-09-10'), (17, 'Rabia', '2025-10-20', '2026-10-20'),
(18, 'Rabia', '2025-11-05', '2026-11-05'), (18, 'Hexavalente', '2025-12-15', '2026-12-15'),
(19, 'Tos de las perreras', '2026-01-25', '2027-01-25'), (19, 'Rabia', '2026-02-10', '2027-02-10'),
(20, 'Triple Felina', '2026-03-18', '2027-03-18'), (20, 'Rabia', '2026-04-28', '2027-04-28'),
(21, 'Rabia', '2021-05-15', '2022-05-15'), (21, 'Pentavalente', '2022-06-10', '2023-06-10'),
(22, 'Parvovirus', '2026-07-20', '2027-07-20'), (22, 'Rabia', '2026-08-05', '2027-08-05'),
(23, 'Triple Felina', '2026-09-12', '2027-09-12'), (23, 'Rabia', '2026-10-22', '2027-10-22'),
(24, 'Rabia', '2026-11-08', '2027-11-08'), (24, 'Hexavalente', '2026-12-18', '2027-12-18'),
(25, 'Tos de las perreras', '2023-01-05', '2024-01-05'), (25, 'Rabia', '2024-02-15', '2025-02-15');