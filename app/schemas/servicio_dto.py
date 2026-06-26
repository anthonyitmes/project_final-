from typing import Optional

from pydantic import BaseModel


class ServicioCreateDTO(BaseModel):
	nombre_servicio: str


class ServicioResponseDTO(BaseModel):
	id_servicio: int
	nombre_servicio: str

	model_config = {
		"from_attributes": True
	}


class ServicioUpdateDTO(BaseModel):
	nombre_servicio: Optional[str] = None