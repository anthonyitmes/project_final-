from sqlalchemy.orm import Session


from app.models.clientes_servicios import ClienteServicio


class ClienteServicioRepository:

	def create_cliente_servicio(self, db: Session, cliente_servicio_db: ClienteServicio) -> ClienteServicio:
		# Inserta la relación cliente-servicio.
		db.add(cliente_servicio_db)
		db.commit()
		db.refresh(cliente_servicio_db)
		return cliente_servicio_db

	def get_cliente_servicio_by_id(self, db: Session, id_cliente_servicio: int) -> ClienteServicio | None:
		# Busca una relación cliente-servicio por su identificador.
		return (
			db.query(ClienteServicio)
			.filter(ClienteServicio.id_cliente_servicio == id_cliente_servicio)
			.first()
		)

	def get_list_by_cliente(self, db: Session, id_cliente: int) -> list[ClienteServicio]:
		# Lista las relaciones de un cliente.
		return db.query(ClienteServicio).filter(ClienteServicio.id_cliente == id_cliente).all()

	def get_list_by_servicio(self, db: Session, id_servicio: int) -> list[ClienteServicio]:
		# Lista las relaciones de un servicio.
		return db.query(ClienteServicio).filter(ClienteServicio.id_servicio == id_servicio).all()

	def get_list_clientes_servicios(self, db: Session) -> list[ClienteServicio]:
		# Lista todas las relaciones cliente-servicio.
		return db.query(ClienteServicio).all()
	
	def update_cliente_servicio(self, db: Session, id_cliente_servicio: int, datos: dict) -> ClienteServicio | None:
		"""Actualiza campos de una relación cliente-servicio. Recibe dict {campo: valor}.

		Fix: antes recibía una entidad ClienteServicio y usaba vars() lo que
		iteraba sobre atributos internos como _sa_instance_state (bug).
		Ahora recibe dict, estandarizado con los demás repos.
		"""
		cliente_servicio = db.query(ClienteServicio).filter(ClienteServicio.id_cliente_servicio == id_cliente_servicio).first()

		if cliente_servicio is None:
			return None
		
		for key, value in datos.items():
			if value is not None and hasattr(cliente_servicio, key):
				setattr(cliente_servicio, key, value)
		db.commit()
		db.refresh(cliente_servicio)
		return cliente_servicio
	
	def delete_cliente_servicio(self, db: Session, id_cliente_servicio: int) -> bool:
		#elimina una relacion cliente servicio de la base de datos
		cliente_servicio = db.query(ClienteServicio).filter(ClienteServicio.id_cliente_servicio == id_cliente_servicio).first()
		if cliente_servicio is None:
			return False
		db.delete(cliente_servicio)
		db.commit()
		return True

cliente_servicio_repository = ClienteServicioRepository()
