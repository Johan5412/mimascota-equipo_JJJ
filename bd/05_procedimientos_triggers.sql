-- ==========================================================
-- ENTREGABLE BD5: PROCEDIMIENTOS ALMACENADOS Y TRIGGERS
-- ==========================================================

DELIMITER //

-- ----------------------------------------------------------
-- 1. PROCEDIMIENTO ALMACENADO (Validación de cruce de agendas)
-- Regla de Negocio: Un veterinario no puede tener dos citas a la misma hora.
-- ----------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_agendar_cita //

CREATE PROCEDURE sp_agendar_cita(
    IN p_id_mascota INT,
    IN p_id_veterinario INT,
    IN p_id_servicio INT,
    IN p_fecha_hora DATETIME
)
BEGIN
    DECLARE v_citas_cruzadas INT;

    -- Contamos si el veterinario ya tiene una cita agendada a esa hora exacta
    SELECT COUNT(*) INTO v_citas_cruzadas
    FROM cita
    WHERE id_veterinario = p_id_veterinario
      AND fecha_hora = p_fecha_hora
      AND estado IN ('programada', 'atendida');

    -- Si el conteo es mayor a 0, lanzamos un error y detenemos la inserción
    IF v_citas_cruzadas > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERROR DE NEGOCIO: El veterinario ya tiene una cita asignada en ese horario.';
    ELSE
        -- Si está libre, insertamos la cita exitosamente
        INSERT INTO cita (id_mascota, id_veterinario, id_servicio, fecha_hora, estado)
        VALUES (p_id_mascota, p_id_veterinario, p_id_servicio, p_fecha_hora, 'programada');
    END IF;
END //

-- ----------------------------------------------------------
-- 2. TRIGGER 1: Control Sanitario Estricto
-- Regla de Negocio: No se pueden vacunar mascotas fallecidas o adoptadas,
-- ni poner fechas de aplicación en el futuro.
-- ----------------------------------------------------------
DROP TRIGGER IF EXISTS trg_validar_vacuna_mascota //

CREATE TRIGGER trg_validar_vacuna_mascota
BEFORE INSERT ON vacuna
FOR EACH ROW
BEGIN
    DECLARE v_estado_mascota VARCHAR(20);

    -- Obtenemos el estado actual de la mascota antes de registrarle la vacuna
    SELECT estado INTO v_estado_mascota
    FROM mascota
    WHERE id_mascota = NEW.id_mascota;

    -- Validación A: Estado de la mascota
    IF v_estado_mascota != 'activa' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERROR DE NEGOCIO: No se pueden registrar vacunas a mascotas fallecidas o adoptadas.';
    END IF;

    -- Validación B: Fechas lógicas
    IF NEW.fecha_aplicacion > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERROR DE NEGOCIO: La fecha de aplicación de la vacuna no puede ser en el futuro.';
    END IF;
END //

-- ----------------------------------------------------------
-- 3. TRIGGER 2: Seguridad en el Historial Clínico
-- Regla de Negocio: Solo las citas con estado "atendida" pueden generar historial clínico.
-- ----------------------------------------------------------
DROP TRIGGER IF EXISTS trg_validar_historial_clinico //

CREATE TRIGGER trg_validar_historial_clinico
BEFORE INSERT ON historial_clinico
FOR EACH ROW
BEGIN
    DECLARE v_estado_cita VARCHAR(20);

    -- Buscamos el estado de la cita a la que se le quiere agregar el historial
    SELECT estado INTO v_estado_cita
    FROM cita
    WHERE id_cita = NEW.id_cita;

    -- Si la cita está programada o cancelada, se bloquea el registro médico
    IF v_estado_cita != 'atendida' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ERROR DE NEGOCIO: Solo se puede crear un historial clínico para citas con estado ATENDIDA.';
    END IF;
END //

DELIMITER ;