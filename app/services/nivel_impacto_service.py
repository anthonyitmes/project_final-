from sqlalchemy.orm import Session

from app.models.niveles_impacto import NivelImpacto
from app.repositories.nivel_impacto_repository import NivelImpactoRepository
from app.schemas.nivel_impacto_dto import NivelImpactoCreateDTO, NivelImpactoResponseDTO, NivelImpactoUpdateDTO


class NivelImpactoService:

    def create_nivel_impacto(
            self,
            db: Session,
            nivel_impacto_in: NivelImpactoCreateDTO,
    ) -> NivelImpactoResponseDTO:

        nivel_impacto_db = NivelImpacto(
            nombre_impacto=nivel_impacto_in.nombre_impacto,
            peso_impacto=nivel_impacto_in.peso_impacto,
        )

        nivel_impacto_creado = NivelImpactoRepository.create_nivel_impacto(db, nivel_impacto_db)

        return NivelImpactoResponseDTO.model_validate(nivel_impacto_creado)

    def get_nivel_impacto_by_id(
            self,
            db: Session,
            id_nivel_impacto: int,
    ) -> NivelImpactoResponseDTO | None:

        nivel_impacto = NivelImpactoRepository.get_nivel_impacto_by_id(db, id_nivel_impacto)

        if nivel_impacto is None:
            return None
        return NivelImpactoResponseDTO.model_validate(nivel_impacto)

    def get_list_niveles_impacto(
            self,
            db: Session,
    ) -> list[NivelImpactoResponseDTO]:

        niveles_impacto = NivelImpactoRepository.get_list_niveles_impacto(db)

        return [NivelImpactoResponseDTO.model_validate(nivel_impacto) for nivel_impacto in niveles_impacto]

    def update_nivel_impacto(
            self,
            db: Session,
            id_nivel_impacto: int,
            nivel_impacto_in: NivelImpactoUpdateDTO,
    ) -> NivelImpactoResponseDTO | None:

        datos = nivel_impacto_in.model_dump(exclude_unset=True)
        if not datos:
            nivel_impacto = NivelImpactoRepository.get_nivel_impacto_by_id(db, id_nivel_impacto)
            return NivelImpactoResponseDTO.model_validate(nivel_impacto) if nivel_impacto else None

        nivel_impacto_actualizado = NivelImpactoRepository.update_nivel_impacto(db, id_nivel_impacto, datos)

        if nivel_impacto_actualizado is None:
            return None

        return NivelImpactoResponseDTO.model_validate(nivel_impacto_actualizado)

    def delete_nivel_impacto(
            self,
            db: Session,
            id_nivel_impacto: int,
    ) -> bool:

        return NivelImpactoRepository.delete_nivel_impacto(db, id_nivel_impacto)


nivel_impacto_service = NivelImpactoService()
