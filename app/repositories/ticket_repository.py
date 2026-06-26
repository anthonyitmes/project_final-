from sqlalchemy.orm import Session
from app.models.tickets import Ticket

class TicketRepository:

    def create_ticket(self, db: Session, ticket_db: Ticket) -> Ticket:
        # Recibe un modelo ticket ya armado y lo inserta en PostgreSQL
        db.add(ticket_db)
        db.commit()
        db.refresh(ticket_db)
        return ticket_db
    
    def get_ticket_by_id(self, db: Session, id_ticket: int) -> Ticket | None: 
        # Busca un ticket por su id
        return db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()
    
    def get_list_by_cliente(self, db: Session, id_cliente: int) -> list[Ticket]:
        # Busca los tickets de un cliente
        return db.query(Ticket).filter(Ticket.id_cliente == id_cliente).all()

    def get_all_tickets(self, db: Session) -> list[Ticket]:
        # Lista todos los tickets
        return db.query(Ticket).all()

    def update_ticket(self, db: Session, id_ticket: int, ticket_update: Ticket) -> Ticket | None:
        # Actualiza un ticket existente en la base de datos
        ticket = db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()
        if ticket is None:
            return None
        for key, value in vars(ticket_update).items():
            if value is not None and not key.startswith("_"):
                setattr(ticket, key, value)
        db.commit()
        db.refresh(ticket)
        return ticket

    def delete_ticket(self, db: Session, id_ticket: int) -> bool:
        # Elimina un ticket de la base de datos
        ticket = db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()
        if ticket is None:
            return False
        db.delete(ticket)
        db.commit()
        return True

ticket_repository = TicketRepository()