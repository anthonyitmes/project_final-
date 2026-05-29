from sqlalchemy import Integer, String, JSONB, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class PlantillaFormulario(Base):
    __tablename__ = "plantilla_formulario"

    id_plantilla: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_plantilla: Mapped[str] = mapped_column(String(100), nullable=False)
    estructura: Mapped[dict] = mapped_column(JSONB, nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, nullable=False)
    