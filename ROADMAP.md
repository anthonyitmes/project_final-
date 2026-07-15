# 🗺️ Roadmap para completar el Backend — `project_final`

> Última actualización: 15/jul/2026 — Fase 4 completada (14/14 routers construidos), Fase 5 (Auth JWT) siguiente

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
| Repositories | ✅ 15/15 estandarizados — todos usan `dict` en update, todos tienen delete |
| Services | ✅ 14/14 implementados |
| Routers (FastAPI) | ✅ 14/14 construidos |
| `main.py` | ⚠️ Solo registra 1 de 14 routers — **siguiente paso inmediato** |
| Auth (JWT) | ❌ Sin implementar — `auth_dto.py` se usará en Fase 5 directamente en el router |
| `.env` | ✅ Existe — requiere revisar `DB_PASSWORD` |
| Exception handlers | ❌ Sin implementar |
| GraphQL | ❌ Carpeta vacía |
| Tests | ❌ Sin tests |

---

## 🔧 Correcciones 30/jun - 06/jul/2026 — Estandarización completa

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

## 🧩 Fase 2 — Repositories ✅ COMPLETADO (06/jul/2026)

- [x] Los 15 repositorios estandarizados con `update(dict)` y `delete`
- [x] `estado_ticket_repository.py` ya no importa schemas
- [x] Contrato único: `(db: Session, id: int, datos: dict) -> Model | None`

---

## 🧠 Fase 3 — Services ✅ COMPLETADO (06/jul/2026)

### 3.1 Services implementados (14/14)

- [x] `app/services/canal_service.py`
- [x] `app/services/cliente_service.py`
- [x] `app/services/cliente_servicio_service.py`
- [x] `app/services/departament_service.py` (⚠️ typo: renombrar a `departamento_service.py`)
- [x] `app/services/direccion_service.py` (⚠️ extensión `.PY` mayúscula, renombrar a `.py`)
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

### 4.1 Routers construidos (14/14)

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
| 9 | `cliente_servicio_router.py` | `/clientes-servicios` | ✅ |
| 10 | `direccion_router.py` | `/direcciones` | ✅ |
| 11 | `empleado_router.py` | `/empleados` | ✅ |
| 12 | `municipio_router.py` | `/municipios` | ✅ |
| 13 | `plantilla_formulario_router.py` | `/plantillas` | ✅ |
| 14 | `ticket_router.py` | `/tickets` | ✅ |

### 4.2 Registrar todos los routers en `main.py`

- [ ] **PENDIENTE:** Importar y registrar los 13 routers faltantes con `app.include_router()`
- [ ] Probar que Swagger (`/docs`) muestra los 14 grupos de endpoints

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

## ✅ Orden de ejecución recomendado (ACTUALIZADO 06/jul/2026)

1. [ ] Revisar `.env` y verificar que arranca (Fase 1)
2. [x] ~~Corregir repositorios~~ ✅ Fase 2 COMPLETADA
3. [x] ~~Crear services faltantes~~ ✅ Fase 3 COMPLETADA
4. [x] ~~Crear los 14 routers~~ ✅ Fase 4 COMPLETADA (pendiente: registrar en `main.py`)
5. [ ] **AHORA:** Implementar autenticación JWT (Fase 5)
6. [ ] Exception handlers (Fase 6)
7. [ ] Paginación genérica (Fase 7)
8. [ ] Alembic + seed (Fase 8)
9. [ ] Tests (Fase 9)
10. [ ] GraphQL (opcional)
11. [ ] Docker