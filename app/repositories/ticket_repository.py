"""
Ticket Repository — Capa de acceso a datos para la entidad Ticket.

Responsabilidad exclusiva: operaciones CRUD directas sobre la tabla `tickets`
usando SQLAlchemy Session. Esta capa NO contiene reglas de negocio,
validaciones ni transformaciones DTO. Solo queries y persistencia.

Flujo: Router → Service → Repository → Base de datos
"""

from sqlalchemy.orm import Session
from app.models.tickets import Ticket

class TicketRepository:

    def create_ticket(self, db: Session, ticket_db: Ticket) -> Ticket:
        """Inserta un ticket (ya armado por el Service) y lo persiste."""
        db.add(ticket_db)
        db.commit()
        db.refresh(ticket_db)
        return ticket_db
    
    def get_ticket_by_id(self, db: Session, id_ticket: int) -> Ticket | None: 
        """Busca un ticket por ID. Retorna None si no existe."""
        return db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()
    
    def get_tickets_by_cliente(self, db: Session, id_cliente: int) -> list[Ticket]:
        """Lista todos los tickets asociados a un cliente específico."""
        return db.query(Ticket).filter(Ticket.id_cliente == id_cliente).all()

    def get_all_tickets(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 50,
        id_estado: int | None = None,
        id_tecnico: int | None = None,
        id_cliente: int | None = None,
    ) -> list[Ticket]:
        """Listado paginado de tickets con filtros opcionales."""
        query = db.query(Ticket)
        if id_estado is not None:
            query = query.filter(Ticket.id_estado == id_estado)
        if id_tecnico is not None:
            query = query.filter(Ticket.id_tecnico == id_tecnico)
        if id_cliente is not None:
            query = query.filter(Ticket.id_cliente == id_cliente)
        return query.offset(skip).limit(limit).all()

    def update_ticket(self, db: Session, id_ticket: int, datos: dict) -> Ticket | None:
        """Actualiza campos de un ticket. Recibe dict {campo: valor}."""
        ticket = db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()
        if ticket is None:
            return None
        for key, value in datos.items():
            if value is not None and hasattr(ticket, key):
                setattr(ticket, key, value)
        db.commit()
        db.refresh(ticket)
        return ticket

    def delete_ticket(self, db: Session, id_ticket: int) -> bool:
        """Elimina físicamente un ticket. Retorna True/False."""
        ticket = db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()
        if ticket is None:
            return False
        db.delete(ticket)
        db.commit()
        return True

# Instancia singleton — usada por el Service.
# TODO: migrar a inyección de dependencias (Depends) para facilitar testing.
ticket_repository = TicketRepository()