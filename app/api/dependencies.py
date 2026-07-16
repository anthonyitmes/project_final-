"""
Dependencias reutilizables para los endpoints de FastAPI.

La dependencia principal es get_current_user, que extrae y valida
el token JWT del header Authorization y devuelve el empleado autenticado.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.empleados import Empleado
from app.models.roles import Rol

# ── Esquema OAuth2 ──────────────────────────────────────────────────
# OAuth2PasswordBearer espera el token en el header:
#   Authorization: Bearer <token>
# La URL tokenUrl es la ruta de login que Swagger usará
# para mostrar el botón "Authorize" con candado.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Empleado:
    """
    Dependencia que protege cualquier endpoint que la incluya.

    Flujo:
      1. Extrae el token JWT del header Authorization.
      2. Decodifica el token → obtiene el email del claim "sub".
      3. Busca al empleado en la BD por email.
      4. Si el empleado no existe o está inactivo → 401.
      5. Devuelve el objeto Empleado para que el endpoint lo use.

    Args:
        token: JWT extraído automáticamente por OAuth2PasswordBearer.
        db: Sesión de BD inyectada por get_db.

    Returns:
        El objeto Empleado autenticado.

    Raises:
        HTTPException 401: Si el token es inválido, expiró, el usuario
            no existe o está desactivado.

    Uso en un endpoint protegido:
        @router.get("/perfil")
        def mi_perfil(current_user: Empleado = Depends(get_current_user)):
            return {"nombre": current_user.nombre_empleado}
    """
    # ── 1. Excepción genérica por credenciales inválidas ─────────────
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # ── 2. Decodificar el token ─────────────────────────────────────
    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # ── 3. Buscar al empleado en la base de datos ────────────────────
    empleado = db.query(Empleado).filter(Empleado.email == email).first()
    if empleado is None:
        raise credentials_exception

    # ── 4. Verificar que el empleado esté activo ─────────────────────
    if not empleado.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario desactivado",
        )

    return empleado