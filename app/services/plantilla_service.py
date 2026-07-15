from sqlalchemy.orm import Session

from app.models.plantilla_formulario import PlantillaFormulario
from app.repositories.plantilla_formulario_repository import plantilla_formulario_repository
from app.schemas.plantilla_formulario_dto import (
    PlantillaFormularioCreateDTO,
    PlantillaFormularioResponseDTO,
    PlantillaFormularioUpdateDTO,
)


class PlantillaService:
    """Servicio para la lógica de negocio de Plantillas de Formulario.

    Nivel: Intermedio-Alto.
    Es el service más complejo de los catálogos porque:
    1. Maneja el campo `estructura_preguntas` (JSONB) que debe ser un
       diccionario válido (Dict[str, Any]).
    2. Tiene `estado_plantilla` (bool) con lógica de activación/
       desactivación — podrías querer validar que solo una plantilla
       esté activa a la vez, o impedir desactivar una en uso.
    3. Está relacionada con `tickets` (un ticket usa una plantilla),
       por lo que un DELETE debería considerar si hay tickets asociados
       (soft-delete recomendado a futuro).

    Conocimientos necesarios:
    - Pydantic v2: `model_validate`, `model_dump(exclude_unset=True)`
    - SQLAlchemy: JSONB column type, relaciones back_populates
    - Regla de oro: el service nunca toca db.add/commit/refresh/delete
    - Validación de tipos: `isinstance(data, dict)` para campos JSONB

    TODO (deuda técnica en el repositorio):
    - `update_plantilla_formulario` aún recibe entidad con vars() —
      debe migrarse a recibir dict como los demás repos.
    - Falta `delete_plantilla_formulario` en el repositorio.
    """

    # ── CREATE ──────────────────────────────────────────────────────
    def create_plantilla(
        self,
        db: Session,
        plantilla_in: PlantillaFormularioCreateDTO,
    ) -> PlantillaFormularioResponseDTO:
        """Crea una nueva plantilla de formulario.

        Valida que `estructura_preguntas` sea un diccionario antes de
        persistir (defensa en profundidad, aunque Pydantic ya lo validó).

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        plantilla_in : PlantillaFormularioCreateDTO
            DTO con nombre_plantilla, estructura_preguntas y estado_plantilla.

        Returns
        -------
        PlantillaFormularioResponseDTO
            DTO con los datos de la plantilla ya persistida.

        Raises
        ------
        ValueError
            Si estructura_preguntas no es un diccionario.
        """
        # Validación extra para JSONB: Pydantic acepta Dict[str, Any] pero
        # un valor mal formado podría colarse si el DTO se construye manualmente.
        if not isinstance(plantilla_in.estructura_preguntas, dict):
            raise ValueError(
                "estructura_preguntas debe ser un diccionario JSON válido"
            )

        plantilla_db = PlantillaFormulario(
            nombre_plantilla=plantilla_in.nombre_plantilla,
            estructura_preguntas=plantilla_in.estructura_preguntas,
            estado_plantilla=plantilla_in.estado_plantilla,
        )
        plantilla_creada = (
            plantilla_formulario_repository.create_plantilla_formulario(
                db, plantilla_db
            )
        )
        return PlantillaFormularioResponseDTO.model_validate(plantilla_creada)

    # ── READ (uno solo) ─────────────────────────────────────────────
    def get_plantilla_by_id(
        self,
        db: Session,
        id_plantilla: int,
    ) -> PlantillaFormularioResponseDTO | None:
        """Obtiene una plantilla por su ID.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        id_plantilla : int
            ID de la plantilla a buscar.

        Returns
        -------
        PlantillaFormularioResponseDTO | None
            DTO de la plantilla si existe; None si no se encuentra.
        """
        plantilla = plantilla_formulario_repository.get_plantilla_formulario_by_id(
            db, id_plantilla
        )
        if plantilla is None:
            return None
        return PlantillaFormularioResponseDTO.model_validate(plantilla)

    # ── READ (listado) ──────────────────────────────────────────────
    def get_all_plantillas(
        self, db: Session
    ) -> list[PlantillaFormularioResponseDTO]:
        """Lista todas las plantillas de formulario.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.

        Returns
        -------
        list[PlantillaFormularioResponseDTO]
            Lista de DTOs (vacía si no hay plantillas).
        """
        plantillas = (
            plantilla_formulario_repository.get_list_plantillas_formulario(db)
        )
        return [
            PlantillaFormularioResponseDTO.model_validate(p) for p in plantillas
        ]

    # ── UPDATE ──────────────────────────────────────────────────────
    def update_plantilla(
        self,
        db: Session,
        id_plantilla: int,
        plantilla_update: PlantillaFormularioUpdateDTO,
    ) -> PlantillaFormularioResponseDTO | None:
        """Actualiza una plantilla (partial update).

        Valida que estructura_preguntas siga siendo un dict si se envía.
        Solo modifica los campos incluidos en el DTO.

        Parameters
        ----------
        db : Session
            Sesión activa de SQLAlchemy.
        id_plantilla : int
            ID de la plantilla a actualizar.
        plantilla_update : PlantillaFormularioUpdateDTO
            DTO con campos opcionales a modificar.

        Returns
        -------
        PlantillaFormularioResponseDTO | None
            DTO actualizado; None si la plantilla no existe.

        Raises
        ------
        ValueError
            Si estructura_preguntas se envía pero no es un dict.
        """
        # Validación extra para JSONB en modo update también
        if plantilla_update.estructura_preguntas is not None:
            if not isinstance(plantilla_update.estructura_preguntas, dict):
                raise ValueError(
                    "estructura_preguntas debe ser un diccionario JSON válido"
                )

        datos = plantilla_update.model_dump(exclude_unset=True)
        if not datos:
            plantilla = (
                plantilla_formulario_repository.get_plantilla_formulario_by_id(
                    db, id_plantilla
                )
            )
            return (
                PlantillaFormularioResponseDTO.model_validate(plantilla)
                if plantilla
                else None
            )

        # TODO: migrar update_plantilla_formulario en el repo para que
        # reciba dict en vez de entidad (mismo fix que canal_repository).
        # Mientras tanto, construimos una entidad temporal con los datos.
        plantilla_temp = PlantillaFormulario(**datos)
        plantilla_actualizada = (
            plantilla_formulario_repository.update_plantilla_formulario(
                db, id_plantilla, plantilla_temp
            )
        )
        if plantilla_actualizada is None:
            return None
        return PlantillaFormularioResponseDTO.model_validate(plantilla_actualizada)

def delete_plantilla(self, db: Session, id_plantilla: int) -> bool:

   
    return plantilla_formulario_repository.delete_plantilla_formulario(
             db, id_plantilla
        )


# Instancia singleton del servicio
plantilla_service = PlantillaService()