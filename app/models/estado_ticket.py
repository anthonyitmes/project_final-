from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Estados_tickets(Base):
    __tablename__ = "estado_ticket"

    id_estado_ticket: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_estado: Mapped[str] = mapped_column(String(100), nullable=False)
    