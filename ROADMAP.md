# 🗺️ Roadmap para completar el Backend — `project_final`

> Última actualización: 24/jun/2026

---

## 📋 Resumen de estado actual

| Capa | Estado |
|---|---|
| Modelos (SQLAlchemy) | ✅ 13/13 completos |
| Schemas/DTOs (Pydantic) | ✅ Completos |
| Repositories | ⚠️ Solo `ticket_repository` implementado; los demás son stubs |
| Routers (FastAPI) | ⚠️ Solo `ticket_router` implementado |
| Auth (JWT) | ❌ Sin implementar |
| `.env` | ✅ Existe — variables básicas configuradas |
| Exception handlers | ❌ Sin implementar |
| GraphQL | ❌ Carpeta vacía |
| Services | ❌ Carpeta vacía |
| Tests | ❌ Sin tests |

---

## 🧱 Fase 1 — Arreglar lo que impide arrancar

### 1.1 Crear archivo `.env`
- [ ] Crear `/.env` en la raíz del proyecto con al menos:

```env
JWT_SECRET_KEY=dev-secret-key-cambiar-en-produccion
DEBUG=true
DB_USER=postgres
DB_PASSWORD=12345678
DB_HOST=localhost
DB_PORT=5432
DB_NAME=User
```

### 1.2 Verificar que la app arranca
- [ ] Ejecutar `uvicorn app.main:app --reload`
- [ ] Abrir `http://localhost:8000/docs` y confirmar que Swagger carga

---

## 🧩 Fase 2 — Implementar Repositories faltantes

Cada repository debe seguir el mismo patrón que `ticket_repository.py` (clase + instancia singleton).

### 2.1 Repositories de catálogos (CRUD simple)
- [ ] `app/repositories/canal_repository.py` — `CanalRepository` con `get_all`, `get_by_id`, `create`, `update`, `delete`
- [ ] `app/repositories/estado_ticket_repository.py` — `EstadoTicketRepository`
- [ ] `app/repositories/tipo_ticket_repository.py` — `TipoTicketRepository`
- [ ] `app/repositories/nivel_impacto_repository.py` — `NivelImpactoRepository`
- [ ] `app/repositories/plantilla_formulario.repository.py` — `PlantillaFormularioRepository`
- [ ] `app/repositories/servicio_repository.py` — `ServicioRepository`
- [ ] `app/repositories/rol_repository.py` — `RolRepository`
- [ ] `app/repositories/departamento_repository.py` — `DepartamentoRepository`
- [ ] `app/repositories/municipio_repository.py` — `MunicipioRepository`

### 2.2 Repositories de entidades principales (CRUD + queries específicas)
- [ ] `app/repositories/cliente_repository.py` — `ClienteRepository` con:
  - `create`, `get_by_id`, `get_by_dpi`, `get_by_email`, `get_all` (paginado), `update`, `delete`
- [ ] `app/repositories/empleado_repository.py` — `EmpleadoRepository` con:
  - `create`, `get_by_id`, `get_by_email`, `get_all`, `update`, `delete`
- [ ] `app/repositories/direccio_repository.py` — `DireccionRepository` con:
  - `create`, `get_by_id`, `get_by_cliente`, `update`, `delete`
- [ ] `app/repositories/cliente_servicio_repository.py` — `ClienteServicioRepository` con:
  - `create`, `get_by_cliente`, `get_by_servicio`, `delete`

> **Patrón de ejemplo:**
> ```python
> class CanalRepository:
>     def get_all(self, db: Session) -> list[Canal]:
>         return db.query(Canal).all()
> 
>     def get_by_id(self, db: Session, id_canal: int) -> Canal | None:
>         return db.query(Canal).filter(Canal.id_canal == id_canal).first()
> 
>     def create(self, db: Session, canal: Canal) -> Canal:
>         db.add(canal)
>         db.commit()
>         db.refresh(canal)
>         return canal
> 
> canal_repository = CanalRepository()
> ```

---

## 🌐 Fase 3 — Crear Routers REST

### 3.1 Routers de catálogos
- [ ] `app/api/routers/canal_router.py` — CRUD de canales (`GET`, `POST`, `PUT`, `DELETE`)
- [ ] `app/api/routers/estado_ticket_router.py` — CRUD de estados
- [ ] `app/api/routers/tipo_ticket_router.py` — CRUD de tipos de ticket
- [ ] `app/api/routers/nivel_impacto_router.py` — CRUD de niveles de impacto
- [ ] `app/api/routers/plantilla_router.py` — CRUD de plantillas de formulario
- [ ] `app/api/routers/servicio_router.py` — CRUD de servicios
- [ ] `app/api/routers/rol_router.py` — CRUD de roles
- [ ] `app/api/routers/departamento_router.py` — CRUD de departamentos
- [ ] `app/api/routers/municipio_router.py` — CRUD de municipios

### 3.2 Routers de entidades principales
- [ ] `app/api/routers/cliente_router.py`:
  - `POST /clientes` — crear cliente
  - `GET /clientes` — listar con paginación (`skip`/`limit`)
  - `GET /clientes/{id}` — obtener por ID
  - `PUT /clientes/{id}` — actualizar
  - `DELETE /clientes/{id}` — borrado lógico o físico
  - `POST /clientes/{id}/servicios` — asociar servicio
  - `GET /clientes/{id}/servicios` — servicios del cliente
  - `GET /clientes/{id}/direcciones` — direcciones del cliente
- [ ] `app/api/routers/empleado_router.py`:
  - `POST /empleados` — crear empleado (con hash de password)
  - `GET /empleados` — listar
  - `GET /empleados/{id}` — obtener
  - `PUT /empleados/{id}` — actualizar
  - `DELETE /empleados/{id}` — soft delete
- [ ] `app/api/routers/direccion_router.py`:
  - `POST /direcciones` — crear dirección
  - `GET /direcciones/{id}` — obtener
  - `PUT /direcciones/{id}` — actualizar
  - `DELETE /direcciones/{id}` — eliminar

### 3.3 Extender ticket_router existente
- [ ] Agregar `GET /tickets` — listar todos con paginación y filtros opcionales (`?estado=`, `?tecnico=`, `?skip=`, `?limit=`)
- [ ] Agregar `DELETE /tickets/{id}` — soft delete
- [ ] Mover `db.commit()` del router al repository (crear método `update_ticket` en `ticket_repository`)

### 3.4 Registrar todos los routers en `main.py`
- [ ] Importar y registrar cada router con `app.include_router()`

---

## 🔐 Fase 4 — Autenticación JWT

### 4.1 Crear utilidades de seguridad
- [ ] `app/core/security.py`:
  - `hash_password(password: str) -> str` (usando `passlib` o `bcrypt`)
  - `verify_password(plain: str, hashed: str) -> bool`
  - `create_access_token(data: dict) -> str` (usando `python-jose`)
  - `decode_access_token(token: str) -> dict`

### 4.2 Crear dependencia de auth
- [ ] `app/api/dependencies.py`:
  - `get_current_user(token: str = Depends(oauth2_scheme)) -> Empleado`
  - Validar token JWT, extraer `sub` (email), buscar empleado en BD
  - Lanzar `HTTPException 401` si no es válido

### 4.3 Crear router de autenticación
- [ ] `app/api/routers/auth_router.py`:
  - `POST /auth/login` — recibe `LoginRequestDTO`, valida credenciales, devuelve `TokenResponseDTO`
  - `GET /auth/me` — devuelve info del usuario autenticado (protegido)

### 4.4 Proteger endpoints
- [ ] Agregar `current_user: Empleado = Depends(get_current_user)` a los endpoints que deban estar protegidos
- [ ] Opcional: crear dependencia `require_role(role_name)` para autorización por rol

---

## 🛡️ Fase 5 — Manejo de errores global

### 5.1 Exception handlers en `main.py`
- [ ] Handler para `SQLAlchemyError` / `IntegrityError` → 409 Conflict
- [ ] Handler para `ValidationError` de Pydantic → 422 (FastAPI ya lo maneja, pero se puede personalizar)
- [ ] Handler genérico `Exception` → 500 con mensaje genérico (sin leak de detalles internos)
- [ ] Handler para `HTTPException` → mantener comportamiento default

> ```python
> from sqlalchemy.exc import IntegrityError
> 
> @app.exception_handler(IntegrityError)
> def integrity_error_handler(request, exc):
>     raise HTTPException(status_code=409, detail="Conflicto: el recurso ya existe o viola una restricción")
> ```

---

## 📄 Fase 6 — Paginación

### 6.1 Crear schema de paginación genérico
- [ ] `app/schemas/common.py`:
  - `class PaginatedResponse(BaseModel)` con `items`, `total`, `skip`, `limit`
- [ ] Usarlo en todos los endpoints GET de lista

---

## 🧪 Fase 7 — Tests

### 7.1 Setup
- [ ] Instalar `pytest`, `httpx`, `pytest-asyncio`
- [ ] Crear `tests/` con `__init__.py` y `conftest.py`
- [ ] En `conftest.py`: fixture `TestClient` + base de datos de prueba (SQLite en memoria o PostgreSQL de test)

### 7.2 Tests mínimos por módulo
- [ ] `tests/test_ticket_router.py` — crear, leer, actualizar ticket
- [ ] `tests/test_cliente_router.py` — CRUD cliente
- [ ] `tests/test_auth.py` — login exitoso, login fallido, token inválido

---

## 🗃️ Fase 8 — Base de datos (migraciones + seed)

### 8.1 Migraciones con Alembic
- [ ] Instalar `alembic`
- [ ] `alembic init alembic`
- [ ] Configurar `alembic.ini` y `alembic/env.py` para usar `Base.metadata`
- [ ] Generar migración inicial: `alembic revision --autogenerate -m "initial"`
- [ ] Aplicar: `alembic upgrade head`

### 8.2 Datos semilla (seed)
- [ ] `app/db/seed.py` — script para insertar datos iniciales:
  - Roles (admin, técnico, recepcionista)
  - Estados de ticket (abierto, en progreso, resuelto, cerrado)
  - Canales (teléfono, web, presencial)
  - Niveles de impacto (bajo, medio, alto, crítico)
  - Tipos de ticket (consulta, incidente, solicitud)
  - Usuario admin por defecto
- [ ] Ejecutar con: `python -m app.db.seed`

---

## 🧠 Fase 9 — GraphQL (opcional, futuro)

- [ ] Usar **Strawberry** o **Ariadne** (recomendado Strawberry por tipado nativo)
- [ ] Crear `app/graphql/schema.py` con tipos y queries
- [ ] Montar en FastAPI con `GraphQLRouter`

---

## 📦 Fase 10 — Docker + despliegue

- [ ] Crear `Dockerfile` para la app FastAPI
- [ ] Crear `docker-compose.yml` con servicios: `app` + `postgres`
- [ ] Verificar que `uvicorn` corre dentro del contenedor

---

## ✅ Checklist rápido (orden de ejecución)

1. [ ] Crear `.env`
2. [ ] Verificar que arranca
3. [ ] Implementar todos los repositories stub
4. [ ] Crear routers de catálogos
5. [ ] Crear router de clientes
6. [ ] Crear router de empleados
7. [ ] Crear router de direcciones
8. [ ] Extender ticket_router (paginación, delete)
9. [ ] Registrar routers en `main.py`
10. [ ] Implementar `security.py` (hash + JWT)
11. [ ] Crear `auth_router.py`
12. [ ] Crear dependencia `get_current_user`
13. [ ] Proteger endpoints
14. [ ] Exception handlers globales
15. [ ] Paginación genérica
16. [ ] Alembic setup + migración inicial
17. [ ] Seed script
18. [ ] Tests básicos
19. [ ] Docker + docker-compose