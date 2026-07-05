from sqlalchemy.orm import Sesion

from app.models.municipios import Municipio
from app.repositories.municipio_repository import MunicipioRepository
from app.schemas.municipio_dto import MunicipioCreateDTO, MunicipioResponseDTO, MunicipioUpdateDTO

class MunicipioService:
    
    def create_municipio(
            self,
            db: Sesion,
            municipio_in: MunicipioCreateDTO,
    ) -> MunicipioResponseDTO:

        municipio_db = Municipio(
            nombre_municipio= municipio_in.nombre_municipio,
            id_departamento= municipio_in.id_departamento
        )

        municipio_creado = MunicipioRepository.create_municipio(db, municipio_db)

        return MunicipioResponseDTO.model_validate(municipio_creado)
    
    def get_municipio_by_id(
            self,
            db: Sesion,
            id_municipio: int,
    ) -> MunicipioResponseDTO | None:

        municipio = MunicipioRepository.get_municipio_by_id(db, id_municipio)

        if municipio is None:
            return None
        return MunicipioResponseDTO.model_validate(municipio)
    
    def get_list_municipios(
            self,
            db: Sesion,
    ) -> list[MunicipioResponseDTO]:

        municipios = MunicipioRepository.get_list_municipios(db)

        return [MunicipioResponseDTO.model_validate(municipio) for municipio in municipios]
    

    def get_list_by_departamento(
            self,
            db: Sesion,
            id_departamento: int,
    ) -> list[MunicipioResponseDTO]:

        municipios = MunicipioRepository.get_list_by_departamento(db, id_departamento)

        return [MunicipioResponseDTO.model_validate(municipio) for municipio in municipios]
    
    def update_municipio(
            self,
            db: Sesion,
            id_municipio: int,
            municipio_in: MunicipioUpdateDTO,
    ) -> MunicipioResponseDTO | None:

        municipio_db = MunicipioRepository.get_municipio_by_id(db, id_municipio)

        if municipio_db is None:
            return None

        # Actualizar los campos del objeto municipio_db con los datos del DTO de entrada
        for field, value in municipio_in.model_dump(exclude_unset=True).items():
            setattr(municipio_db, field, value)

        updated_municipio = MunicipioRepository.update_municipio(db, id_municipio, municipio_db)

        return MunicipioResponseDTO.model_validate(updated_municipio)
    
    def delete_municipio(
            self,
            db: Sesion,
            id_municipio: int,
    ) -> bool:

        municipio_db = MunicipioRepository.get_municipio_by_id(db, id_municipio)

        if municipio_db is None:
            return False

        MunicipioRepository.delete_municipio(db, municipio_db)
        return True
    
municipio_service = MunicipioService()
