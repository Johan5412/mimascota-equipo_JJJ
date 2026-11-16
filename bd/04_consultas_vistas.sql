-- ==========================================================
-- ENTREGABLE BD4: VISTAS Y CONSULTAS COMPLEJAS (PARTE 1)
-- ==========================================================

-- ----------------------------------------------------------
-- SECCIÓN A: LAS 3 VISTAS (Reportes Gerenciales Automáticos)
-- ----------------------------------------------------------

-- VISTA 1: Reporte integral de citas (Cruza 5 tablas para dar el contexto completo)
CREATE OR REPLACE VIEW vista_reporte_citas AS
SELECT
    c.id_cita,
    c.fecha_hora,
    m.nombre AS mascota,
    p.nombre AS propietario,
    v.nombre AS veterinario,
    s.nombre_servicio,
    c.estado
FROM cita c
JOIN mascota m ON c.id_mascota = m.id_mascota
JOIN historial_propietario hp ON m.id_mascota = hp.id_mascota AND hp.fecha_fin IS NULL
JOIN propietario p ON hp.id_propietario = p.id_propietario
JOIN veterinario v ON c.id_veterinario = v.id_veterinario
JOIN servicio s ON c.id_servicio = s.id_servicio;

-- VISTA 2: Alerta de Vacunas próximas (Usa funciones de fecha como DATEDIFF y CURDATE)
CREATE OR REPLACE VIEW vista_alertas_vacunas AS
SELECT
    m.nombre AS mascota,
    m.especie,
    p.nombre AS propietario,
    p.telefono,
    va.nombre_vacuna,
    va.fecha_proxima_dosis,
    DATEDIFF(va.fecha_proxima_dosis, CURDATE()) AS dias_restantes
FROM vacuna va
JOIN mascota m ON va.id_mascota = m.id_mascota
JOIN historial_propietario hp ON m.id_mascota = hp.id_mascota AND hp.fecha_fin IS NULL
JOIN propietario p ON hp.id_propietario = p.id_propietario
WHERE m.estado = 'activa';

-- VISTA 3: Resumen financiero por tipo de servicio (Suma el dinero generado)
CREATE OR REPLACE VIEW vista_ingresos_servicios AS
SELECT
    s.nombre_servicio,
    COUNT(c.id_cita) AS cantidad_prestada,
    SUM(s.precio) AS ingresos_totales
FROM cita c
JOIN servicio s ON c.id_servicio = s.id_servicio
WHERE c.estado = 'atendida'
GROUP BY s.nombre_servicio;

-- CONSULTA 1: Top 3 de mascotas con mayor número de atenciones médicas.
-- Aplica: JOIN, GROUP BY, ORDER BY, LIMIT
SELECT
    m.nombre AS mascota,
    m.especie,
    COUNT(c.id_cita) AS total_visitas
FROM mascota m
JOIN cita c ON m.id_mascota = c.id_mascota
WHERE c.estado = 'atendida'
GROUP BY m.id_mascota
ORDER BY total_visitas DESC
LIMIT 3;

-- CONSULTA 2: Veterinarios y los ingresos que han generado, mostrando solo los que superan $100,000.
-- Aplica: JOIN múltiple, SUM, GROUP BY, y HAVING (filtro sobre grupos)
SELECT
    v.nombre AS veterinario,
    COUNT(c.id_cita) AS citas_atendidas,
    SUM(s.precio) AS total_generado
FROM veterinario v
JOIN cita c ON v.id_veterinario = c.id_veterinario
JOIN servicio s ON c.id_servicio = s.id_servicio
WHERE c.estado = 'atendida'
GROUP BY v.id_veterinario
HAVING total_generado > 100000
ORDER BY total_generado DESC;

-- CONSULTA 3: Historial médico detallado de una mascota en específico (ej. 'Max'), incluyendo sus medicamentos.
-- Aplica: 4 JOINs anidados
SELECT
    c.fecha_hora AS fecha_consulta,
    m.nombre AS mascota,
    hc.diagnostico,
    IFNULL(med.nombre_medicamento, 'Sin medicamentos') AS medicamento,
    IFNULL(da.dosis, 'N/A') AS dosis
FROM cita c
JOIN mascota m ON c.id_mascota = m.id_mascota
JOIN historial_clinico hc ON c.id_cita = hc.id_cita
LEFT JOIN detalle_atencion da ON hc.id_historial_clinico = da.id_historial_clinico
LEFT JOIN medicamento med ON da.id_medicamento = med.id_medicamento
WHERE m.nombre = 'Max';

-- CONSULTA 4: Top 5 de los mejores clientes (Dueños que más dinero han gastado en citas atendidas)
SELECT p.nombre AS cliente, SUM(s.precio) AS total_invertido
FROM propietario p
JOIN historial_propietario hp ON p.id_propietario = hp.id_propietario
JOIN mascota m ON hp.id_mascota = m.id_mascota
JOIN cita c ON m.id_mascota = c.id_mascota
JOIN servicio s ON c.id_servicio = s.id_servicio
WHERE c.estado = 'atendida'
GROUP BY p.id_propietario
ORDER BY total_invertido DESC
LIMIT 5;

-- CONSULTA 5: Mascotas que tienen sus vacunas vencidas (Cruza fechas con el día actual)
SELECT m.nombre, m.especie, v.nombre_vacuna, v.fecha_proxima_dosis
FROM mascota m
JOIN vacuna v ON m.id_mascota = v.id_mascota
WHERE v.fecha_proxima_dosis < CURDATE() AND m.estado = 'activa'
ORDER BY v.fecha_proxima_dosis ASC;

-- CONSULTA 6: Promedio de peso por raza para análisis clínico (Uso de AVG y ROUND)
SELECT m.raza, ROUND(AVG(hc.peso_actual), 2) AS peso_promedio_kg
FROM mascota m
JOIN cita c ON m.id_mascota = c.id_mascota
JOIN historial_clinico hc ON c.id_cita = hc.id_cita
GROUP BY m.raza
ORDER BY peso_promedio_kg DESC;

-- CONSULTA 7: Medicamentos más recetados y su comparación con el stock actual
SELECT m.nombre_medicamento, m.stock AS stock_actual, COUNT(da.id_medicamento) AS veces_recetado
FROM medicamento m
LEFT JOIN detalle_atencion da ON m.id_medicamento = da.id_medicamento
GROUP BY m.id_medicamento
ORDER BY veces_recetado DESC;

-- CONSULTA 8: Propietarios que tienen más de una mascota (Clientes frecuentes usando HAVING)
SELECT p.nombre, p.telefono, COUNT(hp.id_mascota) AS cantidad_mascotas
FROM propietario p
JOIN historial_propietario hp ON p.id_propietario = hp.id_propietario
WHERE hp.fecha_fin IS NULL
GROUP BY p.id_propietario
HAVING cantidad_mascotas > 1
ORDER BY cantidad_mascotas DESC;

-- CONSULTA 9: Historial de cancelaciones por veterinario (Para medir eficiencia)
SELECT v.nombre AS veterinario, COUNT(c.id_cita) AS citas_canceladas
FROM veterinario v
JOIN cita c ON v.id_veterinario = c.id_veterinario
WHERE c.estado = 'cancelada'
GROUP BY v.id_veterinario
ORDER BY citas_canceladas DESC;

-- CONSULTA 10: Mascotas que han sido adoptadas (Han tenido más de un dueño en su historial)
SELECT m.nombre, m.especie, COUNT(hp.id_historial) AS cantidad_duenos
FROM mascota m
JOIN historial_propietario hp ON m.id_mascota = hp.id_mascota
GROUP BY m.id_mascota
HAVING cantidad_duenos > 1;

-- CONSULTA 11: Resumen de facturación mensual en el año 2023 (Agrupamiento por Mes)
SELECT MONTH(c.fecha_hora) AS mes, SUM(s.precio) AS facturacion_mensual
FROM cita c
JOIN servicio s ON c.id_servicio = s.id_servicio
WHERE YEAR(c.fecha_hora) = 2023 AND c.estado = 'atendida'
GROUP BY MONTH(c.fecha_hora)
ORDER BY mes ASC;

-- CONSULTA 12: Pacientes Geriátricos (Mascotas de 5 años o más usando matemática de fechas)
SELECT nombre, especie, fecha_nacimiento,
       TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) AS edad_anios
FROM mascota
WHERE TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) >= 5 AND estado = 'activa'
ORDER BY edad_anios DESC;

-- CONSULTA 13: Diagnósticos más comunes en la clínica (Agrupación de texto)
SELECT diagnostico, COUNT(id_historial_clinico) AS numero_casos
FROM historial_clinico
GROUP BY diagnostico
ORDER BY numero_casos DESC
LIMIT 3;

-- CONSULTA 14: Distribución de la carga laboral (Cuántas citas totales maneja cada veterinario)
SELECT v.nombre, COUNT(c.id_cita) AS carga_citas
FROM veterinario v
LEFT JOIN cita c ON v.id_veterinario = c.id_veterinario
GROUP BY v.id_veterinario
ORDER BY carga_citas DESC;

-- CONSULTA 15: Mascotas inactivas (fallecidas o adoptadas externamente) y su último dueño registrado
SELECT m.nombre AS mascota, m.estado, p.nombre AS ultimo_dueno
FROM mascota m
JOIN historial_propietario hp ON m.id_mascota = hp.id_mascota
JOIN propietario p ON hp.id_propietario = p.id_propietario
WHERE m.estado IN ('fallecida', 'adoptada')
  AND (hp.fecha_fin IS NOT NULL OR hp.id_historial = (SELECT MAX(id_historial) FROM historial_propietario WHERE id_mascota = m.id_mascota));