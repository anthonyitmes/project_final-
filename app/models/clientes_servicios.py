from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ClienteServicio(Base):
    __tablename__ = "clientes_servicios"

    id_cliente_servicio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"), nullable=False)
    id_servicio: Mapped[int] = mapped_column(ForeignKey("servicios.id_servicio"), nullable=False)
    fecha_adquisicion: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="clientes_servicios")
    servicio: Mapped["Servicio"] = relationship("Servicio", back_populates="clientes_servicios")


if TYPE_CHECKING:
    from app.models.clientes import Cliente
    from app.models.servicios import Servicio
