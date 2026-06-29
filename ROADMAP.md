# 🗺️ Roadmap para completar el Backend — `project_final`

> Última actualización: 27/jun/2026 — Refactorización de capa Service + Router completada

---

## 🧠 Conceptos clave (glosario rápido)

| Capa | Carpeta | Responsabilidad | Herramienta |
|------|---------|----------------|-------------|
| **Models** | `app/models/` | Estructura de las tablas en la BD (columnas, FK, relaciones) | SQLAlchemy ORM |
| **Schemas / DTOs** | `app/schemas/` | Forma de los datos que entran/salen por la API (validación y serialización) | Pydantic |
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

---

## 📋 Resumen de estado actual

| Capa | Estado |
|---|---|
| Modelos (SQLAlchemy) | ✅ 13/13 completos |
| Schemas/DTOs (Pydantic) | ✅ Completos |
| Repositories | ⚠️ Solo `ticket_repository` implementado (refactorizado 27/jun: nombres, paginacion, filtros, update con dict) |
| Services | ⚠️ Solo `ticket_service` implementado (refactorizado 27/jun: update_ticket delega al repo, delete_ticket, get_all_tickets) |
| Routers (FastAPI) | ⚠️ Solo `ticket_router` implementado (refactorizado 27/jun: +GET paginado, +DELETE, docstring) |
| Auth (JWT) | ❌ Sin implementar |
| `.env` | ✅ Existe — requiere revisar `DB_PASSWORD` |
| Exception handlers | ❌ Sin implementar |
| GraphQL | ❌ Carpeta vacía |
| Tests | ❌ Sin tests |
| Refactorizacion Service/Repo | ✅ Completada 27/jun: update_ticket ya no usa db.commit() |



## 🔧 Refactorizacion 27/jun/2026 — Correccion arquitectonica Service/Repository

### Cambios realizados:

| Archivo | Que se corrigio |
|---------|----------------|
| `ticket_repository.py` | Nombres consistentes (`get_tickets_by_cliente`), `get_all` con paginacion+filtros, `update_ticket` recibe `dict` |
| `ticket_service.py` | **CRITICO:** `update_ticket` ya NO llama a `db.commit()` ni `db.refresh()`. Delega al Repository via dict. Se agrego `delete_ticket` y `get_all_tickets`. |
| `ticket_router.py` | Se agrego `GET /tickets` paginado, `DELETE /tickets/{id}`, docstrings. |

### Regla de oro establecida:

```
Router -> Service -> Repository -> BD
HTTP      NEGOCIO    PERSISTENCIA   SQL

EL SERVICE NUNCA TOCA: db.commit(), db.add(), db.refresh(), db.delete()
ESO ES TERRITORIO EXCLUSIVO DEL REPOSITORY
El Service construye un dict y se lo pasa al Repository
```

### Lo que falta para cerrar este bloque:

- [ ] Renombrar `ticket_service_new.py` -> `ticket_service.py` (el viejo quedo con codigo duplicado, ver seccion NOTA abajo)
- [ ] Agregar `get_all_tickets` al service (ya esta en el archivo nuevo, falta renombrar)

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

## 🧩 Fase 2 — Implementar Repositories faltantes

Cada repository sigue el patrón: clase con métodos CRUD + instancia singleton al final del archivo.

### 2.1 Repositories de catálogos (CRUD simple: `get_all`, `get_by_id`, `create`, `update`, `delete`)
- [ ] `app/repositories/canal_repository.py`
- [ ] `app/repositories/estado_ticket_repository.py`
- [ ] `app/repositories/tipo_ticket_repository.py`
- [ ] `app/repositories/nivel_impacto_repository.py`
- [ ] `app/repositories/plantilla_formulario_repository.py`
- [ ] `app/repositories/servicio_repository.py`
- [ ] `app/repositories/rol_repository.py`
- [ ] `app/repositories/departamento_repository.py`
- [ ] `app/repositories/municipio_repository.py`

### 2.2 Repositories de entidades principales (CRUD + queries específicas)
- [ ] `app/repositories/cliente_repository.py` — `get_by_dpi`, `get_by_email`, `get_all` paginado
- [ ] `app/repositories/empleado_repository.py` — `get_by_email`, `get_all` paginado
- [ ] `app/repositories/direccion_repository.py` — `get_by_cliente`
- [ ] `app/repositories/cliente_servicio_repository.py` — `get_by_cliente`, `get_by_servicio`

### 2.3 Extender `ticket_repository` existente ✅ COMPLETADO (27/jun)
- [x] Agregar `update_ticket(db, id_ticket, datos)` — ✅ Recibe dict, sin logica de negocio
- [x] Agregar `delete_ticket(db, id_ticket)` — ✅ Delete fisico (TODO: soft-delete futuro)
- [x] Agregar `get_all(db, skip, limit, filtros)` — ✅ Listado paginado con filtros dinamicos

> **Patrón de referencia:** `app/repositories/ticket_repository.py`

---

## 🧠 Fase 3 — Implementar Services

**Nuevo:** Cada entidad principal tendrá su service que contiene la lógica de negocio. Los routers solo delegan.

### 3.1 Services de catálogos
- [ ] `app/services/canal_service.py`
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

### 3.3 Service existente — `ticket_service` ✅ COMPLETADO (27/jun)
- [x] `app/services/ticket_service.py` — implementado y funcionando
- [x] Extender con `delete_ticket`, `get_all_tickets` (paginado + filtros) ✅ Hecho

> **Patrón de referencia:** `app/services/ticket_service.py`

---

## 🌐 Fase 4 — Crear Routers REST

Cada router recibe la petición HTTP, llama al service y devuelve la respuesta. **Nunca contiene lógica de negocio ni acceso directo a BD.**

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

### 4.3 Router existente — `ticket_router` ✅ COMPLETADO (27/jun)
- [x] `app/api/routers/ticket_router.py` — refactorizado con service
- [x] Agregar `GET /tickets` — ✅ Paginado con filtros (`?skip=`, `?limit=`, `?id_estado=`, `?id_tecnico=`, `?id_cliente=`)
- [x] Agregar `DELETE /tickets/{id}` — ✅ Delete fisico (TODO: soft-delete futuro)

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

## ✅ Orden de ejecución recomendado

1. [ ] Revisar `.env` y verificar que arranca (Fase 1)
2. [ ] Implementar todos los repositories (Fase 2)
3. [ ] Implementar todos los services (Fase 3)
4. [ ] Crear routers de catálogos + registrar en `main.py` (Fase 4.1 + 4.4)
5. [ ] Crear routers de entidades principales (Fase 4.2)
6. [x] Extender `ticket_router` con paginacion y delete (Fase 4.3) ✅ COMPLETADO 27/jun
7. [ ] Implementar autenticación JWT (Fase 5)
8. [ ] Exception handlers (Fase 6)
9. [ ] Paginación genérica (Fase 7)
10. [ ] Alembic + seed (Fase 8)
11. [ ] Tests (Fase 9)
12. [ ] GraphQL (opcional — Fase 10)
13. [ ] Docker (Fase 11)