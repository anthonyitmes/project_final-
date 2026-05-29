from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class PlantillaFormulario(Base):
    __tablename__ = "plantilla_formulario"

    id_plantilla: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_plantilla: Mapped[str] = mapped_column(String(100), nullable=False)
    estructura_preguntas: Mapped[dict] = mapped_column(JSONB, nullable=False)
    estado_plantilla: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="plantilla")


if TYPE_CHECKING:
    from app.models.tickets import Ticket
    