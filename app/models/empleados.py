from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    Id_ticket: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    Codigo_ticket: Mapped[int] = mapped_column(Integer, foreign_key="tickets.Id_ticket"), nullable=False)
    Id_cliente: Mapped[str] = mapped_column(String(100), nullable=False)
    Id_receptor: Mapped[str] = mapped_column(String(100), nullable=False)
    Id_tecnico: Mapped[str] = mapped_column(String(50), nullable=False)
    Id_canal: Mapped[str] = mapped_column(String(100), nullable=False)
    Id_estado: Mapped[str] = mapped_column(String(100), nullable=False)
    Id_impacto: Mapped[str] = mapped_column(String(100), nullable=False)
    Id_plantilla: Mapped[str] = mapped_column(String(100), nullable=False)
    Datos_respuestas: Mapped[str] = mapped_column(String(100), nullable=False)
    Fecha_creacion: Mapped[str] = mapped_column(String(100), nullable=False)
    Fecha_Resolucion: Mapped[str] = mapped_column(String(100), nullable=False)





