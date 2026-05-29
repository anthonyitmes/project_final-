from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class TipoTicket(Base):
    __tablename__ = "tipos_ticket"

    id_tipo_ticket: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_tipo_ticket: Mapped[str] = mapped_column(String(100), nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="tipo_ticket")


if TYPE_CHECKING:
    from app.models.tickets import Ticket
    