"""
Ticket Router — Endpoints HTTP para la entidad Ticket.

Flujo: Cliente -> Router -> Service -> Repository -> BD
El router solo maneja HTTP: recibe requests, delega al Service, responde.
"""

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


# GET /tickets — Listado paginado con filtros (Fase 4.3)
@router.get("", response_model=list[TicketResponseDTO])
def get_all_tickets(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Maximo de registros"),
    id_estado: int | None = Query(None, description="Filtrar por ID de estado"),
    id_tecnico: int | None = Query(None, description="Filtrar por ID de tecnico"),
    id_cliente: int | None = Query(None, description="Filtrar por ID de cliente"),
    db: Session = Depends(get_db),
) -> list[TicketResponseDTO]:
    """Lista tickets con paginacion y filtros opcionales."""
    return ticket_service.get_all_tickets(
        db,
        skip=skip,
        limit=limit,
        id_estado=id_estado,
        id_tecnico=id_tecnico,
        id_cliente=id_cliente,
    )


# DELETE /tickets/{id_ticket} — Eliminar un ticket (Fase 4.3)
@router.delete("/{id_ticket}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    id_ticket: int,
    db: Session = Depends(get_db),
) -> None:
    """Elimina un ticket. Retorna 204 si se elimino, 404 si no existe."""
    eliminado = ticket_service.delete_ticket(db, id_ticket)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket no encontrado",
        )