from sqlalchemy.orm import Session
from app.models.roles import Rol
from app.repositories.rol_repository import rol_repository
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

        rol_creado = rol_repository.create_rol(db, rol_db)

        return RolResponseDTO.model_validate(rol_creado)
    
    def get_rol_by_id(
            self,
            db: Session,
            id_rol: int,
    ) -> RolResponseDTO | None:

        rol = rol_repository.get_rol_by_id(db, id_rol)

        if rol is None:
            return None
        return RolResponseDTO.model_validate(rol)
    
    def get_list_roles(
            self,
            db: Session,
    ) -> list[RolResponseDTO]:

        roles = rol_repository.get_list_roles(db)

        return [RolResponseDTO.model_validate(rol) for rol in roles]
    
    def update_rol(
            self,
            db: Session,
            id_rol: int,
            rol_in: RolUpdateDTO,
    ) -> RolResponseDTO | None:

        datos = rol_in.model_dump(exclude_unset=True)
        if not datos:
            rol = rol_repository.get_rol_by_id(db, id_rol)
            if rol is None:
                return None
            return RolResponseDTO.model_validate(rol)

        rol_actualizado = rol_repository.update_rol(db, id_rol, datos)
        if rol_actualizado is None:
            return None

        return RolResponseDTO.model_validate(rol_actualizado)

    def delete_rol(
            self,
            db: Session,
            id_rol: int,
    ) -> bool:

        return rol_repository.delete_rol(db, id_rol)
    

rol_service = RolService()