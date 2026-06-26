from typing import Optional

from pydantic import BaseModel


class MunicipioCreateDTO(BaseModel):
	nombre_municipio: str
	id_departamento: int


class MunicipioResponseDTO(BaseModel):
	id_municipio: int
	nombre_municipio: str
	id_departamento: int

	model_config = {
		"from_attributes": True
	}


class MunicipioUpdateDTO(BaseModel):
	nombre_municipio: Optional[str] = None
	id_departamento: Optional[int] = None