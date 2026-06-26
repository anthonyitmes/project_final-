from typing import Optional

from pydantic import BaseModel


class DireccionCreateDTO(BaseModel):
	descripcion: str
	calle: str
	zona: str
	avenida: Optional[str] = None
	referencia: Optional[str] = None
	detalles_direccion: str
	id_cliente: int
	id_municipio: int


class DireccionResponseDTO(BaseModel):
	id_direccion: int
	descripcion: str
	calle: str
	zona: str
	avenida: Optional[str]
	referencia: Optional[str]
	detalles_direccion: str
	id_cliente: int
	id_municipio: int

	model_config = {
		"from_attributes": True
	}


class DireccionUpdateDTO(BaseModel):
	descripcion: Optional[str] = None
	calle: Optional[str] = None
	zona: Optional[str] = None
	avenida: Optional[str] = None
	referencia: Optional[str] = None
	detalles_direccion: Optional[str] = None
	id_cliente: Optional[int] = None
	id_municipio: Optional[int] = None