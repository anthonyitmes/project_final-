from typing import Optional

from pydantic import BaseModel


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