# 🗺️ Roadmap para completar el Backend — `project_final`

> Última actualización: 30/jun/2026 — Corrección de inconsistencias en Repositories + Services

---

## 🧠 Conceptos clave (glosario rápido)

| Capa | Carpeta | Responsabilidad | Herramienta |
|------|---------|----------------|-------------|
| **Models** | `app/models/` | Estructura de las tablas en la BD (columnas, FK, relaciones) | SQLAlchemy ORM |
| **Schemas / DTOs** | `app/schemas/` | Forma de los datos que entran/salen por la API (validación y serialización) | Pydantic v2 |
| **Repositories** | `app/repositories/` | Operaciones CRUD directas contra la BD (INSERT, SELECT, UPDATE, DELETE) | SQLAlchemy Session |
| **Services** | `app/services/` | Lógica de negocio: orquestación, reglas, transformación DTO ↔ Model | Python puro |
| **Routers** | `app/api/routers/` | Endpoints HTTP: reciben petición, delegan al service, responden | FastAPI |

### Flujo de datos
```
Cliente → Router → Service → Repository → Base de datos
           ↑         ↑           ↑
        HTTP      Reglas      SQL
       (FastAPI)  negocio    (SQLAlchemy)
```

### Regla de oro
```
Router -> Service -> Repository -> BD
HTTP      NEGOCIO    PERSISTENCIA   SQL

EL SERVICE NUNCA TOCA: db.commit(), db.add(), db.refresh(), db.delete()
ESO ES TERRITORIO EXCLUSIVO DEL REPOSITORY
El Service construye un dict y se lo pasa al Repository
El Repository NUNCA recibe DTOs — solo dicts o entidades ORM
```

---

## 📋 Resumen de estado actual

| Capa | Estado |
|---|---|
| Modelos (SQLAlchemy) | ✅ 13/13 completos |
| Schemas/DTOs (Pydantic) | ✅ Completos |
| Repositories | ⚠️ 14 archivos existen — algunos con bugs (update con vars()/DTOs, falta delete) |
| Services | ⚠️ Solo 2/14 implementados: `ticket_service` + `canal_service` |
| Routers (FastAPI) | ⚠️ Solo 1/14 implementado: `ticket_router` |
| `main.py` | ⚠️ Solo registra `ticket_router` |
| Auth (JWT) | ❌ Sin implementar |
| `.env` | ✅ Existe — requiere revisar `DB_PASSWORD` |
| Exception handlers | ❌ Sin implementar |
| GraphQL | ❌ Carpeta vacía |
| Tests | ❌ Sin tests |

---

## 🔧 Correcciones 30/jun/2026 — Estandarización update() en Repositories

### Problema detectado
Varios repositorios usaban `vars(entidad)` en sus métodos `update()`, lo que iteraba sobre
atributos internos de SQLAlchemy como `_sa_instance_state` (bug silencioso).
Otro repositorio (`estado_ticket_repository`) recibía un DTO directamente, rompiendo
la regla de que el Repository no debe conocer Schemas.

### Cambios realizados:

| Archivo | Qué se corrigió |
|---------|----------------|
| `canales.py` | Agregado `from __future__ import annotations` para forward references |
| `canal_repository.py` | `update_canal()`: ahora recibe `dict` en vez de entidad `Canal` (eliminado `vars()`) |
| `canal_service.py` | `update_canal()`: ahora hace `model_dump(exclude_unset=True)` y pasa `dict` al repo |
| `ticket_service.py` | Eliminado comentario residual `# fixed`; agregado docstring a `delete_ticket()` |
| `cliente_repository.py` | `update_cliente()`: ahora recibe `dict` en vez de entidad `Cliente` (estandarizado) |

### Repositorios que AÚN necesitan esta misma corrección:

| Archivo | Problema | Falta |
|---------|----------|-------|
| `rol_repository.py` | `update_rol()` usa `vars()` | Migrar a `dict`, agregar `delete_rol()` |
| `departamento_repository.py` | `update_departamento()` usa `vars()` | Migrar a `dict`, agregar `delete_departamento()` |
| `estado_ticket_repository.py` | `update_estado_ticket()` recibe un DTO | Migrar a `dict` |
| `empleado_repository.py` | Faltan métodos `update` y `delete` | Agregar `update_empleado(dict)` y `delete_empleado()` |
| `municipio_repository.py` | No revisado | Revisar y estandarizar |
| `servicio_repository.py` | No revisado | Revisar y estandarizar |
| `direccio_repository.py` | No revisado | Revisar y estandarizar |
| `nivel_impacto_repository.py` | No revisado | Revisar y estandarizar |
| `plantilla_formulario.repository.py` | No revisado | Revisar y estandarizar |
| `tipo_ticket_repository.py` | No revisado | Revisar y estandarizar |
| `cliente_servicio_repository.py` | No revisado | Revisar y estandarizar |

---

## 🧱 Fase 1 — Arreglar lo que impide arrancar

### 1.1 Revisar archivo `.env`
- [x] Archivo `.env` creado
- [ ] Verificar que `DB_PASSWORD` tenga la contraseña correcta de PostgreSQL
- [ ] Verificar que `DB_NAME` coincida con la BD existente

### 1.2 Verificar que la app arranca
- [ ] Ejecutar `uvicorn app.main:app --reload`
- [ ] Confirmar que imprime `"Conexión correcta a la base de datos"` en consola
- [ ] Abrir `http://localhost:8000/docs` y confirmar que Swagger carga

---

## 🧩 Fase 2 — Corregir y completar Repositories

### 2.1 Estandarizar `update()` a `dict` + agregar `delete()` faltantes

- [ ] `app/repositories/rol_repository.py` — Migrar `update` a dict + agregar `delete`
- [ ] `app/repositories/departamento_repository.py` — Migrar `update` a dict + agregar `delete`
- [ ] `app/repositories/estado_ticket_repository.py` — Migrar `update` de DTO a dict
- [ ] `app/repositories/empleado_repository.py` — Agregar `update` (dict) + `delete`

### 2.2 Revisar y estandarizar repositorios no auditados

- [ ] `app/repositories/municipio_repository.py`
- [ ] `app/repositories/servicio_repository.py`
- [ ] `app/repositories/direccio_repository.py`
- [ ] `app/repositories/nivel_impacto_repository.py`
- [ ] `app/repositories/plantilla_formulario.repository.py`
- [ ] `app/repositories/tipo_ticket_repository.py`
- [ ] `app/repositories/cliente_servicio_repository.py`

> **Patrón de referencia:** `app/repositories/ticket_repository.py`

---

## 🧠 Fase 3 — Implementar Services

**Objetivo:** Crear 12 services nuevos. Cada uno sigue el patrón canónico de `canal_service.py`.

### 3.1 Services de catálogos (CRUD simple)

- [ ] `app/services/estado_ticket_service.py`
- [ ] `app/services/tipo_ticket_service.py`
- [ ] `app/services/nivel_impacto_service.py`
- [ ] `app/services/plantilla_service.py`
- [ ] `app/services/servicio_service.py`
- [ ] `app/services/rol_service.py`
- [ ] `app/services/departamento_service.py`
- [ ] `app/services/municipio_service.py`

### 3.2 Services de entidades principales

- [ ] `app/services/cliente_service.py`
- [ ] `app/services/empleado_service.py`
- [ ] `app/services/direccion_service.py`
- [ ] `app/services/cliente_servicio_service.py`

### 3.3 Services ya implementados

- [x] `app/services/ticket_service.py` — Completo (refactorizado 27/jun, corregido 30/jun)
- [x] `app/services/canal_service.py` — Completo (corregido 30/jun)

> **Patrón de referencia:** `app/services/canal_service.py`

---

## 🌐 Fase 4 — Crear Routers REST

Cada router recibe la petición HTTP, llama al service y devuelve la respuesta.
**Nunca contiene lógica de negocio ni acceso directo a BD.**

### 4.1 Routers de catálogos

- [ ] `app/api/routers/canal_router.py`
- [ ] `app/api/routers/estado_ticket_router.py`
- [ ] `app/api/routers/tipo_ticket_router.py`
- [ ] `app/api/routers/nivel_impacto_router.py`
- [ ] `app/api/routers/plantilla_router.py`
- [ ] `app/api/routers/servicio_router.py`
- [ ] `app/api/routers/rol_router.py`
- [ ] `app/api/routers/departamento_router.py`
- [ ] `app/api/routers/municipio_router.py`

### 4.2 Routers de entidades principales

- [ ] `app/api/routers/cliente_router.py`
- [ ] `app/api/routers/empleado_router.py`
- [ ] `app/api/routers/direccion_router.py`

### 4.3 Router ya implementado

- [x] `app/api/routers/ticket_router.py` — Completo (refactorizado 27/jun)

### 4.4 Registrar todos los routers en `main.py`

- [ ] Importar y registrar cada router con `app.include_router()`

> **Patrón de referencia:** `app/api/routers/ticket_router.py`

---

## 🔐 Fase 5 — Autenticación JWT

### 5.1 Crear utilidades de seguridad
- [ ] `app/core/security.py`:
  - `hash_password(password: str) -> str` (bcrypt / passlib)
  - `verify_password(plain: str, hashed: str) -> bool`
  - `create_access_token(data: dict) -> str` (python-jose)
  - `decode_access_token(token: str) -> dict`

### 5.2 Crear dependencia de auth
- [ ] `app/api/dependencies.py`:
  - `get_current_user(token: str = Depends(oauth2_scheme)) -> Empleado`
  - Lanzar `HTTPException 401` si el token no es válido

### 5.3 Crear router de autenticación
- [ ] `app/api/routers/auth_router.py`:
  - `POST /auth/login` → recibe credenciales, devuelve JWT
  - `GET /auth/me` → devuelve info del usuario autenticado

### 5.4 Proteger endpoints
- [ ] Agregar `Depends(get_current_user)` a endpoints que requieran autenticación

---

## 🛡️ Fase 6 — Manejo de errores global

- [ ] Handler para `IntegrityError` → 409 Conflict
- [ ] Handler genérico `Exception` → 500 (sin leak de detalles internos)
- [ ] Handler personalizado para errores de negocio (opcional)

---

## 📄 Fase 7 — Paginación genérica

- [ ] `app/schemas/common.py` → `PaginatedResponse[T]` con `items`, `total`, `skip`, `limit`
- [ ] Usarlo en todos los endpoints GET de lista

---

## 🗃️ Fase 8 — Base de datos (migraciones + seed)

### 8.1 Migraciones con Alembic
- [ ] Instalar `alembic` e inicializar
- [ ] Configurar `alembic/env.py` para usar `Base.metadata`
- [ ] Generar migración inicial y aplicar

### 8.2 Datos semilla (seed)
- [ ] `app/db/seed.py` — insertar datos iniciales (roles, estados, canales, niveles, tipos, admin)
- [ ] Ejecutar con: `python -m app.db.seed`

---

## 🧪 Fase 9 — Tests

- [ ] Instalar `pytest`, `httpx`
- [ ] Crear `tests/conftest.py` con `TestClient` + BD de prueba
- [ ] Tests mínimos: tickets, clientes, auth

---

## 🧠 Fase 10 — GraphQL (opcional)

- [ ] Implementar con Strawberry
- [ ] Montar en FastAPI con `GraphQLRouter`

---

## 📦 Fase 11 — Docker + despliegue

- [ ] Crear `Dockerfile`
- [ ] Crear `docker-compose.yml` (app + postgres)

---

## ✅ Orden de ejecución recomendado (ACTUALIZADO)

1. [ ] Revisar `.env` y verificar que arranca (Fase 1)
2. [ ] **PRIORITARIO:** Corregir los 4 repos con bugs conocidos (Fase 2.1)
3. [ ] Revisar y estandarizar los 7 repos no auditados (Fase 2.2)
4. [ ] Implementar todos los services (Fase 3)
5. [ ] Crear todos los routers + registrar en `main.py` (Fase 4)
6. [ ] Implementar autenticación JWT (Fase 5)
7. [ ] Exception handlers (Fase 6)
8. [ ] Paginación genérica (Fase 7)
9. [ ] Alembic + seed (Fase 8)
10. [ ] Tests (Fase 9)
11. [ ] GraphQL (opcional — Fase 10)
12. [ ] Docker (Fase 11)