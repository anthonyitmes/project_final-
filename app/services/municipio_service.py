# FIX: Sesion -> Session (typo que causaba ImportError)
from sqlalchemy.orm import Session

from app.models.municipios import Municipio
from app.repositories.municipio_repository import municipio_repository
from app.schemas.municipio_dto import MunicipioCreateDTO, MunicipioResponseDTO, MunicipioUpdateDTO

class MunicipioService:
    
    def create_municipio(
            self,
        db: Session,
        municipio_in: MunicipioCreateDTO,
    ) -> MunicipioResponseDTO:

        municipio_db = Municipio(
            nombre_municipio= municipio_in.nombre_municipio,
            id_departamento= municipio_in.id_departamento
        )

        municipio_creado = municipio_repository.create_municipio(db, municipio_db)

        return MunicipioResponseDTO.model_validate(municipio_creado)
    
    def get_municipio_by_id(
            self,
        db: Session,
        id_municipio: int,
    ) -> MunicipioResponseDTO | None:

        municipio = municipio_repository.get_municipio_by_id(db, id_municipio)

        if municipio is None:
            return None
        return MunicipioResponseDTO.model_validate(municipio)
    
    def get_list_municipios(
            self,
            db: Session,
    ) -> list[MunicipioResponseDTO]:

        municipios = municipio_repository.get_list_municipios(db)

        return [MunicipioResponseDTO.model_validate(municipio) for municipio in municipios]
    

    def get_list_by_departamento(
            self,
        db: Session,
        id_departamento: int,
    ) -> list[MunicipioResponseDTO]:

        municipios = municipio_repository.get_list_by_departamento(db, id_departamento)

        return [MunicipioResponseDTO.model_validate(municipio) for municipio in municipios]
    
    def update_municipio(
            self,
        db: Session,
        id_municipio: int,
        municipio_in: MunicipioUpdateDTO,
    ) -> MunicipioResponseDTO | None:

        municipio_db = municipio_repository.get_municipio_by_id(db, id_municipio)

        if municipio_db is None:
            return None

        # Actualizar los campos del objeto municipio_db con los datos del DTO de entrada
        datos = municipio_in.model_dump(exclude_unset=True)
        if not datos:
            return MunicipioResponseDTO.model_validate(municipio_db)

        municipio_actualizado = municipio_repository.update_municipio(db, id_municipio, datos)
        if municipio_actualizado is None:
            return None

        return MunicipioResponseDTO.model_validate(municipio_actualizado)
    
    def delete_municipio(
            self,
        db: Session,
        id_municipio: int,
    ) -> bool:

        return municipio_repository.delete_municipio(db, id_municipio)
    
municipio_service = MunicipioService()
