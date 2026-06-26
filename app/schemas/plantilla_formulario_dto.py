from typing import Any, Dict, Optional

from pydantic import BaseModel


class PlantillaFormularioCreateDTO(BaseModel):
	nombre_plantilla: str
	estructura_preguntas: Dict[str, Any]
	estado_plantilla: bool = True


class PlantillaFormularioResponseDTO(BaseModel):
	id_plantilla: int
	nombre_plantilla: str
	estructura_preguntas: Dict[str, Any]
	estado_plantilla: bool

	model_config = {
		"from_attributes": True
	}


class PlantillaFormularioUpdateDTO(BaseModel):
	nombre_plantilla: Optional[str] = None
	estructura_preguntas: Optional[Dict[str, Any]] = None
	estado_plantilla: Optional[bool] = None