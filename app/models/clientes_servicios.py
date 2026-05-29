from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.clientes import Cliente


class Cliente_servicio(Base):
    

    __tablename__ = "clientes_servicios"

    # PK
    id_cliente_servicio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # FK hacia municipio y cliente (almacenan los ids asociados)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"), nullable=False)
    id_servicio: Mapped[int] = mapped_column(ForeignKey("servicios.id_servicio"), nullable=False)
    
    #Datos adicionales
    fecha_contratacion: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    # Relación 1:N con Direccion
    direcciones: Mapped[list["Direccion"]] = relationship("Direccion", back_populates="cliente")
    cliente: Mapped[list["Cliente"]] = relationship("Cliente", back_populates="clientes_servicios")

if TYPE_CHECKING:
    from app.models.direcciones import Direccion
