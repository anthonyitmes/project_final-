from sqlalchemy.orm import Session

from app.models.tipos_ticket import TipoTicket
from app.repositories.tipo_ticket_repository import tipo_ticket_repository
from app.schemas.tipo_ticket_dto import TipoTicketCreateDTO, TipoTicketResponseDTO, TipoTicketUpdateDTO


class TipoTicketService:
    """Servicio para la lógica de negocio de Tipos de Ticket.

    Nivel: CRUD simple (igual que CanalService).
    El modelo solo tiene 2 campos: id_tipo_ticket + nombre_tipo_ticket.
    Sin validación extra, sin relaciones complejas que manejar aquí.

    Flujo: DTO → Entidad → Repository → DTO
    """

    # ── CREATE ──────────────────────────────────────────────────────
    def create_tipo_ticket(
        self,
        db: Session,
        tipo_in: TipoTicketCreateDTO,
    ) -> TipoTicketResponseDTO:
        """Crea un nuevo tipo de ticket.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        tipo_in : TipoTicketCreateDTO
            DTO con el nombre del tipo de ticket.

        Returns
        -------
        TipoTicketResponseDTO
            DTO con los datos del tipo ya persistido (incluye su id).
        """
        tipo_db = TipoTicket(
            nombre_tipo_ticket=tipo_in.nombre_tipo_ticket,
        )
        tipo_creado = tipo_ticket_repository.create_tipo_ticket(db, tipo_db)
        return TipoTicketResponseDTO.model_validate(tipo_creado)

    # ── READ (uno solo) ─────────────────────────────────────────────
    def get_tipo_ticket_by_id(
        self,
        db: Session,
        id_tipo_ticket: int,
    ) -> TipoTicketResponseDTO | None:
        """Obtiene un tipo de ticket por su ID.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        id_tipo_ticket : int
            ID del tipo de ticket a buscar.

        Returns
        -------
        TipoTicketResponseDTO | None
            DTO del tipo si existe; None si no se encuentra.
        """
        tipo = tipo_ticket_repository.get_tipo_ticket_by_id(db, id_tipo_ticket)
        if tipo is None:
            return None
        return TipoTicketResponseDTO.model_validate(tipo)

    # ── READ (listado) ──────────────────────────────────────────────
    def get_all_tipos_ticket(self, db: Session) -> list[TipoTicketResponseDTO]:
        """Lista todos los tipos de ticket registrados.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.

        Returns
        -------
        list[TipoTicketResponseDTO]
            Lista de DTOs con todos los tipos (vacía si no hay ninguno).
        """
        tipos = tipo_ticket_repository.get_list_tipos_ticket(db)
        return [TipoTicketResponseDTO.model_validate(t) for t in tipos]

    # ── UPDATE ──────────────────────────────────────────────────────
    def update_tipo_ticket(
        self,
        db: Session,
        id_tipo_ticket: int,
        tipo_update: TipoTicketUpdateDTO,
    ) -> TipoTicketResponseDTO | None:
        """Actualiza un tipo de ticket existente (partial update).

        Solo se modifican los campos enviados en el DTO.
        Los campos no incluidos conservan su valor actual.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        id_tipo_ticket : int
            ID del tipo a actualizar.
        tipo_update : TipoTicketUpdateDTO
            DTO con los campos a modificar (todos opcionales).

        Returns
        -------
        TipoTicketResponseDTO | None
            DTO del tipo actualizado; None si no existe.
        """
        datos = tipo_update.model_dump(exclude_unset=True)
        if not datos:
            tipo = tipo_ticket_repository.get_tipo_ticket_by_id(db, id_tipo_ticket)
            return TipoTicketResponseDTO.model_validate(tipo) if tipo else None
        tipo_actualizado = tipo_ticket_repository.update_tipo_ticket(
            db, id_tipo_ticket, datos
        )
        if tipo_actualizado is None:
            return None
        return TipoTicketResponseDTO.model_validate(tipo_actualizado)

    # ── DELETE ──────────────────────────────────────────────────────
    def delete_tipo_ticket(self, db: Session, id_tipo_ticket: int) -> bool:
        """Elimina un tipo de ticket de la base de datos.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        id_tipo_ticket : int
            ID del tipo a eliminar.

        Returns
        -------
        bool
            True si se eliminó; False si no existía.
        """
        return tipo_ticket_repository.delete_tipo_ticket(db, id_tipo_ticket)


# Instancia singleton del servicio
tipo_ticket_service = TipoTicketService()