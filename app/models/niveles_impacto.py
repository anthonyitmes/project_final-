from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class NivelImpacto(Base):
    __tablename__ = "niveles_impacto"

    id_impacto: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_impacto: Mapped[str] = mapped_column(String(100), nullable=False)
    peso_impacto: Mapped[int] = mapped_column(Integer, nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="impacto")


if TYPE_CHECKING:
    from app.models.tickets import Ticket

