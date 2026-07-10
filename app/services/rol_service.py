from sqlalchemy.orm import Session
from app.models.roles import Rol
from app.repositories.rol_repository import RolRepository
from app.schemas.rol_dto import RolCreateDTO, RolResponseDTO, RolUpdateDTO

class RolService:
    def create_rol(
            self,
            db: Session,
            rol_in: RolCreateDTO,
    ) -> RolResponseDTO:

        rol_db = Rol(
            nombre_rol= rol_in.nombre_rol
        )

        rol_creado = RolRepository.create_rol(db, rol_db)

        return RolResponseDTO.model_validate(rol_creado)
    
    def get_rol_by_id(
            self,
            db: Session,
            id_rol: int,
    ) -> RolResponseDTO | None:

        rol = RolRepository.get_rol_by_id(db, id_rol)

        if rol is None:
            return None
        return RolResponseDTO.model_validate(rol)
    
    def get_list_roles(
            self,
            db: Session,
    ) -> list[RolResponseDTO]:

        roles = RolRepository.get_list_roles(db)

        return [RolResponseDTO.model_validate(rol) for rol in roles]
    
    def update_rol(
            self,
            db: Session,
            id_rol: int,
            rol_in: RolUpdateDTO,
    ) -> RolResponseDTO | None:

        rol_db = RolRepository.get_rol_by_id(db, id_rol)

        if rol_db is None:
            return None

        # Actualizar los campos del objeto rol_db con los datos del DTO de entrada
        for field, value in rol_in.model_dump(exclude_unset=True).items():
            setattr(rol_db, field, value)

    def delete_rol(
            self,
            db: Session,
            id_rol: int,
    ) -> bool:

        rol = RolRepository.get_rol_by_id(db, id_rol)

        if rol is None:
            return False

        return RolRepository.delete_rol(db, id_rol)
    

rol_service = RolService()