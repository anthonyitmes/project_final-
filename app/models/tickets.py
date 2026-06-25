from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id_ticket: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo_ticket: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    # Campos de clave foránea
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"), nullable=False)
    id_receptor: Mapped[int] = mapped_column(ForeignKey("empleados.id_empleado"), nullable=False)
    id_tecnico: Mapped[int | None] = mapped_column(ForeignKey("empleados.id_empleado"), nullable=True)
    id_canal: Mapped[int] = mapped_column(ForeignKey("canales.id_canal"), nullable=False)
    id_estado: Mapped[int] = mapped_column(ForeignKey("estado_ticket.id_estado"), nullable=False)
    id_tipo_ticket: Mapped[int] = mapped_column(ForeignKey("tipos_ticket.id_tipo_ticket"), nullable=False)
    id_impacto: Mapped[int] = mapped_column(ForeignKey("niveles_impacto.id_impacto"), nullable=False)
    id_plantilla: Mapped[int] = mapped_column(ForeignKey("plantilla_formulario.id_plantilla"), nullable=False)

    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str] = mapped_column(String, nullable=False)
    datos_respuesta: Mapped[dict] = mapped_column(JSONB, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_resolucion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Relación con otras tablas
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="tickets")
    receptor: Mapped["Empleado"] = relationship("Empleado", back_populates="tickets_receptor", foreign_keys=[id_receptor])
    tecnico: Mapped["Empleado"] = relationship("Empleado", back_populates="tickets_tecnico", foreign_keys=[id_tecnico])
    canal: Mapped["Canal"] = relationship("Canal", back_populates="tickets")
    estado: Mapped["EstadoTicket"] = relationship("EstadoTicket", back_populates="tickets")
    tipo_ticket: Mapped["TipoTicket"] = relationship("TipoTicket", back_populates="tickets")
    impacto: Mapped["NivelImpacto"] = relationship("NivelImpacto", back_populates="tickets")
    plantilla: Mapped["PlantillaFormulario"] = relationship("PlantillaFormulario", back_populates="tickets")


if TYPE_CHECKING:
    from app.models.clientes import Cliente
    from app.models.empleados import Empleado
    from app.models.canales import Canal
    from app.models.estado_ticket import EstadoTicket
    from app.models.tipos_ticket import TipoTicket
    from app.models.niveles_impacto import NivelImpacto
    from app.models.plantilla_formulario import PlantillaFormulario




