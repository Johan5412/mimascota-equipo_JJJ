-- Migración de la tabla veterinario para bases ya creadas con el esquema anterior.
-- Ejecutar una sola vez; no ejecutar sobre una base recién creada con 01_ddl.sql.

USE administracionmascotasbd;

ALTER TABLE veterinario
    ADD COLUMN especialidad VARCHAR(60) NULL AFTER nombre,
    ADD COLUMN correo VARCHAR(100) NULL AFTER telefono;

UPDATE veterinario
SET especialidad = CASE tarjeta_profesional
        WHEN 'TP-90812' THEN 'Medicina general'
        WHEN 'TP-77634' THEN 'Medicina felina'
        WHEN 'TP-55421' THEN 'Cirugía veterinaria'
        WHEN 'TP-11298' THEN 'Dermatología veterinaria'
        ELSE 'Medicina general'
    END,
    correo = CASE tarjeta_profesional
        WHEN 'TP-90812' THEN 'roberto.jaramillo@mimascota.com'
        WHEN 'TP-77634' THEN 'laura.montes@mimascota.com'
        WHEN 'TP-55421' THEN 'julian.bastidas@mimascota.com'
        WHEN 'TP-11298' THEN 'sofia.vergara@mimascota.com'
        ELSE CONCAT('veterinario', id_veterinario, '@mimascota.com')
    END;

ALTER TABLE veterinario
    MODIFY COLUMN especialidad VARCHAR(60) NOT NULL,
    MODIFY COLUMN correo VARCHAR(100) NOT NULL,
    ADD CONSTRAINT uq_veterinario_correo UNIQUE (correo);
