from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.ticket_dto import TicketCreateDTO, TicketResponseDTO, TicketUpdateDTO
from app.services.ticket_service import ticket_service


router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("", response_model=TicketResponseDTO, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_in: TicketCreateDTO,
    id_receptor: int = Query(..., description="ID del empleado que recibe el ticket"),
    id_estado: int = Query(..., description="ID del estado inicial del ticket"),
    id_tecnico: int | None = Query(None, description="ID del técnico asignado, si aplica"),
    db: Session = Depends(get_db),
) -> TicketResponseDTO:
    return ticket_service.create_ticket(db, ticket_in, id_receptor, id_estado, id_tecnico)


@router.get("/{id_ticket}", response_model=TicketResponseDTO)
def get_ticket_by_id(id_ticket: int, db: Session = Depends(get_db)) -> TicketResponseDTO:
    ticket = ticket_service.get_ticket_by_id(db, id_ticket)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
    return ticket


@router.get("/cliente/{id_cliente}", response_model=list[TicketResponseDTO])
def get_tickets_by_cliente(id_cliente: int, db: Session = Depends(get_db)) -> list[TicketResponseDTO]:
    return ticket_service.get_tickets_by_cliente(db, id_cliente)


@router.patch("/{id_ticket}", response_model=TicketResponseDTO)
def update_ticket(
    id_ticket: int,
    ticket_update: TicketUpdateDTO,
    db: Session = Depends(get_db),
) -> TicketResponseDTO:
    ticket = ticket_service.update_ticket(db, id_ticket, ticket_update)
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
    return ticket