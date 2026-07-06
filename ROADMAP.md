# 🗺️ Roadmap para completar el Backend — `project_final`

> Última actualización: 05/jul/2026 — Verificación de services, corrección de estado

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

## 📋 Resumen de estado actual (05/jul/2026)

| Capa | Estado |
|---|---|
| Modelos (SQLAlchemy) | ✅ 14/14 completos |
| Schemas/DTOs (Pydantic) | ✅ Completos (15 archivos — `auth_dto.py` no requiere service propio) |
| Repositories | ✅ 15/15 archivos existen — pendiente auditar calidad de `update()` y `delete()` |
| Services | ⚠️ 11/14 implementados — faltan 3 |
| Routers (FastAPI) | ⚠️ Solo 1/14 implementado: `ticket_router` |
| `main.py` | ⚠️ Solo registra `ticket_router` |
| Auth (JWT) | ❌ Sin implementar — `auth_dto.py` se usará en Fase 5 directamente en el router |
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

## 🧠 Fase 3 — Completar Services

### 3.1 Services YA implementados (11/14)

- [x] `app/services/canal_service.py` — Completo (corregido 30/jun)
- [x] `app/services/cliente_service.py` — Implementado
- [x] `app/services/cliente_servicio_service.py` — Implementado
- [x] `app/services/departament_service.py` — Implementado (⚠️ typo: renombrar a `departamento_service.py`)
- [x] `app/services/direccion_service.py` — Implementado (⚠️ extensión `.PY` mayúscula, renombrar a `.py`)
- [x] `app/services/empleado_service.py` — Implementado
- [x] `app/services/estado_ticket_service.py` — Implementado
- [x] `app/services/municipio_service.py` — Implementado
- [x] `app/services/nivel_impacto_service.py` — Implementado
- [x] `app/services/rol_service.py` — Implementado
- [x] `app/services/ticket_service.py` — Completo (refactorizado 27/jun, corregido 30/jun)

### 3.2 Services FALTANTES (3)

- [ ] `app/services/servicio_service.py` → Model: `servicios.py`, Repo: `servicio_repository.py`, DTO: `servicio_dto.py`
- [ ] `app/services/plantilla_service.py` → Model: `plantilla_formulario.py`, Repo: `plantilla_formulario.repository.py`, DTO: `plantilla_formulario_dto.py`
- [ ] `app/services/tipo_ticket_service.py` → Model: `tipos_ticket.py`, Repo: `tipo_ticket_repository.py`, DTO: `tipo_ticket_dto.py`

> **Patrón de referencia:** `app/services/canal_service.py`

### 3.3 ¿Por qué `auth_dto.py` NO necesita service?

`auth_dto.py` contiene DTOs de transporte para autenticación JWT:
- `LoginRequestDTO` → email + password (entrada)
- `TokenResponseDTO` → access_token + token_type (salida)

Estos DTOs se usarán **directamente en el router de autenticación** (`auth_router.py`)
en la Fase 5. No representan una entidad de base de datos, no tienen repository,
y la lógica de autenticación (hash, verify, JWT) vive en `app/core/security.py`,
no en un service CRUD tradicional.

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

> **Nota:** El DTO `auth_dto.py` ya existe. Se usará directamente aquí, sin service intermedio.

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
  - `POST /auth/login` → recibe `LoginRequestDTO`, devuelve `TokenResponseDTO`
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

## ✅ Orden de ejecución recomendado (ACTUALIZADO 05/jul/2026)

1. [ ] Revisar `.env` y verificar que arranca (Fase 1)
2. [ ] Corregir typos: renombrar `departament_service.py` → `departamento_service.py`, `direccion_service.PY` → `direccion_service.py`
3. [ ] **PRIORITARIO:** Crear los 3 services faltantes: `servicio_service.py`, `plantilla_service.py`, `tipo_ticket_service.py` (Fase 3.2)
4. [ ] Corregir los repos con bugs conocidos (Fase 2.1)
5. [ ] Revisar y estandarizar los repos no auditados (Fase 2.2)
6. [ ] Crear todos los routers + registrar en `main.py` (Fase 4)
7. [ ] Implementar autenticación JWT (Fase 5)
8. [ ] Exception handlers (Fase 6)
9. [ ] Paginación genérica (Fase 7)
10. [ ] Alembic + seed (Fase 8)
11. [ ] Tests (Fase 9)
12. [ ] GraphQL (opcional — Fase 10)
13. [ ] Docker (Fase 11)