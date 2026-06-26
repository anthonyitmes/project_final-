from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ClienteServicioCreateDTO(BaseModel):
	id_cliente: int
	id_servicio: int
	fecha_adquisicion: datetime


class ClienteServicioResponseDTO(BaseModel):
	id_cliente_servicio: int
	id_cliente: int
	id_servicio: int
	fecha_adquisicion: datetime

	model_config = {
		"from_attributes": True
	}


class ClienteServicioUpdateDTO(BaseModel):
	id_cliente: Optional[int] = None
	id_servicio: Optional[int] = None
	fecha_adquisicion: Optional[datetime] = None