<<<<<<< HEAD
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TicketCreateDTO(BaseModel):
    id_cliente: int
    id_canal: int
    id_tipo_ticket: int
    id_impacto: int
    id_plantilla: int

    titulo: str = Field(..., max_length=150, description="Asunto principal")
    descripcion: str = Field(..., description="Detalle del problema")
    respuestas_extra: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TicketUpdateDTO(BaseModel):
    id_estado: Optional[int] = None
    id_tecnico: Optional[int] = None
    id_impacto: Optional[int] = None
    titulo: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None


class TicketResponseDTO(BaseModel):
    id_ticket: int
    codigo_ticket: str

    id_cliente: int
    id_receptor: int
    id_tecnico: Optional[int]
    id_canal: int
    id_estado: int
    id_tipo_ticket: int
    id_impacto: int
    id_plantilla: int

    titulo: str
    descripcion: str
    datos_respuesta: Dict[str, Any]

    fecha_creacion: datetime
    fecha_resolucion: Optional[datetime]

    class Config:
        from_attributes = True
=======
>>>>>>> 3a1cf6837dd5ebc307a324bb8a6dbd29a6f8492d
