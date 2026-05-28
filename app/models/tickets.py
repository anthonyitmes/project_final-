from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id_ticket: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo_ticket: Mapped[int] = mapped_column(Integer, nullable=False)
    id_cliente: Mapped[str] = mapped_column(String(100), nullable=False)
    id_receptor: Mapped[str] = mapped_column(String(100), nullable=False)
    id_tecnico: Mapped[str] = mapped_column(String(50), nullable=False)
    id_canal: Mapped[str] = mapped_column(String(100), nullable=False)
    id_estado: Mapped[str] = mapped_column(String(100), nullable=False)
    id_impacto: Mapped[str] = mapped_column(String(100), nullable=False)
    id_plantilla: Mapped[str] = mapped_column(String(100), nullable=False)
    datos_respuestas: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_creacion: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_resolucion: Mapped[str] = mapped_column(String(100), nullable=False)





