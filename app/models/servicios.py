from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Servicio(Base):
    __tablename__ = "servicios"

    id_servicio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_servicio: Mapped[str] = mapped_column(String(100), nullable=False)
    