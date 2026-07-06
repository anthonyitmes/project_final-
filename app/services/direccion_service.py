from sqlalchemy.orm import Session

from app.models.direcciones import Direccion
from app.repositories.direccio_repository import DireccionRepository
from app.schemas.direccion_dto import DireccionCreateDTO, DireccionResponseDTO, DireccionUpdateDTO

class DireccionService:
    
    def create_direccion(
            self,
            db: Session,
            direccion_in: DireccionCreateDTO,
    ) -> DireccionResponseDTO:

        direccion_db = Direccion(
            nombre_direccion= direccion_in.descripcion
        )

        direccion_creado = DireccionRepository.create_direccion(db, direccion_db)

        return DireccionResponseDTO.model_validate(direccion_creado)
    
    # ── READ (uno solo) ─────────────────────────────────────────────
    def get_direccion_by_id(
            self,
            db: Session,
            id_direccion: int,
    ) -> DireccionResponseDTO | None:

        direccion = DireccionRepository.get_direccion_by_id(db, id_direccion)

        if direccion is None:
            return None
        return DireccionResponseDTO.model_validate(direccion)
    
    def get_list_direcciones(
            self,
            db: Session,
    ) -> list[DireccionResponseDTO]:

        direcciones = DireccionRepository.get_list_direcciones(db)

        return [DireccionResponseDTO.model_validate(direccion) for direccion in direcciones]
    
    def update_direccion(
            self,
            db: Session,
            id_direccion: int,
            direccion_in: DireccionUpdateDTO,
    ) -> DireccionResponseDTO | None:

        direccion_db = DireccionRepository.get_direccion_by_id(db, id_direccion)

        if direccion_db is None:
            return None

        # Actualizar los campos del objeto direccion_db con los datos del DTO de entrada
        for field, value in direccion_in.model_dump(exclude_unset=True).items():
            setattr(direccion_db, field, value)


    def delete_direccion(
            self,
            db: Session,
            id_direccion: int,
    ) -> bool:

        direccion_db = DireccionRepository.get_direccion_by_id(db, id_direccion)

        if direccion_db is None:
            return False

        DireccionRepository.delete_direccion(db, direccion_db)
        return True
    
direccion_service = DireccionService()
