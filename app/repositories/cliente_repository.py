from sqlalchemy.orm import Session

from app.models.clientes import Cliente


class ClienteRepository:

    def create_cliente(self, db: Session, cliente_db: Cliente) -> Cliente:
        # Inserta un cliente en la base de datos.
        db.add(cliente_db)
        db.commit()
        db.refresh(cliente_db)
        return cliente_db

    def get_cliente_by_id(self, db: Session, id_cliente: int) -> Cliente | None:
        # Busca un cliente por su identificador.
        return db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()

    def get_cliente_by_email(self, db: Session, email: str) -> Cliente | None:
        # Busca un cliente por correo electrónico.
        return db.query(Cliente).filter(Cliente.email == email).first()

    def get_list_clientes(self, db: Session) -> list[Cliente]:
        # Lista todos los clientes (sin paginar).
        return db.query(Cliente).all()

    # ── Paginación ───────────────────────────────────────────────────
    def get_list_clientes_paginated(self, db: Session, offset: int, limit: int) -> list[Cliente]:
        # Devuelve solo los registros de una página.
        return db.query(Cliente).offset(offset).limit(limit).all()

    def count_clientes(self, db: Session) -> int:
        # Cuenta el total de clientes para calcular páginas.
        return db.query(Cliente).count()

    def update_cliente(self, db: Session, id_cliente: int, datos: dict) -> Cliente | None:
        """Actualiza campos de un cliente. Recibe dict {campo: valor}.

        Fix: antes recibía una entidad Cliente y usaba vars() con filtro
        `not key.startswith("_")` para evitar _sa_instance_state.
        Ahora recibe dict directamente, estandarizado con los demás repos.
        """
        cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()

        if cliente is None:
            return None

        for key, value in datos.items():
            if value is not None and hasattr(cliente, key):
                setattr(cliente, key, value)

        db.commit()
        db.refresh(cliente)
        return cliente

    def delete_cliente(self, db: Session, id_cliente: int) -> bool:
        # Elimina un cliente de la base de datos.
        cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()

        if cliente is None:
            return False

        db.delete(cliente)
        db.commit()
        return True

# FIX: singleton exportado para que los services no instancien la clase directamente
cliente_repository = ClienteRepository()

