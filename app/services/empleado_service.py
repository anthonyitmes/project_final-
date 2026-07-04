from sqlalchemy.orm import Session

from app.models.empleados import Empleado
from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.empleado_dto import EmpleadoCreateDTO, EmpleadoResponseDTO, EmpleadoUpdateDTO

class EmpleadoService:
    def create_empleado(
            self,
            db: Session,
            empleado_in: EmpleadoCreateDTO,
    ) -> EmpleadoResponseDTO:

        empleado_db = Empleado(
            nombre_empleado= empleado_in.nombre_empleado
        )

        empleado_creado = EmpleadoRepository.create_empleado(db, empleado_db)

        return EmpleadoResponseDTO.model_validate(empleado_creado)

    def get_empleado_by_id(
            self,
            db: Session,
            id_empleado: int,
    ) -> EmpleadoResponseDTO | None:

        empleado = EmpleadoRepository.get_empleado_by_id(db, id_empleado)

        if empleado is None:
            return None
        return EmpleadoResponseDTO.model_validate(empleado)
    
    def get_list_empleados(
            self,
            db: Session,
    ) -> list[EmpleadoResponseDTO]:

        empleados = EmpleadoRepository.get_list_empleados(db)

        return [EmpleadoResponseDTO.model_validate(empleado) for empleado in empleados]
    
    def update_empleado(
            self,
            db: Session,
            id_empleado: int,
            empleado_in: EmpleadoUpdateDTO,
    ) -> EmpleadoResponseDTO | None:

        empleado_db = EmpleadoRepository.get_empleado_by_id(db, id_empleado)

        if empleado_db is None:
            return None

        # Actualizar los campos del objeto empleado_db con los datos del DTO de entrada
        for field, value in empleado_in.model_dump(exclude_unset=True).items():
            setattr(empleado_db, field, value)

        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(empleado_db)

        return EmpleadoResponseDTO.model_validate(empleado_db)
    def delete_empleado(
            self,
            db: Session,
            id_empleado: int,
    ) -> bool:

        empleado_db = EmpleadoRepository.get_empleado_by_id(db, id_empleado)

        if empleado_db is None:
            return False

        EmpleadoRepository.delete_empleado(db, empleado_db)
        return True
    
empleado_service = EmpleadoService()