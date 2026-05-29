from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Direccion(Base):
    """Direcciones de clientes: relación con `Cliente` y `Municipio`."""

    __tablename__ = "direcciones"

    id_direccion: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    descripcion: Mapped[str] = mapped_column(String(255), nullable=False)
    calle: Mapped[str] = mapped_column(String(255), nullable=False)
    zona: Mapped[str] = mapped_column(String(50), nullable=False)
    avenida: Mapped[str | None] = mapped_column(String(255), nullable=True)
    referencia: Mapped[str | None] = mapped_column(String(255), nullable=True)
    detalles_direccion: Mapped[str] = mapped_column(String(255), nullable=False)

    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"), nullable=False)
    id_municipio: Mapped[int] = mapped_column(ForeignKey("municipios.id_municipio"), nullable=False)

    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="direcciones")
    municipio: Mapped["Municipio"] = relationship("Municipio", back_populates="direcciones")


if TYPE_CHECKING:
    from app.models.clientes import Cliente
    from app.models.municipios import Municipio
