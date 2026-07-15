from sqlalchemy.orm import Session

from app.models.direcciones import Direccion
from app.repositories.direccio_repository import direccion_repository
from app.schemas.direccion_dto import DireccionCreateDTO, DireccionResponseDTO, DireccionUpdateDTO


class DireccionService:

    def create_direccion(
            self,
            db: Session,
            direccion_in: DireccionCreateDTO,
    ) -> DireccionResponseDTO:

        direccion_db = Direccion(
            descripcion=direccion_in.descripcion,
            calle=direccion_in.calle,
            zona=direccion_in.zona,
            avenida=direccion_in.avenida,
            referencia=direccion_in.referencia,
            detalles_direccion=direccion_in.detalles_direccion,
            id_cliente=direccion_in.id_cliente,
            id_municipio=direccion_in.id_municipio,
        )

        direccion_creada = direccion_repository.create_direccion(db, direccion_db)

        return DireccionResponseDTO.model_validate(direccion_creada)

    # ── READ (uno solo) ─────────────────────────────────────────────
    def get_direccion_by_id(
            self,
            db: Session,
            id_direccion: int,
    ) -> DireccionResponseDTO | None:

        direccion = direccion_repository.get_direccion_by_id(db, id_direccion)

        if direccion is None:
            return None
        return DireccionResponseDTO.model_validate(direccion)

    def get_list_direcciones(
            self,
            db: Session,
    ) -> list[DireccionResponseDTO]:

        direcciones = direccion_repository.get_list_direcciones(db)

        return [DireccionResponseDTO.model_validate(direccion) for direccion in direcciones]

    def update_direccion(
            self,
            db: Session,
            id_direccion: int,
            direccion_in: DireccionUpdateDTO,
    ) -> DireccionResponseDTO | None:

        datos = direccion_in.model_dump(exclude_unset=True)
        direccion_actualizada = direccion_repository.update_direccion(db, id_direccion, datos)

        if direccion_actualizada is None:
            return None

        return DireccionResponseDTO.model_validate(direccion_actualizada)

    def delete_direccion(
            self,
            db: Session,
            id_direccion: int,
    ) -> bool:

        return direccion_repository.delete_direccion(db, id_direccion)


direccion_service = DireccionService()