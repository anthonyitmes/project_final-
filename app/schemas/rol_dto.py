from typing import Optional

from pydantic import BaseModel


class RolCreateDTO(BaseModel):
	nombre_rol: str
	descripcion: Optional[str] = None


class RolResponseDTO(BaseModel):
	id_rol: int
	nombre_rol: str
	descripcion: Optional[str]

	model_config = {
		"from_attributes": True
	}


class RolUpdateDTO(BaseModel):
	nombre_rol: Optional[str] = None
	descripcion: Optional[str] = None
