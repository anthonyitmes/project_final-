from sqlalchemy.orm import Session

from app.models.servicios import Servicio
from app.repositories.servicio_repository import servicio_repository
from app.schemas.servicio_dto import ServicioCreateDTO, ServicioResponseDTO, ServicioUpdateDTO


class ServicioService:
    """Servicio para la lógica de negocio de Servicios.

    Nivel: Intermedio bajo.
    Modelo con 2 campos: id_servicio + nombre_servicio.
    Tiene relación con clientes_servicios (tabla asociativa), pero esa
    relación se maneja en ClienteServicioService, no aquí.

    Correcciones aplicadas (05/jul/2026):
    - create: eliminada referencia a campo 'descripcion' que no existe
      en el DTO ni en el modelo.
    - update: ahora convierte DTO → dict con model_dump(exclude_unset=True)
      antes de pasarlo al repositorio. Ya no usa setattr en el service
      (rompía la regla de oro).
    - delete: ahora pasa solo el ID al repositorio, no la entidad completa.
    - Todas las llamadas al repo usan la instancia singleton
      'servicio_repository', no la clase directamente.
    """

    # ── CREATE ──────────────────────────────────────────────────────
    def create_servicio(
        self,
        db: Session,
        servicio_in: ServicioCreateDTO,
    ) -> ServicioResponseDTO:
        """Crea un nuevo servicio en la base de datos.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        servicio_in : ServicioCreateDTO
            DTO con el nombre del servicio.

        Returns
        -------
        ServicioResponseDTO
            DTO con los datos del servicio ya persistido (incluye su id).
        """
        servicio_db = Servicio(
            nombre_servicio=servicio_in.nombre_servicio,
        )
        servicio_creado = servicio_repository.create_servicio(db, servicio_db)
        return ServicioResponseDTO.model_validate(servicio_creado)

    # ── READ (uno solo) ─────────────────────────────────────────────
    def get_servicio_by_id(
        self,
        db: Session,
        id_servicio: int,
    ) -> ServicioResponseDTO | None:
        """Obtiene un servicio por su identificador único.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        id_servicio : int
            ID del servicio a buscar.

        Returns
        -------
        ServicioResponseDTO | None
            DTO del servicio si existe; None si no se encuentra.
        """
        servicio = servicio_repository.get_servicio_by_id(db, id_servicio)
        if servicio is None:
            return None
        return ServicioResponseDTO.model_validate(servicio)

    # ── READ (listado) ──────────────────────────────────────────────
    def get_all_servicios(self, db: Session) -> list[ServicioResponseDTO]:
        """Lista todos los servicios registrados.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.

        Returns
        -------
        list[ServicioResponseDTO]
            Lista de DTOs con todos los servicios (vacía si no hay ninguno).
        """
        servicios = servicio_repository.get_list_servicios(db)
        return [ServicioResponseDTO.model_validate(s) for s in servicios]

    # ── UPDATE ──────────────────────────────────────────────────────
    def update_servicio(
        self,
        db: Session,
        id_servicio: int,
        servicio_in: ServicioUpdateDTO,
    ) -> ServicioResponseDTO | None:
        """Actualiza un servicio existente (partial update).

        Solo se modifican los campos enviados en el DTO.
        Los campos no incluidos conservan su valor actual.

        Fix: antes usaba setattr directamente sobre la entidad en el
        service (rompía la regla de oro). Ahora convierte el DTO a dict
        y se lo pasa al repositorio.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        id_servicio : int
            ID del servicio a actualizar.
        servicio_in : ServicioUpdateDTO
            DTO con los campos a modificar (todos opcionales).

        Returns
        -------
        ServicioResponseDTO | None
            DTO del servicio actualizado; None si no existe.
        """
        datos = servicio_in.model_dump(exclude_unset=True)
        if not datos:
            servicio = servicio_repository.get_servicio_by_id(db, id_servicio)
            return ServicioResponseDTO.model_validate(servicio) if servicio else None
        servicio_actualizado = servicio_repository.update_servicio(
            db, id_servicio, datos
        )
        if servicio_actualizado is None:
            return None
        return ServicioResponseDTO.model_validate(servicio_actualizado)

    # ── DELETE ──────────────────────────────────────────────────────
    def delete_servicio(self, db: Session, id_servicio: int) -> bool:
        """Elimina un servicio de la base de datos.

        Fix: antes pasaba la entidad completa al repositorio.
        Ahora solo pasa el ID (el repo ya sabe cómo hacer el DELETE).

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        id_servicio : int
            ID del servicio a eliminar.

        Returns
        -------
        bool
            True si se eliminó correctamente; False si no existía.
        """
        return servicio_repository.delete_servicio(db, id_servicio)


# Instancia singleton del servicio
servicio_service = ServicioService()