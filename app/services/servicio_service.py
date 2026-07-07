from sqlalchemy.orm import Session

from app.models.servicios import Servicio
from app.repositories.servicio_repository import ServicioRepository
from app.schemas.servicio_dto import ServicioCreateDTO, ServicioResponseDTO, ServicioUpdateDTO


class ServicioService:
    def create_servicio(
            self,
            db: Session,
            servicio_in: ServicioCreateDTO,
    ) -> ServicioResponseDTO:

        servicio_db = Servicio(
            nombre_servicio=servicio_in.nombre_servicio,
            descripcion=servicio_in.descripcion
        )

        servicio_creado = ServicioRepository.create_servicio(db, servicio_db)

        return ServicioResponseDTO.model_validate(servicio_creado)
    
    def get_servicio_by_id(
            self,
            db: Session,
            id_servicio: int,
    ) -> ServicioResponseDTO | None:

        servicio = ServicioRepository.get_servicio_by_id(db, id_servicio)

        if servicio is None:
            return None
        return ServicioResponseDTO.model_validate(servicio)
    

    def get_list_servicios(
            self,
            db: Session,
    ) -> list[ServicioResponseDTO]:

        servicios = ServicioRepository.get_list_servicios(db)

        return [ServicioResponseDTO.model_validate(servicio) for servicio in servicios]
    
    def update_servicio(
            self,
            db: Session,
            id_servicio: int,
            servicio_in: ServicioUpdateDTO,
    ) -> ServicioResponseDTO | None:

        servicio_db = ServicioRepository.get_servicio_by_id(db, id_servicio)

        if servicio_db is None:
            return None

        # Actualizar los campos del objeto servicio_db con los datos del DTO de entrada
        for field, value in servicio_in.model_dump(exclude_unset=True).items():
            setattr(servicio_db, field, value)

        servicio_actualizado = ServicioRepository.update_servicio(db, servicio_db)

        return ServicioResponseDTO.model_validate(servicio_actualizado)
    
    def delete_servicio(
            self,
            db: Session,
            id_servicio: int,
    ) -> bool:

        servicio_db = ServicioRepository.get_servicio_by_id(db, id_servicio)

        if servicio_db is None:
            return False

        ServicioRepository.delete_servicio(db, servicio_db)
        return True

servicio_service = ServicioService()