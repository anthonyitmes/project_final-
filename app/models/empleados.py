from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Empleado(Base):
    """Modelo para la tabla 'empleados'. Representa un empleado del sistema."""

    __tablename__ = "empleados"

    id_empleado: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_empleado: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_bash: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    id_rol: Mapped[int] = mapped_column(ForeignKey("roles.id_rol"), nullable=False)
    rol: Mapped["Rol"] = relationship("Rol", back_populates="empleados")
    tickets_receptor: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="receptor",
        foreign_keys="[Ticket.id_receptor]",
    )
    tickets_tecnico: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="tecnico",
        foreign_keys="[Ticket.id_tecnico]",
    )


if TYPE_CHECKING:
    from app.models.roles import Rol
    from app.models.tickets import Ticket







