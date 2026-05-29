from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Canal(Base):
    __tablename__ = "canales"

    id_canal: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_canal: Mapped[str] = mapped_column(String(100), nullable=False)
    