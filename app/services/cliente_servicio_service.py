from sqlalchemy.orm import Session

from app.models.clientes_servicios import ClienteServicio
from app.repositories.cliente_servicio_repository import cliente_servicio_repository
from app.schemas.cliente_servicio_dto import ClienteServicioCreateDTO, ClienteServicioResponseDTO, ClienteServicioUpdateDTO

class ClienteServicioService:
    
    def create_cliente_servicio(
            self,
            db: Session,
            cliente_servicio_in: ClienteServicioCreateDTO,
    ) -> ClienteServicioResponseDTO:

        cliente_servicio_db = ClienteServicio(
            id_cliente= cliente_servicio_in.id_cliente,
            id_servicio= cliente_servicio_in.id_servicio,
            fecha_adquisicion= cliente_servicio_in.fecha_adquisicion
        )

        cliente_servicio_creado = cliente_servicio_repository.create_cliente_servicio(db, cliente_servicio_db)

        return ClienteServicioResponseDTO.model_validate(cliente_servicio_creado)
    
    # ── READ (uno solo) ─────────────────────────────────────────────
    def get_cliente_servicio_by_id(
            self,
            db: Session,
            id_cliente_servicio: int,
    ) -> ClienteServicioResponseDTO | None:

        cliente_servicio = cliente_servicio_repository.get_cliente_servicio_by_id(db, id_cliente_servicio)

        if cliente_servicio is None:
            return None
        return ClienteServicioResponseDTO.model_validate(cliente_servicio)
    
    def get_list_clientes_servicios(
            self,
            db: Session,
    ) -> list[ClienteServicioResponseDTO]:

        clientes_servicios = cliente_servicio_repository.get_list_clientes_servicios(db)

        return [ClienteServicioResponseDTO.model_validate(cliente_servicio) for cliente_servicio in clientes_servicios]
    
    def update_cliente_servicio(
            self,
            db: Session,
            id_cliente_servicio: int,
            cliente_servicio_in: ClienteServicioUpdateDTO,
    ) -> ClienteServicioResponseDTO | None:

        cliente_servicio_db = cliente_servicio_repository.get_cliente_servicio_by_id(db, id_cliente_servicio)

        if cliente_servicio_db is None:
            return None

        # Actualizar los campos del objeto cliente_servicio_db con los datos del DTO de entrada
        for field, value in cliente_servicio_in.model_dump(exclude_unset=True).items():
            setattr(cliente_servicio_db, field, value)

        # Guardar los cambios en la base de datos
        cliente_servicio_actualizado = cliente_servicio_repository.update_cliente_servicio(db, cliente_servicio_db)

        return ClienteServicioResponseDTO.model_validate(cliente_servicio_actualizado)
    
    def delete_cliente_servicio(
            self,
            db: Session,
            id_cliente_servicio: int,
    ) -> bool:

        cliente_servicio_db = cliente_servicio_repository.get_cliente_servicio_by_id(db, id_cliente_servicio)

        if cliente_servicio_db is None:
            return False

        cliente_servicio_repository.delete_cliente_servicio(db, cliente_servicio_db)

        return True 

cliente_servicio_service = ClienteServicioService()