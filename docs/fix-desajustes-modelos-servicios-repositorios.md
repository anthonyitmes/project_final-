# Corrección de desajustes entre modelos, servicios, repositorios y routers

**Fecha:** 2026-07-20  
**Autor:** Anthony Sub  
**Rama:** `fix/desajustes-modelos-servicios`

---

## 1. Problema detectado

Al levantar la API con `uvicorn app.main:app`, múltiples endpoints fallaban con errores como:

- `AttributeError: 'RolService' object has no attribute 'get_all_roles'`
- `sqlalchemy.exc.ProgrammingError: column roles.descripcion_rol does not exist`
- `AttributeError: 'EstadoTicketRepository' object has no attribute 'get_list_estado_tickets'`

Estos errores evidenciaban **tres tipos de desajustes** entre las capas de la aplicación:

1. **Routers** llamando métodos del servicio con nombres incorrectos (`get_all_*` vs `get_list_*`)
2. **Modelos SQLAlchemy** con columnas que no existen en la base de datos, o con nombres distintos
3. **Servicios** llamando métodos de repositorios con nombres incorrectos o pasando parámetros en formato equivocado (entidades en vez de diccionarios)

---

## 2. Diagnóstico

### 2.1. Causa raíz

El proyecto fue generado parcialmente con herramientas automáticas y/o copiado desde plantillas (copy-paste de un módulo a otro), lo que provocó que:

- Los routers tuvieran una convención de nombres (`get_all_*`) heredada de un módulo plantilla, mientras que los servicios implementaban otra (`get_list_*`)
- Algunos modelos definían columnas con nombres distintos a los que realmente existen en la tabla PostgreSQL
- El modelo `Ticket` incluía columnas `titulo` y `descripcion` que no existen en la tabla `Tickets`
- Los servicios de algunas entidades pasaban objetos entidad a los repositorios, en lugar de diccionarios `{campo: valor}`, lo que causaba que se iterara sobre atributos internos de SQLAlchemy como `_sa_instance_state`

### 2.2. Metodología de diagnóstico

1. Se capturó el traceback del error `AttributeError` en `rol_router.py`
2. Se comparó el método llamado en el router (`get_all_roles`) contra los métodos reales del servicio (`get_list_roles`)
3. Se hizo una búsqueda masiva con regex `get_all_*` en todos los routers y `def get_(all|list)_*` en todos los servicios para encontrar el patrón completo
4. Se compararon los modelos SQLAlchemy contra el script `proyecto.sql` para detectar columnas inexistentes o con nombres incorrectos
5. Se revisó la firma de cada método en repositorios y servicios para asegurar consistencia en parámetros (dict vs entidad, id vs objeto)

---

## 3. Cambios realizados

### 3.1. Routers: métodos `get_all_*` → `get_list_*`

| Archivo | Línea | Antes | Después |
|---|---|---|---|
| `app/api/routers/rol_router.py` | 37 | `rol_services.get_all_roles(db)` | `rol_services.get_list_roles(db)` |
| `app/api/routers/cliente_servicio_router.py` | 46 | `cliente_servicio_services.get_all_cliente_servicios(db)` | `cliente_servicio_services.get_list_clientes_servicios(db)` |
| `app/api/routers/empleado_router.py` | 46 | `empleado_services.get_all_empleados(db)` | `empleado_services.get_list_empleados(db)` |
| `app/api/routers/estado_ticket_router.py` | 39 | `estado_ticket_services.get_all_estados_ticket(db)` | `estado_ticket_services.get_list_estado_tickets(db)` |
| `app/api/routers/municipio_router.py` | 45 | `municipio_services.get_all_municipios(db)` | `municipio_services.get_list_municipios(db)` |
| `app/api/routers/nivel_impacto_router.py` | 38 | `nivel_impacto_service.get_all_niveles_impacto(db)` | `nivel_impacto_service.get_list_niveles_impacto(db)` |

**Routers que ya estaban correctos** (no requirieron cambios):
- `canal_router.py` → el servicio sí tiene `get_all_canales()`
- `cliente_router.py` → ya llamaba `get_list_clientes()`
- `departamento_router.py` → ya llamaba `get_list_departamentos()`
- `direccion_router.py` → ya llamaba `get_list_direcciones()`
- `servicio_router.py` → el servicio sí tiene `get_all_servicios()`
- `tipo_ticket_router.py` → el servicio sí tiene `get_all_tipos_ticket()`
- `ticket_router.py` → el servicio sí tiene `get_all_tickets()`
- `plantilla_formulario_router.py` → el servicio sí tiene `get_all_plantillas()`

### 3.2. Modelos: columnas corregidas

#### 3.2.1. `app/models/roles.py`

| Concepto | Antes | Después | Motivo |
|---|---|---|---|
| Columna | `descripcion_rol` | `descripcion` | La tabla `Roles` en PostgreSQL tiene la columna `Descripcion` (sin sufijo `_rol`) |
| Nullable | `nullable=True` | `nullable=False` | La columna en BD es `NOT NULL` |

#### 3.2.2. `app/models/tickets.py`

| Concepto | Antes | Después | Motivo |
|---|---|---|---|
| Columna `titulo` | `Mapped[str]` | **Eliminada** | La tabla `Tickets` no tiene columna `titulo` |
| Columna `descripcion` | `Mapped[str]` | **Eliminada** | La tabla `Tickets` no tiene columna `descripcion` |

### 3.3. DTOs corregidos

#### 3.3.1. `app/schemas/rol_dto.py`

Se renombró el campo `descripcion_rol` → `descripcion` en los tres DTOs:
- `RolCreateDTO`
- `RolResponseDTO`
- `RolUpdateDTO`

#### 3.3.2. `app/schemas/ticket_dto.py`

Se eliminaron los campos `titulo` y `descripcion` de:
- `TicketCreateDTO`
- `TicketUpdateDTO`
- `TicketResponseDTO`

### 3.4. Servicios: parámetros y métodos corregidos

#### 3.4.1. `app/services/estado_ticket_service.py`

| Método | Cambio |
|---|---|
| `create_estado_ticket()` | `nombre_estado_ticket` → `nombre_estado` (coincide con el DTO y modelo) |
| `get_list_estado_tickets()` | Llama a `get_list_estados_ticket()` (con 's') en el repositorio |
| `update_estado_ticket()` | Ahora pasa `dict` (con `model_dump`) en vez de entidad; llama a `update_estado_ticket(db, id, datos)` en vez de `update_estado_ticket(db, entidad)` |
| `delete_estado_ticket()` | Llama a `delete_estado_ticket(db, id)` en vez de `delete_estado_ticket(db, entidad)` |

#### 3.4.2. `app/services/empleado_service.py`

| Método | Cambio |
|---|---|
| `create_empleado()` | Agregados todos los campos requeridos: `email`, `password_bash`, `activo`, `id_rol` (antes solo pasaba `nombre_empleado`) |
| `update_empleado()` | Ahora usa `dict` y llama a `update_empleado(db, id, datos)` en vez de modificar la entidad directamente con `setattr` + `db.commit()` |
| `delete_empleado()` | Llama a `delete_empleado(db, id)` en vez de `delete_empleado(db, entidad)` |

#### 3.4.3. `app/services/municipio_service.py`

| Método | Cambio |
|---|---|
| `update_municipio()` | Ahora pasa `dict` al repo en vez de la entidad; llama a `update_municipio(db, id, datos)` |
| `delete_municipio()` | Llama a `delete_municipio(db, id)` en vez de `delete_municipio(db, entidad)` |

#### 3.4.4. `app/services/cliente_servicio_service.py`

| Método | Cambio |
|---|---|
| `update_cliente_servicio()` | Ahora pasa `dict` al repo; llama a `update_cliente_servicio(db, id, datos)` en vez de `update_cliente_servicio(db, entidad)` |
| `delete_cliente_servicio()` | Llama a `delete_cliente_servicio(db, id)` en vez de `delete_cliente_servicio(db, entidad)` |

#### 3.4.5. `app/services/rol_service.py`

| Método | Cambio |
|---|---|
| `update_rol()` | **Crítico:** antes iteraba con `setattr` sobre la entidad pero **nunca llamaba a `db.commit()`**, por lo que los cambios no se persistían. Ahora pasa `dict` al repositorio que sí hace commit |
| `delete_rol()` | Simplificado: llama directamente a `delete_rol(db, id)` sin pre-verificar existencia (el repo ya lo hace) |

#### 3.4.6. `app/services/ticket_service.py`

| Método | Cambio |
|---|---|
| `_build_ticket_entity()` | Eliminadas las líneas `titulo=ticket_in.titulo` y `descripcion=ticket_in.descripcion` |

### 3.5. Repositorio corregido

#### 3.5.1. `app/repositories/cliente_servicio_repository.py`

| Método | Antes | Después |
|---|---|---|
| Listar todos | `get_list_cliente_servicios()` | `get_list_clientes_servicios()` |

El nombre del método no coincidía con el que el servicio intentaba llamar.

---

## 4. Verificación

### 4.1. Importación del módulo principal

```bash
python -c "from app.main import app; print('OK')"
# Salida: OK
```

### 4.2. Endpoints probados exitosamente

```bash
curl http://localhost:8000/           # → {"message":"API project_final funcionando"}
curl http://localhost:8000/roles      # → []
curl http://localhost:8000/estados-ticket  # → []
```

---

## 5. Lecciones aprendidas

1. **Convención de nombres uniforme:** Todos los servicios deben seguir la misma convención. Se recomienda estandarizar en `get_list_*` ya que la mayoría de servicios y repositorios ya usan ese prefijo.

2. **No hacer copy-paste sin revisar:** Al copiar un router/servicio de un módulo a otro, verificar que los nombres de métodos existen realmente en la capa inferior.

3. **Los modelos deben reflejar fielmente la BD:** Cualquier columna en el modelo que no exista en PostgreSQL causará un `ProgrammingError` al hacer queries.

4. **Separación de responsabilidades:** El servicio NO debe hacer `db.commit()` directamente. Debe delegar en el repositorio, pasando datos crudos (`dict`) en lugar de entidades SQLAlchemy.

5. **Pruebas de integración tempranas:** Un simple `curl` a cada endpoint después de generar el código habría detectado estos errores inmediatamente.

---

## 6. Impacto en otros módulos

- **GraphQL:** No fue necesario modificar la capa GraphQL porque usa los mismos servicios ya corregidos.
- **Auth:** El módulo de autenticación (`auth_router.py`, `security.py`, `dependencies.py`) no requirió cambios.
- **Base de datos:** No se modificó el esquema SQL. Todos los cambios fueron en la capa de aplicación para alinearse con la BD existente.

---

## 7. Commits relacionados

```bash
git add app/api/routers/rol_router.py \
        app/api/routers/cliente_servicio_router.py \
        app/api/routers/empleado_router.py \
        app/api/routers/estado_ticket_router.py \
        app/api/routers/municipio_router.py \
        app/api/routers/nivel_impacto_router.py \
        app/models/roles.py \
        app/models/tickets.py \
        app/schemas/rol_dto.py \
        app/schemas/ticket_dto.py \
        app/services/estado_ticket_service.py \
        app/services/empleado_service.py \
        app/services/municipio_service.py \
        app/services/cliente_servicio_service.py \
        app/services/rol_service.py \
        app/services/ticket_service.py \
        app/repositories/cliente_servicio_repository.py \
        docs/fix-desajustes-modelos-servicios-repositorios.md

git commit -m "fix: corregir desajustes entre modelos, servicios, repositorios y routers

- Routers: get_all_* -> get_list_* (6 archivos)
- Modelo Rol: descripcion_rol -> descripcion
- Modelo Ticket: eliminar columnas titulo y descripcion inexistentes
- DTOs: actualizar Rol y Ticket
- Servicios: corregir parámetros (dict vs entidad), métodos faltantes
- Repositorio: renombrar get_list_cliente_servicios -> get_list_clientes_servicios

Closes #fix/desajustes-modelos-servicios"