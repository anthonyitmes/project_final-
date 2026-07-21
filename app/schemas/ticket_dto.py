from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


# FIX: nombre de clase corregido (antes "echTicketCreateDTO")
class TicketCreateDTO(BaseModel):
    id_cliente: int
    id_canal: int
    id_tipo_ticket: int
    id_impacto: int
    id_plantilla: int

    respuestas_extra: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TicketUpdateDTO(BaseModel):
    id_estado: Optional[int] = None
    id_tecnico: Optional[int] = None
    id_impacto: Optional[int] = None


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

    datos_respuesta: Dict[str, Any]

    fecha_creacion: datetime
    fecha_resolucion: Optional[datetime]

    class Config:
        from_attributes = True
