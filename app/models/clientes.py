from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Cliente(Base):
    """Modelo para clientes."""

    __tablename__ = "clientes"

    # PK
    id_cliente: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Datos personales
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    dpi: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    celular: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    direcciones: Mapped[list["Direccion"]] = relationship("Direccion", back_populates="cliente")
    clientes_servicios: Mapped[list["ClienteServicio"]] = relationship("ClienteServicio", back_populates="cliente")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="cliente")

if TYPE_CHECKING:
    from app.models.direcciones import Direccion
    from app.models.clientes_servicios import ClienteServicio
    from app.models.tickets import Ticket