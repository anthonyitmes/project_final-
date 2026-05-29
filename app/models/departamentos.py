from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Departamento(Base):
    """Modelo para la tabla 'departamentos'. Representa un departamento/provincia."""

    # nombre de la tabla en la base de datos (recomendado en minúsculas)
    __tablename__ = "departamentos"

    # PK: identificador del departamento
    id_departamento: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Nombre del departamento (no nulo, hasta 100 caracteres)
    nombre_departamento: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    municipios: Mapped[list["Municipio"]] = relationship("Municipio", back_populates="departamento")


if TYPE_CHECKING:
    # Import sólo para el chequeo de tipos y evitar imports circulares en tiempo de ejecución
    from app.models.municipios import Municipio
