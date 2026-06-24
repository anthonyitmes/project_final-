from datetime import datetime, timezone
from secrets import token_hex

from sqlalchemy.orm import Session

from app.models.tickets import Ticket
from app.repositories.ticket_repository import ticket_repository
from app.schemas.ticket_dto import TicketCreateDTO, TicketResponseDTO, TicketUpdateDTO


class TicketService:

    def _build_ticket_entity(
        self,
        ticket_in: TicketCreateDTO,
        id_receptor: int,
        id_estado: int,
        id_tecnico: int | None,
    ) -> Ticket:
        codigo_ticket = f"TK-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{token_hex(4)}"
        return Ticket(
            codigo_ticket=codigo_ticket,
            id_cliente=ticket_in.id_cliente,
            id_receptor=id_receptor,
            id_tecnico=id_tecnico,
            id_canal=ticket_in.id_canal,
            id_estado=id_estado,
            id_tipo_ticket=ticket_in.id_tipo_ticket,
            id_impacto=ticket_in.id_impacto,
            id_plantilla=ticket_in.id_plantilla,
            titulo=ticket_in.titulo,
            descripcion=ticket_in.descripcion,
            datos_respuesta=ticket_in.respuestas_extra or {},
        )

    def create_ticket(
        self,
        db: Session,
        ticket_in: TicketCreateDTO,
        id_receptor: int,
        id_estado: int,
        id_tecnico: int | None,
    ) -> TicketResponseDTO:
        ticket_db = self._build_ticket_entity(ticket_in, id_receptor, id_estado, id_tecnico)
        ticket_created = ticket_repository.create_ticket(db, ticket_db)
        return TicketResponseDTO.model_validate(ticket_created)

    def get_ticket_by_id(self, db: Session, id_ticket: int) -> TicketResponseDTO | None:
        ticket = ticket_repository.get_ticket_by_id(db, id_ticket)
        if ticket is None:
            return None
        return TicketResponseDTO.model_validate(ticket)

    def get_tickets_by_cliente(self, db: Session, id_cliente: int) -> list[TicketResponseDTO]:
        tickets = ticket_repository.get_list_by_cliente(db, id_cliente)
        return [TicketResponseDTO.model_validate(ticket) for ticket in tickets]

    def update_ticket(
        self,
        db: Session,
        id_ticket: int,
        ticket_update: TicketUpdateDTO,
    ) -> TicketResponseDTO | None:
        ticket = ticket_repository.get_ticket_by_id(db, id_ticket)
        if ticket is None:
            return None

        if ticket_update.id_estado is not None:
            ticket.id_estado = ticket_update.id_estado
        if ticket_update.id_tecnico is not None:
            ticket.id_tecnico = ticket_update.id_tecnico
        if ticket_update.id_impacto is not None:
            ticket.id_impacto = ticket_update.id_impacto

        if ticket_update.titulo is not None:
            ticket.titulo = ticket_update.titulo
        if ticket_update.descripcion is not None:
            ticket.descripcion = ticket_update.descripcion

        db.commit()
        db.refresh(ticket)
        return TicketResponseDTO.model_validate(ticket)


ticket_service = TicketService()