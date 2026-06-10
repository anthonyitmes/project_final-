from typing import Any, Dict, Optional

from pydantic import BaseModel


class RolCreateDTO(BaseModel):
	nombre_rol: str
	descripcion_rol: Optional[str] = None


class RolResponseDTO(BaseModel):
	id_rol: int
	nombre_rol: str
	descripcion_rol: Optional[str]

	model_config = {
		"from_attributes": True
	}


class RolUpdateDTO(BaseModel):
	nombre_rol: Optional[str] = None
	descripcion_rol: Optional[str] = None


class CanalCreateDTO(BaseModel):
	nombre_canal: str


class CanalResponseDTO(BaseModel):
	id_canal: int
	nombre_canal: str

	model_config = {
		"from_attributes": True
	}


class CanalUpdateDTO(BaseModel):
	nombre_canal: Optional[str] = None


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
