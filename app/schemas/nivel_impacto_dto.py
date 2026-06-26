from typing import Optional

from pydantic import BaseModel


class NivelImpactoCreateDTO(BaseModel):
	nombre_impacto: str
	peso_impacto: int


class NivelImpactoResponseDTO(BaseModel):
	id_impacto: int
	nombre_impacto: str
	peso_impacto: int

	model_config = {
		"from_attributes": True
	}


class NivelImpactoUpdateDTO(BaseModel):
	nombre_impacto: Optional[str] = None
	peso_impacto: Optional[int] = None