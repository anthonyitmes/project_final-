from typing import Optional

from pydantic import BaseModel


class DepartamentoCreateDTO(BaseModel):
	nombre_departamento: str


class DepartamentoResponseDTO(BaseModel):
	id_departamento: int
	nombre_departamento: str

	model_config = {
		"from_attributes": True
	}


class DepartamentoUpdateDTO(BaseModel):
	nombre_departamento: Optional[str] = None