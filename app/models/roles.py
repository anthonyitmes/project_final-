from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Rol(Base):
    """Modelo para la tabla 'roles'. Representa un rol dentro del sistema."""

    __tablename__ = "roles"

    # PK: identificador del rol
    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Nombre del rol
    nombre_rol: Mapped[str] = mapped_column(String(100), nullable=False)
    # Descripción opcional del rol
    descripcion: Mapped[str] = mapped_column(String(255), nullable=False)
    # Relación 1:N con Empleado. Un rol puede tener varios empleados.
    empleados: Mapped[list["Empleado"]] = relationship("Empleado", back_populates="rol")


