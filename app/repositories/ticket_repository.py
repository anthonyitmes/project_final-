from sqlalchemy.orm import Session
from app.models.tickets import Ticket

class TicketRepository:

    def create_ticket(self, db: Session, ticket_db: Ticket) -> Ticket:
        #Reciba un modelo ticket ya armado y lo inserta postgresql
        db.add(ticket_db)
        db.commit()
        db.refresh(ticket_db) #recupera el objeto actualizado con el id generado
        return ticket_db
    
    def get_ticket_by_id(self, db: Session, id_ticket: int) -> Ticket | None: 
        #busca un ticket por su id
        return db.query(Ticket).filter(Ticket.id_ticket == id_ticket).first()
    
    def get_list_by_cliente(self, db: Session, id_cliente: int) -> list[Ticket]:
        #busca los tickets de un cliente
        return db.query(Ticket).filter(Ticket.id_cliente == id_cliente).all()

ticket_repository = TicketRepository()