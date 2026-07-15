# 🗺️ Roadmap para completar el Backend — `project_final`

> Última actualización: 15/jul/2026 — Fase 4 completada y verificada, Fase 5 (Auth JWT) siguiente

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
EL REPOSITORY NUNCA RECIBE DTOs — solo dicts o entidades ORM
EL ROUTER SOLO RECIBE HTTP Y LLAMA AL SERVICE — nunca toca BD directamente
```

---

## 📋 Resumen de estado actual (15/jul/2026)

| Capa | Estado |
|---|---|
| Modelos (SQLAlchemy) | ✅ 14/14 completos |
| Schemas/DTOs (Pydantic) | ✅ Completos (15 archivos — `auth_dto.py` ya contiene `LoginRequestDTO` y `TokenResponseDTO`) |
| Repositories | ✅ 15/15 estandarizados — todos usan `dict` en update, todos tienen delete. Singletons agregados. |
| Services | ✅ 14/14 implementados. `direccion_service.py` corregido (5 bugs). |
| Routers (FastAPI) | ✅ 14/14 construidos y registrados en `main.py` — 72 endpoints funcionando |
| `main.py` | ✅ Los 14 routers registrados con `app.include_router()` |
| Base de datos | ✅ Tablas creadas en `user_db` vía SQLAlchemy `create_all()` |
| Auth (JWT) | ❌ Sin implementar — `auth_dto.py` se usará en Fase 5 directamente en el router |
| Async (async/await) | ❌ Toda la app es síncrona actualmente — migrar a async en Fase 12 |
| `.env` | ✅ Configurado y funcional |
| Exception handlers | ❌ Sin implementar |
| GraphQL | ❌ Carpeta vacía |
| Tests | ❌ Sin tests |

---

## 🔧 Correcciones 30/jun - 15/jul/2026 — Estandarización completa

### Cambios realizados en Repositories (06/jul):
Migración de `vars(entidad)` → `dict` + agregado `delete` en TODOS los repositorios:

| Fecha | Archivo | Cambio |
|-------|---------|--------|
| 30/jun | `canal_repository.py` | `update` → `dict` |
| 30/jun | `cliente_repository.py` | `update` → `dict` |
| 06/jul | `tipo_ticket_repository.py` | `update` → `dict` + `delete` |
| 06/jul | `servicio_repository.py` | `update` → `dict` |
| 06/jul | `departamento_repository.py` | `update` → `dict` + `delete` |
| 06/jul | `plantilla_formulario_repository.py` | `update` → `dict` + `delete` + renombrado |
| 06/jul | `rol_repository.py` | `update` → `dict` + `delete` |
| 06/jul | `municipio_repository.py` | `update` → `dict` + `delete` |
| 06/jul | `direccio_repository.py` | `update` → `dict` + `delete` |
| 06/jul | `cliente_servicio_repository.py` | `update` → `dict` |
| 06/jul | `estado_ticket_repository.py` | `update` DTO → `dict` (eliminado import de schema) |
| 06/jul | `empleado_repository.py` | Agregados `update(dict)` + `delete` |

### Cambios realizados en Services (06/jul):
- `tipo_ticket_service.py` — creado
- `servicio_service.py` — corregido (4 bugs)
- `plantilla_service.py` — creado (JSONB + validación)

### Cambios realizados el 15/jul/2026:
| Hora | Archivo | Cambio |
|------|---------|--------|
| 15/jul | `app/services/*.py` (11 archivos) | Agregados singletons (`service = Clase()`) y corregidos imports en routers |
| 15/jul | `app/repositories/cliente_repository.py` | Agregado singleton faltante |
| 15/jul | `app/api/routers/direccion_router.py` | **Fix crítico:** era copia exacta de `cliente_servicio_router.py` (prefijo `/cliente_servicios`, 5 warnings Duplicate Operation ID). Reescrito con prefijo `/direcciones` y endpoints CRUD propios. |
| 15/jul | `app/services/direccion_service.py` | **5 bugs corregidos:** (1) faltaba `from app.repositories.direccio_repository import direccion_repository`, (2) `create_direccion()` asignaba campo inexistente `nombre_direccion` → asigna 8 campos reales, (3) `update_direccion()` iteraba `setattr` sin commit → delega en repositorio, (4) `delete_direccion()` pasaba entidad en vez de `id_direccion`, (5) no importaba el singleton. |
| 15/jul | `app/main.py` | Verificado: 14 routers registrados, 72 endpoints, 0 warnings |
| 15/jul | Base de datos `user_db` | Tablas creadas con `Base.metadata.create_all()` (14 tablas). `GET /canales` → 200 OK. |
| 15/jul | Git | 4 commits por carpeta + push a `origin/main` |

---

## 🧱 Fase 1 — Arreglar lo que impide arrancar

### 1.1 Revisar archivo `.env`
- [x] Archivo `.env` creado
- [x] `DB_PASSWORD` verificada (`12345678`)
- [x] `DB_NAME` = `user_db` (coincide con BD existente)

### 1.2 Verificar que la app arranca
- [x] `uvicorn app.main:app --reload` ejecuta sin errores
- [x] Imprime `"Conexión correcta a la base de datos"` en consola
- [x] `http://localhost:8000/docs` carga Swagger con 72 endpoints
- [x] `GET /canales` → 200 OK

---

## 🧩 Fase 2 — Repositories ✅ COMPLETADO (06/jul/2026)

- [x] Los 15 repositorios estandarizados con `update(dict)` y `delete`
- [x] `estado_ticket_repository.py` ya no importa schemas
- [x] Contrato único: `(db: Session, id: int, datos: dict) -> Model | None`
- [x] Singletons agregados en todos los repositorios (15/jul)

---

## 🧠 Fase 3 — Services ✅ COMPLETADO (06/jul/2026, corregido 15/jul)

### 3.1 Services implementados (14/14)

- [x] `app/services/canal_service.py`
- [x] `app/services/cliente_service.py`
- [x] `app/services/cliente_servicio_service.py`
- [x] `app/services/departament_service.py` (⚠️ typo: renombrar a `departamento_service.py`)
- [x] `app/services/direccion_service.py` — corregido 15/jul (5 bugs)
- [x] `app/services/empleado_service.py`
- [x] `app/services/estado_ticket_service.py`
- [x] `app/services/municipio_service.py`
- [x] `app/services/nivel_impacto_service.py`
- [x] `app/services/plantilla_service.py`
- [x] `app/services/rol_service.py`
- [x] `app/services/servicio_service.py`
- [x] `app/services/ticket_service.py`
- [x] `app/services/tipo_ticket_service.py`

---

## 🌐 Fase 4 — Crear Routers REST ✅ COMPLETADO (15/jul/2026)

### 4.1 Routers construidos y registrados (14/14)

| # | Archivo | Prefijo | Estado |
|---|---------|---------|--------|
| 1 | `canal_router.py` | `/canales` | ✅ |
| 2 | `departamento_router.py` | `/departamentos` | ✅ |
| 3 | `estado_ticket_router.py` | `/estados-ticket` | ✅ |
| 4 | `nivel_impacto_router.py` | `/niveles-impacto` | ✅ |
| 5 | `rol_router.py` | `/roles` | ✅ |
| 6 | `servicio_router.py` | `/servicios` | ✅ |
| 7 | `tipo_ticket_router.py` | `/tipos-ticket` | ✅ |
| 8 | `cliente_router.py` | `/clientes` | ✅ |
| 9 | `cliente_servicio_router.py` | `/cliente_servicios` | ✅ |
| 10 | `direccion_router.py` | `/direcciones` | ✅ (corregido 15/jul) |
| 11 | `empleado_router.py` | `/empleados` | ✅ |
| 12 | `municipio_router.py` | `/municipios` | ✅ |
| 13 | `plantilla_formulario_router.py` | `/plantillas` | ✅ |
| 14 | `ticket_router.py` | `/tickets` | ✅ |

### 4.2 Registrar todos los routers en `main.py`

- [x] **COMPLETADO:** Los 14 routers importados y registrados con `app.include_router()`
- [x] Swagger (`/docs`) muestra 72 endpoints en 14 grupos
- [x] 0 warnings de OpenAPI (corregido el Duplicate Operation ID)

---

## 🔐 Fase 5 — Autenticación JWT

> **Nota:** El DTO `auth_dto.py` ya existe con `LoginRequestDTO` y `TokenResponseDTO`.
> Se usará directamente en el router de auth, sin service intermedio.

### 5.1 Crear utilidades de seguridad
- [ ] `app/core/security.py`:
  - `hash_password(password: str) -> str` (bcrypt / passlib)
  - `verify_password(plain: str, hashed: str) -> bool`
  - `create_access_token(data: dict) -> str` (python-jose)
  - `decode_access_token(token: str) -> dict`

### 5.2 Crear dependencia de auth
- [ ] `app/api/dependencies.py`:
  - `get_current_user(token: str = Depends(oauth2_scheme)) -> Empleado`

### 5.3 Crear router de autenticación
- [ ] `app/api/routers/auth_router.py`:
  - `POST /auth/login` → recibe `LoginRequestDTO`, devuelve `TokenResponseDTO`
  - `GET /auth/me` → devuelve info del usuario autenticado

---

## 🛡️ Fase 6 — Manejo de errores global

- [ ] Handler para `IntegrityError` → 409 Conflict
- [ ] Handler genérico `Exception` → 500

---

## 📄 Fase 7 — Paginación genérica

- [ ] `app/schemas/common.py` → `PaginatedResponse[T]`

---

## 🗃️ Fase 8 — Alembic + seed

- [ ] Instalar `alembic`, inicializar, generar migración
- [ ] `app/db/seed.py` — datos iniciales

---

## 🧪 Fase 9 — Tests

- [ ] `pytest` + `httpx` + `TestClient`

---

## 🧠 Fase 10 — GraphQL (opcional)

---

## 📦 Fase 11 — Docker + despliegue

---

## ⚡ Fase 12 — Migración a async/await (NUEVA)

> **Objetivo:** Convertir toda la app a async para aprovechar el event loop de FastAPI,
> permitir concurrencia real en operaciones I/O (DB, llamadas externas) y mejorar el rendimiento.

### 12.1 — Migrar base de datos a async
- [ ] Instalar `asyncpg` y `sqlalchemy[asyncio]`
- [ ] Cambiar `engine` a `create_async_engine()` con `asyncpg`
- [ ] Cambiar `SessionLocal` a `async_sessionmaker`
- [ ] Actualizar `get_db()` a `async def get_db()` con `async with`

### 12.2 — Migrar Repositories a async
- [ ] Convertir los 15 repositorios a métodos `async def`
- [ ] Usar `await db.execute()` en vez de `db.query()`
- [ ] Usar `select()` de SQLAlchemy 2.0 style (ya compatible con async)

### 12.3 — Migrar Services a async
- [ ] Convertir los 14 services a métodos `async def`
- [ ] `await` en cada llamada al repositorio

### 12.4 — Migrar Routers a async
- [ ] Convertir los 72 endpoints a `async def`
- [ ] `await` en cada llamada al service

### 12.5 — Verificar concurrencia
- [ ] Probar con `httpx.AsyncClient` o `wrk` que múltiples requests se manejan concurrentemente
- [ ] Verificar que no hay bloqueos con SQLAlchemy async

---

## ✅ Orden de ejecución recomendado (ACTUALIZADO 15/jul/2026)

1. [x] ~~Revisar `.env` y verificar que arranca~~ ✅ Fase 1 COMPLETADA
2. [x] ~~Corregir repositorios~~ ✅ Fase 2 COMPLETADA
3. [x] ~~Crear services faltantes~~ ✅ Fase 3 COMPLETADA
4. [x] ~~Crear y registrar los 14 routers~~ ✅ Fase 4 COMPLETADA
5. [ ] **AHORA:** Implementar autenticación JWT (Fase 5)
6. [ ] Exception handlers (Fase 6)
7. [ ] Paginación genérica (Fase 7)
8. [ ] Alembic + seed (Fase 8)
9. [ ] Tests (Fase 9)
10. [ ] GraphQL (Fase 10, opcional)
11. [ ] Docker (Fase 11)
12. [ ] Migración a async/await (Fase 12)