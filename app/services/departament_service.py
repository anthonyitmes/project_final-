from sqlalchemy.orm import Session

from app.models.departamentos import Departamento
from app.repositories.departamento_repository import DepartamentoRepository
from app.schemas.departamento_dto import DepartamentoCreateDTO, DepartamentoResponseDTO, DepartamentoUpdateDTO

class DepartamentoService:
    
    def create_departamento(
            self,
            db: Session,
            departamento_in: DepartamentoCreateDTO,
    ) -> DepartamentoResponseDTO:

        departamento_db = Departamento(
            nombre_departamento= departamento_in.nombre_departamento
        )

        departamento_creado = DepartamentoRepository.create_departamento(db, departamento_db)

        return DepartamentoResponseDTO.model_validate(departamento_creado)
    
    # ── READ (uno solo) ─────────────────────────────────────────────
    def get_departamento_by_id(
            self,
            db: Session,
            id_departamento: int,
    ) -> DepartamentoResponseDTO | None:

        departamento = DepartamentoRepository.get_departamento_by_id(db, id_departamento)

        if departamento is None:
            return None
        return DepartamentoResponseDTO.model_validate(departamento)
    
    def get_list_departamentos(
            self,
            db: Session,
    ) -> list[DepartamentoResponseDTO]:

        departamentos = DepartamentoRepository.get_list_departamentos(db)

        return [DepartamentoResponseDTO.model_validate(departamento) for departamento in departamentos]
    
    def update_departamento(
            self,
            db: Session,
            id_departamento: int,
            departamento_in: DepartamentoUpdateDTO,
    ) -> DepartamentoResponseDTO | None:

        departamento_db = DepartamentoRepository.get_departamento_by_id(db, id_departamento)

        if departamento_db is None:
            return None

        # Actualizar los campos del objeto departamento_db con los datos del DTO de entrada
        for field, value in departamento_in.model_dump(exclude_unset=True).items():
            setattr(departamento_db, field, value)

        # Delegar la actualización al repositorio (commit)
        departamento_actualizado = DepartamentoRepository.update_departamento(db, departamento_db)

        return DepartamentoResponseDTO.model_validate(departamento_actualizado)
    
    def delete_departamento(
            self,
            db: Session,
            id_departamento: int,
    ) -> bool:

        departamento_db = DepartamentoRepository.get_departamento_by_id(db, id_departamento)

        if departamento_db is None:
            return False

        DepartamentoRepository.delete_departamento(db, departamento_db)
        return True
    

#instancia
departamento_service = DepartamentoService()