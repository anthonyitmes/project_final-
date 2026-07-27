# 🔐 Fases 5, 6, 7 — Auth JWT, Exception Handlers y Paginación

**Fecha:** 2026-07-27
**Autor:** Anthony Sub (verificación y documentación)
**Rama:** `main`
**Commit base:** `6407a12`

---

## Resumen — Las 3 fases ya estaban completadas

Durante la verificación de la Fase 8, se detectó que las fases 5, 6 y 7 también estaban implementadas pero el `ROADMAP.md` seguía marcándolas como pendientes. Este documento consolida la evidencia del estado real de cada una.

| Fase | Estado real | En ROADMAP (antes) | Archivos clave |
|---|---|---|---|
| 5 — Auth JWT | ✅ Completa | ❌ Pendiente | `security.py`, `dependencies.py`, `auth_router.py`, `auth_dto.py` |
| 6 — Exception handlers | ✅ Completa | ❌ Pendiente | `main.py` (líneas 28-40) |
| 7 — Paginación genérica | ✅ Completa | ❌ Pendiente | `schemas/common.py` |

---

## Fase 5 — Autenticación JWT ✅

### 5.1 `app/core/security.py` — Utilidades de seguridad (106 líneas)

```python
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str       # bcrypt
def verify_password(plain: str, hashed: str) -> bool
def create_access_token(data: dict) -> str    # python-jose, expira en ACCESS_TOKEN_EXPIRE_MINUTES
def decode_access_token(token: str) -> dict   # lanza JWTError si el token es inválido
```

**¿Qué hace?** Proporciona las 4 funciones criptográficas necesarias para el ciclo completo de autenticación: hashear contraseñas al crear usuarios, verificarlas al hacer login, generar tokens JWT firmados con `JWT_SECRET_KEY` (definida en `.env`), y decodificarlos/validarlos en cada petición protegida.

**¿Por qué bcrypt?** Es el estándar _de facto_ para hashing de contraseñas. Incluye salt automático y es resistente a ataques de fuerza bruta por su costo computacional configurable. `passlib` lo abstrae y permite migrar a algoritmos futuros sin cambiar el código.

**¿Por qué python-jose?** Es la librería recomendada en la documentación oficial de FastAPI para JWT. Soporta HS256, RS256 y otros algoritmos. Aquí se usa HS256 (simétrico) porque la misma app emite y verifica los tokens.

### 5.2 `app/api/dependencies.py` — Dependencia `get_current_user` (84 líneas)

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Empleado:
    # 1. Decodifica el token → extrae email del claim "sub"
    # 2. Busca al empleado en la BD por email
    # 3. Verifica que esté activo
    # 4. Devuelve el objeto Empleado (o lanza 401)
```

**¿Qué hace?** Es una dependencia de FastAPI que se inyecta en cualquier endpoint protegido. Extrae el token del header `Authorization: Bearer <token>`, lo valida, busca al usuario en la BD y verifica que esté activo. Si algo falla, devuelve `HTTPException 401`.

**¿Por qué así?** FastAPI tiene un sistema de inyección de dependencias que permite proteger endpoints declarativamente. Con solo agregar `current_user: Empleado = Depends(get_current_user)` a la firma de un endpoint, toda la lógica de autenticación se ejecuta automáticamente antes de entrar al cuerpo del endpoint.

**¿Por qué `OAuth2PasswordBearer`?** Es el esquema estándar que Swagger UI reconoce. Agrega el botón "Authorize" con candado en `/docs`, permitiendo probar endpoints protegidos ingresando el token manualmente.

### 5.3 `app/api/routers/auth_router.py` — Router de autenticación (85 líneas)

```python
router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=TokenResponseDTO)
def login(credentials: LoginRequestDTO, db: Session = Depends(get_db)):
    # 1. Busca empleado por email → 401 si no existe
    # 2. Verifica que esté activo → 401 si desactivado
    # 3. Verifica contraseña con verify_password() → 401 si no coincide
    # 4. Genera token con create_access_token({"sub": email})
    # 5. Devuelve TokenResponseDTO(access_token=..., token_type="bearer")

@router.get("/me", response_model=EmpleadoResponseDTO)
def get_me(current_user: Empleado = Depends(get_current_user)):
    return current_user  # protegido por get_current_user
```

**¿Qué hace?** Dos endpoints:
- `POST /auth/login`: autentica al usuario con email + contraseña y devuelve un JWT.
- `GET /auth/me`: devuelve los datos del empleado autenticado. Protegido por `get_current_user`.

**¿Por qué el router de auth consulta la BD directamente (`db.query(Empleado)`)?** La regla de oro dice "Router → Service → Repository → BD", pero el ROADMAP original (línea 172) estableció explícitamente: _"Se usará directamente en el router de auth, sin service intermedio"_. La razón es que `POST /auth/login` es un endpoint de infraestructura (no de negocio): no crea, actualiza ni elimina entidades de dominio, solo autentica. Usar un service aquí añadiría una capa de abstracción innecesaria para una operación que es puramente de seguridad.

### 5.4 `app/schemas/auth_dto.py` — DTOs de autenticación (14 líneas)

```python
class LoginRequestDTO(BaseModel):
    email: str
    password: str

class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

**¿Por qué DTOs separados para auth?** Los DTOs de autenticación son conceptualmente distintos de los DTOs de dominio. `LoginRequestDTO` solo tiene credenciales (no es una entidad de BD). `TokenResponseDTO` solo tiene el token (no mapea a ninguna tabla). Mantenerlos en `auth_dto.py` separado de `empleado_dto.py` sigue el principio de responsabilidad única.

### 5.5 Registro en `main.py`

```python
from app.api.routers.auth_router import router as auth_router  # línea 22
app.include_router(auth_router)                                 # línea 43 (primer router registrado)
```

El router de auth se registra **primero** para que Swagger lo muestre al inicio de la lista de endpoints.

---

## Fase 6 — Exception Handlers ✅

### 6.1 Implementación en `main.py` (líneas 28-40)

```python
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Violación de integridad: El recurso ya existe o hay datos en conflicto"}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
    )
```

**¿Qué hace?** Captura excepciones no manejadas a nivel global y las convierte en respuestas JSON estructuradas en lugar de dejar que FastAPI devuelva un traceback HTML o un error genérico sin formato.

**¿Por qué `IntegrityError` → 400 y no 409?** El ROADMAP sugería 409 Conflict, pero el desarrollador eligió 400 Bad Request. Técnicamente:
- **409 Conflict** es más correcto semánticamente: "la petición no pudo completarse por un conflicto con el estado actual del recurso" (RFC 7231).
- **400 Bad Request** es más genérico: "la petición es inválida".

En la práctica, ambos funcionan. 409 sería más preciso porque `IntegrityError` de SQLAlchemy ocurre típicamente por violación de unique constraints (intentar crear un recurso que ya existe) o foreign key constraints (referenciar un registro inexistente). **Se recomienda cambiar 400 → 409** para cumplir con el estándar HTTP, pero no es bloqueante.

### 6.2 ¿Por qué el handler genérico captura `Exception`?

Capturar `Exception` (la clase base de todas las excepciones no-sistema) garantiza que **cualquier error inesperado** (TypeError, ValueError, AttributeError, etc.) devuelva un 500 con un mensaje controlado, en lugar de exponer detalles internos del servidor. Esto es una buena práctica de seguridad: nunca se debe filtrar el traceback al cliente en producción.

---

## Fase 7 — Paginación Genérica ✅

### 7.1 `app/schemas/common.py` — `PaginatedResponse[T]` (35 líneas)

```python
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
```

**¿Qué hace?** Define un schema genérico para respuestas paginadas. Usa `Generic[T]` de Pydantic para que Swagger muestre el tipo concreto. Por ejemplo:

```python
@router.get("", response_model=PaginatedResponse[ClienteResponseDTO])
def get_all_clientes(page: int = 1, size: int = 20):
    ...
    return PaginatedResponse(
        items=[...],
        total=100,
        page=page,
        size=size,
        pages=5,
    )
```

**¿Por qué `Generic[T]`?** Sin genéricos, cada entidad necesitaría su propio schema de paginación (`PaginatedClienteResponse`, `PaginatedCanalResponse`, etc.), lo que generaría 14 archivos duplicados con la misma estructura. Con `Generic[T]`, un solo schema sirve para todas las entidades.

**¿Por qué incluye `pages`?** `pages = ceil(total / size)`. Incluirlo en la respuesta evita que el frontend tenga que calcularlo. Sigue el estándar de APIs paginadas (GitHub, Stripe, etc.).

**Campos de la respuesta:**

| Campo | Tipo | Propósito |
|---|---|---|
| `items` | `list[T]` | Registros de la página actual |
| `total` | `int` | Cantidad total de registros en BD |
| `page` | `int` | Página actual (1-based) |
| `size` | `int` | Cantidad máxima por página |
| `pages` | `int` | Cantidad total de páginas |

---

## Verificación de integridad

### Fase 5 — Auth JWT

| Componente | Archivo | Líneas | Estado |
|---|---|---|---|
| Hash + verify password | `app/core/security.py` | 1-55 | ✅ |
| Crear + decodificar token | `app/core/security.py` | 57-106 | ✅ |
| Dependencia `get_current_user` | `app/api/dependencies.py` | 1-84 | ✅ |
| `POST /auth/login` | `app/api/routers/auth_router.py` | 22-65 | ✅ |
| `GET /auth/me` | `app/api/routers/auth_router.py` | 68-85 | ✅ |
| DTOs de auth | `app/schemas/auth_dto.py` | 1-14 | ✅ |
| Registro en `main.py` | `app/main.py:22,43` | — | ✅ |
| `python-jose` en `requirements.txt` | `requirements.txt:30` | — | ✅ |
| `JWT_SECRET_KEY` en `.env` | `.env` | — | ✅ |

### Fase 6 — Exception Handlers

| Componente | Archivo | Líneas | Estado |
|---|---|---|---|
| `IntegrityError` → 400 | `app/main.py` | 28-33 | ✅ |
| `Exception` → 500 | `app/main.py` | 35-40 | ✅ |

### Fase 7 — Paginación Genérica

| Componente | Archivo | Líneas | Estado |
|---|---|---|---|
| `PaginatedResponse[T]` | `app/schemas/common.py` | 1-35 | ✅ |

---

## Observaciones

### 1. `IntegrityError` handler devuelve 400 en vez de 409
El ROADMAP original especificaba `IntegrityError` → 409 Conflict. La implementación actual usa 400. 409 es semánticamente más correcto. **Recomendación:** cambiar a 409 en una futura iteración.

### 2. El handler genérico captura `Exception` sin logging
No hay `print()` ni `logging.error()` dentro del handler genérico. En producción, los errores 500 desaparecerían sin dejar rastro. **Recomendación:** agregar `logging.exception(exc)` dentro del handler para mantener trazabilidad.

### 3. `PaginatedResponse` no está siendo usado en ningún router aún
El schema existe pero los 14 routers no lo usan — todos devuelven `list[T]` directamente. Esto es esperable: la Fase 7 solo pedía _crear_ el schema. Una fase futura debería _aplicarlo_ a los endpoints de listado.

### 4. El tipado de `PaginatedResponse` es compatible con Pydantic v2
Usa `BaseModel, Generic[T]` que es la sintaxis correcta para Pydantic v2 (a diferencia de Pydantic v1 que usaba `GenericModel`). Verificado con la versión `pydantic==2.13.4` en `requirements.txt`.

---

## Conclusión

**Fases 5, 6 y 7 — COMPLETADAS ✅**

Las 3 fases estaban implementadas antes de esta verificación. El ROADMAP no reflejaba su estado real. Con este documento y la actualización del ROADMAP, quedan correctamente documentadas.

**Próxima fase realmente pendiente:** Fase 9 — Tests (`pytest` + `httpx` + `TestClient`)