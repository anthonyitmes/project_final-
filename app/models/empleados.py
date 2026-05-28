from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Empleado(Base):
    """Modelo para la tabla 'empleados'. Representa un empleado del sistema."""

    __tablename__ = "empleados"

    # PK: identificador del empleado
    id_empleado: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Nombre completo del empleado
    nombre_empleado: Mapped[str] = mapped_column(String(100), nullable=False)
    # Email único del empleado
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    # Contraseña hasheada
    password_bash: Mapped[str] = mapped_column(String(255), nullable=False)
    # Estado activo/inactivo
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # FK a roles.id_rol para relacionar el empleado con su rol
    id_rol: Mapped[int] = mapped_column(ForeignKey("roles.id_rol"), nullable=False)
    # Relación many -> one. 'back_populates' enlaza con 'empleados' en Rol.
    rol: Mapped["Rol"] = relationship("Rol", back_populates="empleados")


if TYPE_CHECKING:
    from app.models.roles import Rol







