from sqlalchemy.orm import  Session

from app.models.estado_ticket import EstadoTicket
from app.repositories.estado_ticket_repository import estado_ticket_repository
from app.schemas.estado_ticket_dto import EstadoTicketCreateDTO, EstadoTicketResponseDTO, EstadoTicketUpdateDTO

class EstadoTicketService:
    def create_estado_ticket(
            self,
            db: Session,
            estado_ticket_in: EstadoTicketCreateDTO,
    ) -> EstadoTicketResponseDTO:

        estado_ticket_db = EstadoTicket(
            nombre_estado= estado_ticket_in.nombre_estado
        )

        estado_ticket_creado = estado_ticket_repository.create_estado_ticket(db, estado_ticket_db)

        return EstadoTicketResponseDTO.model_validate(estado_ticket_creado)
    
    def get_estado_ticket_by_id(
            self,
            db: Session,
            id_estado_ticket: int,
    ) -> EstadoTicketResponseDTO | None:

        estado_ticket = estado_ticket_repository.get_estado_ticket_by_id(db, id_estado_ticket)

        if estado_ticket is None:
            return None
        return EstadoTicketResponseDTO.model_validate(estado_ticket)
    def get_list_estado_tickets(
            self,
            db: Session,
    ) -> list[EstadoTicketResponseDTO]:

        estado_tickets = estado_ticket_repository.get_list_estados_ticket(db)

        return [EstadoTicketResponseDTO.model_validate(estado_ticket) for estado_ticket in estado_tickets]
    
    def update_estado_ticket(
            self,
            db: Session,
            id_estado_ticket: int,
            estado_ticket_in: EstadoTicketUpdateDTO,
    ) -> EstadoTicketResponseDTO | None:

        datos = estado_ticket_in.model_dump(exclude_unset=True)
        if not datos:
            estado_ticket = estado_ticket_repository.get_estado_ticket_by_id(db, id_estado_ticket)
            if estado_ticket is None:
                return None
            return EstadoTicketResponseDTO.model_validate(estado_ticket)

        estado_ticket_actualizado = estado_ticket_repository.update_estado_ticket(db, id_estado_ticket, datos)
        if estado_ticket_actualizado is None:
            return None

        return EstadoTicketResponseDTO.model_validate(estado_ticket_actualizado)
    
    def delete_estado_ticket(
            self,
            db: Session,
            id_estado_ticket: int,
    ) -> bool:

        estado_ticket_db = estado_ticket_repository.get_estado_ticket_by_id(db, id_estado_ticket)

        if estado_ticket_db is None:
            return False

        return estado_ticket_repository.delete_estado_ticket(db, id_estado_ticket)

estado_ticket_service = EstadoTicketService()
