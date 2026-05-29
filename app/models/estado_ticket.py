from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class EstadoTicket(Base):
    __tablename__ = "estado_ticket"

    id_estado: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_estado: Mapped[str] = mapped_column(String(100), nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="estado")


if TYPE_CHECKING:
    from app.models.tickets import Ticket
    