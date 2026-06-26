from typing import Optional

from pydantic import BaseModel


class EstadoTicketCreateDTO(BaseModel):
	nombre_estado: str


class EstadoTicketResponseDTO(BaseModel):
	id_estado: int
	nombre_estado: str

	model_config = {
		"from_attributes": True
	}


class EstadoTicketUpdateDTO(BaseModel):
	nombre_estado: Optional[str] = None