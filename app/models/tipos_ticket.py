from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class NivelImpacto(Base):
    __tablename__ = "niveles_impacto"

    id_nivel_impacto: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_impacto: Mapped[str] = mapped_column(String(100), nullable=False)
    