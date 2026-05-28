from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Direccion(Base):
    """Direcciones de clientes: relación con `Cliente` y `Municipio`."""

    __tablename__ = "direcciones"

    # PK
    id_direccion: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Campos de la dirección
    descripcion: Mapped[str] = mapped_column(String(255), nullable=False)
    calle: Mapped[str] = mapped_column(String(255), nullable=False)
    zona: Mapped[str] = mapped_column(String(255), nullable=False)
    avenida: Mapped[str] = mapped_column(String(255), nullable=False)
    referencia: Mapped[str] = mapped_column(String(255), nullable=True)

    # FK hacia municipio y cliente (almacenan los ids asociados)
    id_municipio: Mapped[int] = mapped_column(ForeignKey("municipios.id_municipio"), nullable=False)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"), nullable=False)

    # Relaciones ORM: permiten acceder a objetos relacionados en Python
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="direcciones")
    municipio: Mapped["Municipio"] = relationship("Municipio", back_populates="direcciones")


if TYPE_CHECKING:
    # Importes sólo para chequeo de tipos y evitar ciclos de import en tiempo de ejecución
    from app.models.clientes import Cliente
    from app.models.municipios import Municipio
