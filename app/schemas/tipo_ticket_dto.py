from typing import Optional

from pydantic import BaseModel


class TipoTicketCreateDTO(BaseModel):
	nombre_tipo_ticket: str


class TipoTicketResponseDTO(BaseModel):
	id_tipo_ticket: int
	nombre_tipo_ticket: str

	model_config = {
		"from_attributes": True
	}


class TipoTicketUpdateDTO(BaseModel):
	nombre_tipo_ticket: Optional[str] = None