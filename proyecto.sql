--Creacion de la base de datos
CREATE DATABASE gestion_tickets;

--CRreacion del esquema o base de datos

CREATE SCHEMA IF NOT EXISTS Gestion_tickets;



--apartir de aqui se crean las tablas
SET search_path TO Gestion_tickets;

-- ENTIDADES DE PRIMER NIVEL

-- TABLA DEPARTAMENTOS
CREATE TABLE Departamentos (
  Id_departamento INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- DP001
  Nombre_departamento VARCHAR(50) UNIQUE NOT NULL,
  CONSTRAINT pk_departamentos PRIMARY KEY (Id_departamento)
);

-- TABLA SERVICIOS
CREATE TABLE Servicios (
  Id_servicio INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- SC001
  Nombre_servicio VARCHAR(100) NOT NULL,
  CONSTRAINT pk_servicios PRIMARY KEY (Id_servicio)
);

-- TABLA NIVELES DE IMPACTO
CREATE TABLE Niveles_impacto (
  Id_impacto INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- NI001
  Nombre_impacto VARCHAR(100) NOT NULL,
  Peso_impacto INT NOT NULL,
  CONSTRAINT pk_niveles_impacto PRIMARY KEY (Id_impacto)
);

-- TABLA PLANTILLA DE FORMULARIO
CREATE TABLE Plantilla_formulario (
  Id_plantilla INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- PF001
  Nombre_plantilla VARCHAR(100) NOT NULL,
  Estructura_preguntas JSONB NOT NULL,
  Estado_plantilla BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT pk_plantilla_formulario PRIMARY KEY (Id_plantilla)
);

-- TABLA DE TIPOS DE TICKET
CREATE TABLE Tipos_ticket (
  Id_tipo_ticket INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- TT001
  Nombre_tipo_ticket VARCHAR(100) NOT NULL,
  CONSTRAINT pk_tipos_ticket PRIMARY KEY (Id_tipo_ticket)
);

-- TABLA DE CANALES DE INGRESO
CREATE TABLE Canales (
  Id_canal INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- CN001
  Nombre_canal VARCHAR(100) NOT NULL,
  CONSTRAINT pk_canales PRIMARY KEY (Id_canal)
);

-- TABLA DE ESTADOS DE TICKET
CREATE TABLE Estado_ticket (
  Id_estado INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- ET001
  Nombre_estado VARCHAR(100) NOT NULL,
  CONSTRAINT pk_estado_ticket PRIMARY KEY (Id_estado)
);

-- TABLA DE ROLES DE USUARIOS
CREATE TABLE Roles (
  Id_rol INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- RL001
  Nombre_rol VARCHAR(100) NOT NULL,
  Descripcion VARCHAR(255) NOT NULL,
  CONSTRAINT pk_roles PRIMARY KEY (Id_rol)
);

-- TABLA DE CLIENTES
CREATE TABLE Clientes (
  Id_cliente INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- CL001
  Nombres VARCHAR(100) NOT NULL,
  Apellidos VARCHAR(100) NOT NULL,
  DPI VARCHAR(20) UNIQUE NOT NULL,
  Celular VARCHAR(20) UNIQUE NOT NULL,
  Email VARCHAR(100) UNIQUE NOT NULL,
  CONSTRAINT pk_clientes PRIMARY KEY (Id_cliente)
);

-- ENTIDADES DE SEGUNDO NIVEL

-- DEPENDE DE DEPARTAMENTOS
-- TABLA MUNICIPIOS
CREATE TABLE Municipios (
  Id_municipio INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- MP001
  Nombre_municipio VARCHAR(100) NOT NULL,
  Id_departamento INT NOT NULL,
  CONSTRAINT pk_municipios PRIMARY KEY (Id_municipio),
  CONSTRAINT fk_municipios_departamentos FOREIGN KEY (Id_departamento) REFERENCES Departamentos(Id_departamento)
);

-- DEPENDE DE ROLES
-- TABLA EMPLEADOS
CREATE TABLE Empleados (
  Id_empleado INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- EM001
  Nombre_empleado VARCHAR(100) NOT NULL,
  Email VARCHAR(100) UNIQUE NOT NULL,
  Password_bash VARCHAR(255) NOT NULL,
  Activo BOOLEAN NOT NULL DEFAULT TRUE,
  Id_rol INT NOT NULL,
  CONSTRAINT pk_empleados PRIMARY KEY (Id_empleado),
  CONSTRAINT fk_empleados_roles FOREIGN KEY (Id_rol) REFERENCES Roles(Id_rol)
);

-- ENTIDADES DE TERCER NIVEL
-- TABLA DIRECCIONES
CREATE TABLE Direcciones (
  Id_direccion INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- DR001
  Descripcion VARCHAR(255) NOT NULL,
  Calle VARCHAR(255) NOT NULL,
  Zona VARCHAR(50) NOT NULL,
  Avenida VARCHAR(255),
  Referencia VARCHAR(255),
  Id_cliente INT NOT NULL,
  Id_municipio INT NOT NULL,
  Detalles_direccion VARCHAR(255) NOT NULL,
  CONSTRAINT pk_direcciones PRIMARY KEY (Id_direccion),
  CONSTRAINT fk_direcciones_clientes FOREIGN KEY (Id_cliente) REFERENCES Clientes(Id_cliente),
  CONSTRAINT fk_direcciones_municipios FOREIGN KEY (Id_municipio) REFERENCES Municipios(Id_municipio)
);

-- TABLA CLIENTES SERVICIOS
CREATE TABLE Clientes_servicios (
  Id_cliente_servicio INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- CS001
  Id_cliente INT NOT NULL,
  Id_servicio INT NOT NULL,
  Fecha_adquisicion TIMESTAMP NOT NULL,
  CONSTRAINT pk_clientes_servicios PRIMARY KEY (Id_cliente_servicio),
  CONSTRAINT fk_clientes_servicios_clientes FOREIGN KEY (Id_cliente) REFERENCES Clientes(Id_cliente),
  CONSTRAINT fk_clientes_servicios_servicios FOREIGN KEY (Id_servicio) REFERENCES Servicios(Id_servicio)
);

-- TABLA TICKETS
CREATE TABLE Tickets (
  Id_ticket INT GENERATED ALWAYS AS IDENTITY NOT NULL, -- TK0001
  Codigo_ticket VARCHAR(20) UNIQUE NOT NULL, -- Formato: TK-0001, TK-0002, etc.
  Id_cliente INT NOT NULL,
  Id_receptor INT NOT NULL,
  Id_tecnico INT,
  Id_canal INT NOT NULL,
  Id_estado INT NOT NULL,
  Id_tipo_ticket INT NOT NULL,
  Id_impacto INT NOT NULL,
  Id_plantilla INT NOT NULL,
  Datos_respuesta JSONB NOT NULL,
  Fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Fecha_resolucion TIMESTAMP,
  CONSTRAINT pk_tickets PRIMARY KEY (Id_ticket),
  CONSTRAINT fk_tickets_clientes FOREIGN KEY (Id_cliente) REFERENCES Clientes(Id_cliente),
  CONSTRAINT fk_tickets_receptor FOREIGN KEY (Id_receptor) REFERENCES Empleados(Id_empleado),
  CONSTRAINT fk_tickets_tecnico FOREIGN KEY (Id_tecnico) REFERENCES Empleados(Id_empleado),
  CONSTRAINT fk_tickets_canales FOREIGN KEY (Id_canal) REFERENCES Canales(Id_canal),
  CONSTRAINT fk_tickets_estado FOREIGN KEY (Id_estado) REFERENCES Estado_ticket(Id_estado),
  CONSTRAINT fk_tickets_tipo_ticket FOREIGN KEY (Id_tipo_ticket) REFERENCES Tipos_ticket(Id_tipo_ticket),
  CONSTRAINT fk_tickets_impacto FOREIGN KEY (Id_impacto) REFERENCES Niveles_impacto(Id_impacto),
  CONSTRAINT fk_tickets_plantilla FOREIGN KEY (Id_plantilla) REFERENCES Plantilla_formulario(Id_plantilla)
);


INSERT INTO Departamentos(Nombre_departamento) VALUES
('Guatemala'),
('El Progreso'),
('Sacatepéquez'),
('Chimaltenango'),
('Escuintla'),
('Santa Rosa'),
('Sololá'),
('Totonicapán'),
('Quetzaltenango'),
('Suchitepéquez'),
('Retalhuleu'),
('San Marcos'),
('Huehuetenango'),
('Quiché'),
('Baja Verapaz'),
('Alta Verapaz'),
('Petén'),
('Izabal'),
('Zacapa'),
('Chiquimula'), 
('Jalapa'),
('Jutiapa');

INSERT INTO Servicios(Nombre_servicio) VALUES
('Soporte Técnico'),
('Mantenimiento de Software'),
('Instalación de Hardware'),
('Consultoría IT'),
('Capacitación en Tecnología');

INSERT INTO Niveles_impacto(Nombre_impacto, Peso_impacto) VALUES
('Bajo', 1),
('Medio', 2),
('Alto', 3);

INSERT INTO Plantilla_formulario(Nombre_plantilla, Estructura_preguntas) VALUES
('Plantilla General', '[
  {"pregunta": "¿Cuál es el problema que estás experimentando?", "tipo": "texto"},
  {"pregunta": "¿Cuándo comenzó el problema?", "tipo": "fecha"},
  {"pregunta": "¿Has intentado alguna solución por tu cuenta?", "tipo": "booleano"},
  {"pregunta": "¿Cuál es tu nivel de urgencia?", "tipo": "opciones", "opciones": ["Bajo", "Medio", "Alto"]}
]');
INSERT INTO Tipos_ticket(Nombre_tipo_ticket) VALUES
('Incidente'),
('Solicitud de Servicio'),
('Consulta'),
('Requerimiento de Cambio');

INSERT INTO Canales(Nombre_canal) VALUES
('Correo Electrónico'),
('Teléfono');

INSERT INTO Estado_ticket(Nombre_estado) VALUES
('Abierto'),
('En Proceso'),
('Resuelto'),
('Cerrado');

INSERT INTO Roles(Nombre_rol, Descripcion) VALUES
('Administrador', 'Usuario con acceso completo a todas las funcionalidades del sistema.'),
('Técnico', 'Usuario encargado de resolver los tickets asignados.'),
('Receptor', 'Usuario encargado de recibir y clasificar los tickets.');

INSERT INTO Clientes(Nombres, Apellidos, DPI, Celular, Email) VALUES
('Juan', 'Pérez', '1234567890101', '555-1234', 'juan.perez@example.com'), 
('María', 'Gómez', '1098765432101', '555-5678', 'maria.gomez@example.com'),
('Carlos', 'López', '1122334455667', '555-9012', 'carlos.lopez@example.com');

INSERT INTO Municipios(Nombre_municipio, Id_departamento) VALUES
('Guatemala', 1),
('Mixco', 1),
('Villa Nueva', 1),
('Santa Catarina Pinula', 1),
('San Miguel Petapa', 1);

INSERT INTO Empleados(Nombre_empleado, Id_rol, Email, Password_bash) VALUES
('Ana Martínez', 1, 'ana.martinez@example.com', 'hashed_password_1'), 
('Luis Rodríguez', 2, 'luis.rodriguez@example.com', 'hashed_password_2'), 
('Sofía Hernández', 3, 'sofia.hernandez@example.com', 'hashed_password_3');

INSERT INTO Direcciones(Id_cliente, Descripcion, Id_municipio, Detalles_direccion) VALUES
(1, 'Dirección Principal', 1, 'Zona 1, Calle Principal #123'),
(2, 'Dirección Secundaria', 2, 'Zona 2, Avenida Central #456'),
(3, 'Dirección Terciaria', 3, 'Zona 3, Barrio El Progreso #789');

INSERT INTO Clientes_servicios(Id_cliente, Id_servicio, Fecha_adquisicion) VALUES
(1, 1, '2024-01-15'),
(1, 2, '2024-02-20'),z
(2, 1, '2024-03-10'),
(3, 3, '2024-04-05');

INSERT INTO Tickets(Codigo_ticket, Id_cliente, Id_receptor, Id_tecnico, Id_canal, Id_estado, Id_tipo_ticket, Id_impacto, Id_plantilla, Datos_respuesta) VALUES
('TK-0001', 1, 3, 2, 1, 1, 1, 2, 1, '{
  "¿Cuál es el problema que estás experimentando?": "Mi computadora no enciende.",
  "¿Cuándo comenzó el problema?": "2024-05-01",
  "¿Has intentado alguna solución por tu cuenta?": true,
  "¿Cuál es tu nivel de urgencia?": "Alto"
}'),
('TK-0002', 2, 3, NULL, 2, 1, 2, 1, 1, '{
  "¿Cuál es el problema que estás experimentando?": "Necesito instalar un nuevo software.",
  "¿Cuándo comenzó el problema?": "2024-05-02",
  "¿Has intentado alguna solución por tu cuenta?": false,
  "¿Cuál es tu nivel de urgencia?": "Medio"
}'),
('TK-0003', 3, 3, NULL, 1, 1, 3, 3, 1, '{
  "¿Cuál es el problema que estás experimentando?": "Tengo una consulta sobre mi servicio.",
  "¿Cuándo comenzó el problema?": "2024-05-03",
  "¿Has intentado alguna solución por tu cuenta?": false,
  "¿Cuál es tu nivel de urgencia?": "Bajo"
}');

/*
CONSULTAS

Nivel Básico (Filtros y Búsquedas Simples)

1. El cliente impaciente: Un estudiante llama por teléfono y dice: "Hola, mi DPI es 1234567890101, 
necesito saber qué código de ticket me asignaron la semana pasada para mi reporte". ¿Cómo buscas 
el Codigo_ticket y la Fecha_creacion filtrando únicamente por el DPI de ese cliente?

2. Tickets en el limbo: El coordinador de soporte te pide un listado urgente de todos los tickets 
(mostrando el Codigo_ticket) que actualmente están "Abiertos" (asumiendo que conoces el ID o nombre de ese estado), 
pero que aún no tienen un técnico asignado (Id_tecnico está vacío).

Nivel Intermedio (Uso de JOINs y Relaciones)
3. El historial del cliente (N:M): Auditoría te pide el expediente de un cliente específico. Necesitan que 
muestres los Nombres y Apellidos del cliente junto con el nombre de todos los servicios que tiene contratados
actualmente (Aquí entra en juego tu tabla pivote Clientes_servicios).

4. Desglose de direcciones: Un técnico necesita ir a la casa de un estudiante para revisar un equipo. Tienes 
el Codigo_ticket (ej. 'TK-0150'). Construye una consulta que devuelva los Detalles_direccion completos, incluyendo 
el nombre del Municipio y el nombre del Departamento de ese cliente en específico.

5. Carga laboral (Agrupaciones): Recursos Humanos quiere saber cuántos tickets tiene asignados cada técnico. Crea 
un reporte que muestre el nombre de cada empleado y al lado el total (conteo) de tickets que tiene a su cargo.

6. Los empleados inactivos (LEFT JOIN): Necesitamos una lista de todos los técnicos (Empleados) que en este momento
no tienen asignado absolutamente ningún ticket.

Nivel Avanzado (Fechas, JSONB y Múltiples Tablas)

7. Tiempos de resolución: Gerencia necesita medir la eficiencia. Quieren un listado de los tickets que ya fueron 
resueltos, mostrando el Codigo_ticket, el nombre del técnico que lo resolvió, y calculando cuántos días (o horas)
 pasaron entre la Fecha_creacion y la Fecha_resolucion.

8. Búsqueda dinámica en JSONB: Tienes un formulario dinámico guardado en la columna Datos_respuesta de la tabla de
tickets. Necesitas encontrar todos los tickets donde, dentro de ese JSON, la llave "¿Cuál es tu nivel de urgencia?" sea exactamente 
igual al valor "Alto". (Tip: Investiga los operadores ->> de PostgreSQL).

9. El reporte completo de fin de mes: Crea una "vista" general. Un reporte que devuelva: Codigo_ticket, Nombre 
completo del Cliente, Nombre del Servicio asociado al problema (si aplica), Nombre del Canal por el que ingresó, 
Nombre del Estado actual, y Nombre del Técnico asignado.

10. Filtrado post-agrupación (HAVING): El director quiere saber qué Municipios nos están generando más reportes 
de fallas. Haz una consulta que cuente cuántos tickets provienen de cada municipio, pero que solo muestre aquellos 
municipios que tengan más de 50 tickets registrados.

*/

--Consulta 1
SELECT clientes.id_cliente, clientes.dpi, tickets.codigo_ticket, tickets.fecha_creacion
FROM clientes
INNER JOIN tickets
ON clientes.id_cliente = tickets.id_cliente
WHERE clientes.dpi = '1234567890101';


--Consulta 2
SELECT  tickets.id_ticket, tickets.codigo_ticket, tickets.id_tecnico, tickets.id_estado
FROM tickets
INNER JOIN estado_ticket
ON tickets.id_estado = estado_ticket.id_estado
WHERE tickets.id_estado = 1 AND tickets.id_tecnico IS NULL;

--Consulta 2 uso de alias
SELECT a.id_ticket, 
		a.codigo_ticket, 
		a.id_tecnico, 
		a.id_estado 
FROM tickets a
INNER JOIN estado_ticket b ON a.id_estado = b.id_estado
WHERE a.id_estado = 1 AND a.id_tecnico IS NULL;

--Consulta 3
SELECT a.id_cliente, a.nombres, s.id_servicio, s.nombre_servicio
FROM clientes a
INNER JOIN clientes_servicios cs ON a.id_cliente = cs.id_cliente
INNER JOIN servicios s ON cs.id_servicio = s.id_servicio
WHERE 
	a.id_cliente = 1;

--Consulta 4
SELECT 
a.nombres, 
a.apellidos, 
b.detalles_direccion, 
c.nombre_municipio, 
d.nombre_departamento
FROM clientes a 
INNER JOIN direcciones b ON a.id_cliente = b.id_cliente
INNER JOIN municipios c ON b.id_municipio = c.id_municipio
INNER JOIN departamentos d ON c.id_departamento = d.id_departamento
INNER JOIN tickets t ON a.id_cliente = t.id_cliente
WHERE
	t.codigo_ticket = 'TK-0001';

--Consulta 5
SELECT 
    e.nombre_empleado, 
    COUNT(t.id_ticket) AS total_tickets
FROM empleados e
INNER JOIN tickets t ON e.id_empleado = t.id_tecnico
GROUP BY e.nombre_empleado;

--Consulta 6 
SELECT 
    e.Id_empleado,
    e.Nombre_empleado,
    r.Nombre_rol
FROM 
    Empleados e
INNER JOIN 
    Roles r ON e.Id_rol = r.Id_rol
LEFT JOIN 
    Tickets t ON e.Id_empleado = t.Id_tecnico
WHERE 
    t.Id_ticket IS NULL
    AND r.Nombre_rol = 'Técnico'; -- Filtramos para que no salgan administrativos

--Consulta 7
SELECT 
    t.codigo_ticket,
    e.nombre_empleado AS Tecnico_asignado,
    t.Fecha_creacion,
    t.Fecha_resolucion,
    -- AGE() devuelve un formato legible como "2 days 04:00:00"
    AGE(t.Fecha_resolucion, t.Fecha_creacion) AS Tiempo_invertido
FROM 
    tickets t
INNER JOIN 
    Empleados e ON t.Id_tecnico = e.Id_empleado
WHERE 
    t.Fecha_resolucion IS NOT NULL;

--Consulta 8
SELECT * FROM tickets;

SELECT 
    Codigo_ticket,
    Id_cliente,
    Datos_respuesta
FROM 
    Tickets
WHERE 
    -- El operador ->> entra al JSON y saca el valor de "tipo_falla" como texto
    Datos_respuesta ->> '¿Cuál es tu nivel de urgencia?' = 'Alto';

--Consulta 9
SELECT 
    t.Codigo_ticket,
    c.Nombres || ' ' || c.Apellidos AS Nombre_Cliente,
    cn.Nombre_canal AS Ingreso,
    es.Nombre_estado AS Estado,
    e.Nombre_empleado AS Tecnico,
    -- Agrupamos todos los servicios del cliente separados por coma
    STRING_AGG(s.Nombre_servicio, ', ') AS Servicios_Contratados
FROM 
    Tickets t
INNER JOIN Clientes c ON t.Id_cliente = c.Id_cliente
INNER JOIN Canales cn ON t.Id_canal = cn.Id_canal
INNER JOIN Estado_ticket es ON t.Id_estado = es.Id_estado
-- Usamos LEFT JOIN por si el ticket aún no tiene técnico
LEFT JOIN Empleados e ON t.Id_tecnico = e.Id_empleado
-- Cruzamos hacia los servicios usando la tabla intermedia
LEFT JOIN Clientes_servicios cs ON c.Id_cliente = cs.Id_cliente
LEFT JOIN Servicios s ON cs.Id_servicio = s.Id_servicio
GROUP BY 
    t.Codigo_ticket, c.Nombres, c.Apellidos, cn.Nombre_canal, es.Nombre_estado, e.Nombre_empleado;

--Consulta 10
SELECT 
    m.Nombre_municipio,
    COUNT(t.Id_ticket) AS Total_Tickets
FROM 
    Tickets t
INNER JOIN Clientes c ON t.Id_cliente = c.Id_cliente
INNER JOIN Direcciones d ON c.Id_cliente = d.Id_cliente
INNER JOIN Municipios m ON d.Id_municipio = m.Id_municipio
GROUP BY 
    m.Nombre_municipio
HAVING 
    COUNT(t.Id_ticket) > 0
ORDER BY 
    Total_Tickets DESC; -- Los ordenamos del mayor al menor