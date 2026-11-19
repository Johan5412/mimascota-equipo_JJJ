-- ==========================================================
-- 1. LIMPIEZA PREVENTIVA
-- Se borran en orden inverso a su creación (de hijos a padres)
-- ==========================================================
DROP TABLE IF EXISTS detalle_atencion;
DROP TABLE IF EXISTS historial_clinico;
DROP TABLE IF EXISTS cita;
DROP TABLE IF EXISTS vacuna;
DROP TABLE IF EXISTS historial_propietario;
DROP TABLE IF EXISTS mascota;
DROP TABLE IF EXISTS medicamento;
DROP TABLE IF EXISTS servicio;
DROP TABLE IF EXISTS veterinario;
DROP TABLE IF EXISTS propietario;

-- ==========================================================
-- 2. CREACIÓN DE TABLAS MAESTRAS (Sin Llaves Foráneas)
-- ==========================================================

CREATE TABLE propietario (
    id_propietario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100) UNIQUE,
    direccion VARCHAR(150)
);

CREATE TABLE veterinario (
    id_veterinario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    especialidad VARCHAR(60) NOT NULL,
    tarjeta_profesional VARCHAR(30) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE servicio (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_servicio VARCHAR(60) NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0) -- Restricción CHECK
);

CREATE TABLE medicamento (
    id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre_medicamento VARCHAR(60) NOT NULL,
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0) -- Restricción DEFAULT y CHECK
);

-- ==========================================================
-- 3. CREACIÓN DE TABLAS TRANSACCIONALES Y DEPENDIENTES
-- ==========================================================

CREATE TABLE mascota (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    especie VARCHAR(30) NOT NULL,
    raza VARCHAR(50),
    fecha_nacimiento DATE,
    sexo ENUM('Macho', 'Hembra') NOT NULL,
    estado ENUM('activa', 'fallecida', 'adoptada') NOT NULL DEFAULT 'activa'
);

CREATE TABLE historial_propietario (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_mascota INT NOT NULL,
    id_propietario INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    FOREIGN KEY (id_mascota) REFERENCES mascota(id_mascota),
    FOREIGN KEY (id_propietario) REFERENCES propietario(id_propietario)
);

CREATE TABLE vacuna (
    id_vacuna INT AUTO_INCREMENT PRIMARY KEY,
    id_mascota INT NOT NULL,
    nombre_vacuna VARCHAR(50) NOT NULL,
    fecha_aplicacion DATE NOT NULL,
    fecha_proxima_dosis DATE NOT NULL,
    FOREIGN KEY (id_mascota) REFERENCES mascota(id_mascota)
);

CREATE TABLE cita (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_mascota INT NOT NULL,
    id_veterinario INT NOT NULL,
    id_servicio INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    estado ENUM('programada', 'atendida', 'cancelada') NOT NULL DEFAULT 'programada',
    FOREIGN KEY (id_mascota) REFERENCES mascota(id_mascota),
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_veterinario),
    FOREIGN KEY (id_servicio) REFERENCES servicio(id_servicio)
);

CREATE TABLE historial_clinico (
    id_historial_clinico INT AUTO_INCREMENT PRIMARY KEY,
    id_cita INT UNIQUE NOT NULL, -- UNIQUE garantiza que 1 cita = 1 historial
    diagnostico TEXT NOT NULL,
    peso_actual DECIMAL(5,2) NOT NULL CHECK (peso_actual > 0),
    observaciones TEXT,
    FOREIGN KEY (id_cita) REFERENCES cita(id_cita)
);

CREATE TABLE detalle_atencion (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_historial_clinico INT NOT NULL,
    id_medicamento INT NOT NULL,
    dosis VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_historial_clinico) REFERENCES historial_clinico(id_historial_clinico),
    FOREIGN KEY (id_medicamento) REFERENCES medicamento(id_medicamento)
);

-- ==========================================================
-- 4. CREACIÓN DE LOS 3 ÍNDICES OBLIGATORIOS
-- ==========================================================
-- Acelera las consultas por especie, fechas de citas y vacunas por vencer
CREATE INDEX idx_mascota_especie ON mascota(especie);
CREATE INDEX idx_cita_fecha ON cita(fecha_hora);
CREATE INDEX idx_vacuna_proxima_dosis ON vacuna(fecha_proxima_dosis);