from sqlalchemy.orm import Session

from app.models.empleados import Empleado
from app.repositories.empleado_repository import empleado_repository
from app.schemas.empleado_dto import EmpleadoCreateDTO, EmpleadoResponseDTO, EmpleadoUpdateDTO

class EmpleadoService:
    def create_empleado(
            self,
            db: Session,
            empleado_in: EmpleadoCreateDTO,
    ) -> EmpleadoResponseDTO:

        empleado_db = Empleado(
            nombre_empleado= empleado_in.nombre_empleado,
            email= empleado_in.email,
            password_bash= empleado_in.password_bash,
            activo= empleado_in.activo,
            id_rol= empleado_in.id_rol,
        )

        empleado_creado = empleado_repository.create_empleado(db, empleado_db)

        return EmpleadoResponseDTO.model_validate(empleado_creado)

    def get_empleado_by_id(
            self,
            db: Session,
            id_empleado: int,
    ) -> EmpleadoResponseDTO | None:

        empleado = empleado_repository.get_empleado_by_id(db, id_empleado)

        if empleado is None:
            return None
        return EmpleadoResponseDTO.model_validate(empleado)
    
    def get_list_empleados(
            self,
            db: Session,
    ) -> list[EmpleadoResponseDTO]:

        empleados = empleado_repository.get_list_empleados(db)

        return [EmpleadoResponseDTO.model_validate(empleado) for empleado in empleados]
    
    def update_empleado(
            self,
            db: Session,
            id_empleado: int,
            empleado_in: EmpleadoUpdateDTO,
    ) -> EmpleadoResponseDTO | None:

        datos = empleado_in.model_dump(exclude_unset=True)
        if not datos:
            empleado = empleado_repository.get_empleado_by_id(db, id_empleado)
            if empleado is None:
                return None
            return EmpleadoResponseDTO.model_validate(empleado)

        empleado_actualizado = empleado_repository.update_empleado(db, id_empleado, datos)
        if empleado_actualizado is None:
            return None

        return EmpleadoResponseDTO.model_validate(empleado_actualizado)

    def delete_empleado(
            self,
            db: Session,
            id_empleado: int,
    ) -> bool:

        return empleado_repository.delete_empleado(db, id_empleado)
    
empleado_service = EmpleadoService()