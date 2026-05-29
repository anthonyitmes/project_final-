from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Servicio(Base):
    __tablename__ = "servicios"

    id_servicio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_servicio: Mapped[str] = mapped_column(String(100), nullable=False)

    clientes_servicios: Mapped[list["ClienteServicio"]] = relationship(
        "ClienteServicio",
        back_populates="servicio",
    )


if TYPE_CHECKING:
    from app.models.clientes_servicios import ClienteServicio
    