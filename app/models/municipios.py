from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Municipio(Base):
    """Modelo para la tabla 'municipios'. Representa un municipio/ciudad."""

    # nombre de la tabla en la base de datos (recomendado en minúsculas)
    __tablename__ = "municipios"

    # PK: identificador del municipio
    id_municipio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Nombre del municipio (no nulo)
    nombre_municipio: Mapped[str] = mapped_column(String(100), nullable=False)



    # FK hacia departamentos.id_departamento (columna que almacena la relación)
    id_departamento: Mapped[int] = mapped_column(ForeignKey("departamentos.id_departamento"), nullable=False)
  
    # Relación inversa (many -> one). 'back_populates' enlaza con 'municipios' en Departamento.
    departamento: Mapped["Departamento"] = relationship("Departamento", back_populates="municipios")
    
    
    # Relación 1:N con Dirección. Un municipio puede tener muchas direcciones.
    direcciones: Mapped[list["Direccion"]] = relationship("Direccion", back_populates="municipio")


if TYPE_CHECKING:
    # Import sólo para chequeo de tipos y evitar imports circulares en tiempo de ejecución
    from app.models.departamentos import Departamento
    from app.models.direcciones import Direccion
